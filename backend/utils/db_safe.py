"""
Helpers sécurisés pour les requêtes Supabase
Prévention des injections SQL et sanitisation des inputs

Usage:
    from utils.db_safe import sanitize_like_pattern, safe_ilike, build_or_search

    # Sanitiser un pattern ILIKE
    clean_search = sanitize_like_pattern(user_input)
    query = query.ilike("name", f"%{clean_search}%")

    # Ou utiliser le helper direct
    query = safe_ilike(query, "name", user_input)

    # Recherche multi-colonnes
    query = build_or_search(query, ["name", "description"], user_input)
"""

import re
import structlog
from typing import Optional, List

logger = structlog.get_logger()


def sanitize_like_pattern(value: str) -> str:
    """
    Sanitise une valeur pour utilisation dans un pattern ILIKE

    Échappe les caractères spéciaux SQL:
    - % (wildcard multi-caractères)
    - _ (wildcard single-caractère)
    - \\ (caractère d'échappement)

    Args:
        value: La valeur à sanitiser

    Returns:
        Valeur sanitisée sans caractères spéciaux SQL

    Example:
        >>> sanitize_like_pattern("test%value")
        'testvalue'
        >>> sanitize_like_pattern("test_value")
        'testvalue'
    """
    if not value:
        return ""

    # Supprimer les caractères dangereux pour ILIKE
    # On retire % et _ qui sont des wildcards SQL
    cleaned = value.replace("%", "").replace("_", "").replace("\\", "")

    # Optionnel: supprimer d'autres caractères potentiellement dangereux
    # cleaned = re.sub(r'[^\w\s\-éèêëàâäôöûüîïç]', '', cleaned, flags=re.IGNORECASE)

    return cleaned.strip()


def sanitize_sql_identifier(value: str) -> str:
    """
    Sanitise un identifiant SQL (nom de table, colonne, etc.)

    N'accepte que: lettres, chiffres, underscore

    Args:
        value: L'identifiant à sanitiser

    Returns:
        Identifiant sanitisé

    Example:
        >>> sanitize_sql_identifier("users; DROP TABLE")
        'usersDROPTABLE'
    """
    if not value:
        return ""

    # Ne garder que les caractères alphanumériques et underscore
    cleaned = re.sub(r'[^\w]', '', value)

    return cleaned


def safe_ilike(query, column: str, search_value: Optional[str], wildcard: str = "both") -> object:
    """
    Effectue un ILIKE de manière sécurisée

    Args:
        query: La query Supabase
        column: Nom de la colonne (sanitisé automatiquement)
        search_value: Valeur à rechercher (sanitisée automatiquement)
        wildcard: Position du wildcard - "both" (défaut), "start", "end", "none"

    Returns:
        Query Supabase avec le filtre ILIKE appliqué

    Example:
        >>> query = safe_ilike(query, "name", user_input, wildcard="both")
        # Équivaut à: query.ilike("name", "%search%")
    """
    if not search_value:
        return query

    # Sanitiser le nom de colonne
    clean_column = sanitize_sql_identifier(column)

    # Sanitiser la valeur de recherche
    clean_value = sanitize_like_pattern(search_value)

    if not clean_value:
        logger.warning("safe_ilike_empty_value", column=column, original=search_value)
        return query

    # Construire le pattern selon le wildcard
    if wildcard == "both":
        pattern = f"%{clean_value}%"
    elif wildcard == "start":
        pattern = f"%{clean_value}"
    elif wildcard == "end":
        pattern = f"{clean_value}%"
    else:  # none
        pattern = clean_value

    return query.ilike(clean_column, pattern)


def build_or_search(query, columns: List[str], search_value: Optional[str]) -> object:
    """
    Construit une recherche OR sur plusieurs colonnes de manière sécurisée

    Args:
        query: La query Supabase
        columns: Liste des noms de colonnes
        search_value: Valeur à rechercher

    Returns:
        Query Supabase avec les filtres OR appliqués

    Example:
        >>> query = build_or_search(query, ["name", "description"], "laptop")
        # Équivaut à: query.or_("name.ilike.%laptop%,description.ilike.%laptop%")
    """
    if not search_value or not columns:
        return query

    # Sanitiser la valeur
    clean_value = sanitize_like_pattern(search_value)

    if not clean_value:
        logger.warning("build_or_search_empty_value", columns=columns, original=search_value)
        return query

    # Construire les conditions OR
    or_conditions = []
    for col in columns:
        clean_col = sanitize_sql_identifier(col)
        or_conditions.append(f"{clean_col}.ilike.%{clean_value}%")

    or_string = ",".join(or_conditions)

    return query.or_(or_string)


def validate_sort_field(
    field: str,
    allowed_fields: List[str],
    default: str = "created_at"
) -> str:
    """
    Valide un champ de tri contre une whitelist

    Args:
        field: Le champ de tri demandé
        allowed_fields: Liste des champs autorisés
        default: Champ par défaut si invalide

    Returns:
        Champ de tri validé

    Example:
        >>> field = validate_sort_field("price", ["name", "price", "created_at"])
        'price'
        >>> field = validate_sort_field("malicious", ["name", "price"], "created_at")
        'created_at'
    """
    clean_field = sanitize_sql_identifier(field)

    if clean_field in allowed_fields:
        return clean_field

    logger.warning("invalid_sort_field", requested=field, allowed=allowed_fields)
    return default


def validate_order(order: str, default: str = "desc") -> str:
    """
    Valide l'ordre de tri (asc/desc)

    Args:
        order: L'ordre demandé
        default: Ordre par défaut

    Returns:
        "asc" ou "desc"

    Example:
        >>> validate_order("asc")
        'asc'
        >>> validate_order("invalid")
        'desc'
    """
    order_lower = order.lower().strip()

    if order_lower in ["asc", "desc"]:
        return order_lower

    logger.warning("invalid_order", requested=order, default=default)
    return default


def safe_numeric_filter(value: any, min_val: Optional[float] = None, max_val: Optional[float] = None) -> Optional[float]:
    """
    Valide et sanitise une valeur numérique

    Args:
        value: Valeur à valider
        min_val: Valeur minimale autorisée
        max_val: Valeur maximale autorisée

    Returns:
        Valeur numérique validée ou None

    Example:
        >>> safe_numeric_filter("100", 0, 1000)
        100.0
        >>> safe_numeric_filter("-50", 0, 1000)
        None
    """
    try:
        num_value = float(value)

        if min_val is not None and num_value < min_val:
            logger.warning("numeric_filter_below_min", value=num_value, min=min_val)
            return None

        if max_val is not None and num_value > max_val:
            logger.warning("numeric_filter_above_max", value=num_value, max=max_val)
            return None

        return num_value

    except (ValueError, TypeError):
        logger.warning("numeric_filter_invalid", value=value)
        return None


# Export all functions
__all__ = [
    "sanitize_like_pattern",
    "sanitize_sql_identifier",
    "safe_ilike",
    "build_or_search",
    "validate_sort_field",
    "validate_order",
    "safe_numeric_filter",
]
