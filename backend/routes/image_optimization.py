"""
Routes API pour l'optimisation d'images
Endpoints pour upload, optimisation et gestion d'images
"""
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import io
from typing import Optional

from services.image_optimizer import ImageOptimizer
from utils.image_processing import validate_image, ImageValidationError, get_safe_filename
from utils.logger import logger

# Créer le blueprint
image_bp = Blueprint('image_optimization', __name__, url_prefix='/api/images')

# Initialiser le service d'optimisation
optimizer = ImageOptimizer(
    storage_path='/var/www/optimized_images',
    enable_avif=True,
    enable_webp=True
)

# Configuration
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'gif'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


def allowed_file(filename: str) -> bool:
    """Vérifie si l'extension du fichier est autorisée"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@image_bp.route('/upload', methods=['POST'])
def upload_image():
    """
    Upload et optimise une image

    Body (multipart/form-data):
        - file: Fichier image
        - formats: Liste des formats à générer (webp,avif,jpeg)
        - quality: Qualité de compression (50-100)
        - generate_thumbnails: Générer thumbnails (true/false)

    Returns:
        JSON avec URLs et métadonnées des images optimisées
    """
    try:
        # Vérifier qu'un fichier est présent
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Aucun fichier fourni'
            }), 400

        file = request.files['file']

        # Vérifier que le fichier a un nom
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nom de fichier vide'
            }), 400

        # Vérifier l'extension
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'Extension non autorisée. Formats acceptés: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400

        # Lire les données du fichier
        file_data = file.read()

        # Vérifier la taille
        if len(file_data) > MAX_FILE_SIZE:
            return jsonify({
                'success': False,
                'error': f'Fichier trop grand. Maximum: {MAX_FILE_SIZE / 1024 / 1024}MB'
            }), 400

        # Nom de fichier sécurisé
        filename = get_safe_filename(secure_filename(file.filename))

        # Paramètres optionnels
        formats = request.form.get('formats', 'webp,jpeg').split(',')
        quality = request.form.get('quality', type=int)
        generate_thumbnails = request.form.get('generate_thumbnails', 'true').lower() == 'true'

        # Optimiser l'image
        result = optimizer.optimize_image(
            image_data=file_data,
            filename=filename,
            generate_formats=formats,
            quality=quality
        )

        if not result['success']:
            return jsonify(result), 400

        # Générer les thumbnails si demandé
        thumbnails = None
        if generate_thumbnails:
            thumb_result = optimizer.generate_thumbnails(
                image_data=file_data,
                filename=filename,
                formats=formats
            )
            if thumb_result['success']:
                thumbnails = thumb_result['thumbnails']

        # Construire la réponse
        response = {
            'success': True,
            'filename': filename,
            'original': result['original'],
            'optimized': {
                fmt: {
                    'size': data['size'],
                    'size_kb': round(data['size'] / 1024, 2),
                    'compression_percentage': data['compression']['percentage'],
                    'quality': data['quality'],
                    'url': f'/api/images/serve/{filename.rsplit(".", 1)[0]}.{fmt}'
                }
                for fmt, data in result['optimized'].items()
            },
            'metadata': result['metadata'],
            'thumbnails': thumbnails,
            'processing_time': result['processing_time']
        }

        logger.info(
            "Image uploadée et optimisée",
            filename=filename,
            formats=formats,
            original_size_kb=result['original']['size'] / 1024
        )

        return jsonify(response), 200

    except ImageValidationError as e:
        logger.error(f"Validation échouée: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': 'validation'
        }), 400

    except Exception as e:
        logger.error(f"Erreur upload image: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Erreur serveur lors du traitement',
            'error_type': 'server'
        }), 500


@image_bp.route('/optimize', methods=['POST'])
def optimize_existing():
    """
    Optimise une image existante (par URL ou ID)

    Body (JSON):
        - image_url: URL de l'image à optimiser
        - image_id: ID de l'image en base de données
        - formats: Liste des formats
        - quality: Qualité

    Returns:
        JSON avec images optimisées
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Body JSON requis'
            }), 400

        # TODO: Récupérer l'image depuis URL ou DB
        # Pour l'exemple, on suppose qu'on a l'image

        return jsonify({
            'success': False,
            'error': 'Non implémenté'
        }), 501

    except Exception as e:
        logger.error(f"Erreur optimisation: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@image_bp.route('/compress', methods=['POST'])
def compress_image():
    """
    Compression intelligente avec taille cible

    Body (multipart/form-data):
        - file: Fichier image
        - target_size_kb: Taille cible en KB
        - preserve_quality: Préserver qualité (true/false)

    Returns:
        Image compressée
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Aucun fichier fourni'
            }), 400

        file = request.files['file']
        file_data = file.read()
        filename = get_safe_filename(secure_filename(file.filename))

        # Paramètres
        target_size_kb = request.form.get('target_size_kb', type=int)
        preserve_quality = request.form.get('preserve_quality', 'true').lower() == 'true'

        # Compression intelligente
        result = optimizer.compress_smart(
            image_data=file_data,
            filename=filename,
            target_size_kb=target_size_kb,
            preserve_quality=preserve_quality
        )

        if not result['success']:
            return jsonify(result), 400

        # Retourner l'image compressée
        return send_file(
            io.BytesIO(result['data']),
            mimetype=f'image/{result["format"]}',
            as_attachment=True,
            download_name=f'compressed_{filename}'
        )

    except Exception as e:
        logger.error(f"Erreur compression: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@image_bp.route('/thumbnails', methods=['POST'])
def generate_thumbnails():
    """
    Génère des thumbnails pour une image

    Body (multipart/form-data):
        - file: Fichier image
        - sizes: Tailles personnalisées (JSON)
        - formats: Formats de sortie

    Returns:
        JSON avec tous les thumbnails
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Aucun fichier fourni'
            }), 400

        file = request.files['file']
        file_data = file.read()
        filename = get_safe_filename(secure_filename(file.filename))

        # Paramètres
        formats = request.form.get('formats', 'webp,jpeg').split(',')
        custom_sizes = request.form.get('sizes')  # JSON optionnel

        # Générer les thumbnails
        result = optimizer.generate_thumbnails(
            image_data=file_data,
            filename=filename,
            sizes=None,  # TODO: Parser custom_sizes si fourni
            formats=formats
        )

        if not result['success']:
            return jsonify(result), 400

        logger.info(
            "Thumbnails générés",
            filename=filename,
            count=len(result['thumbnails'])
        )

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Erreur génération thumbnails: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@image_bp.route('/metadata', methods=['POST'])
def extract_metadata():
    """
    Extrait les métadonnées d'une image

    Body (multipart/form-data):
        - file: Fichier image

    Returns:
        JSON avec métadonnées complètes
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Aucun fichier fourni'
            }), 400

        file = request.files['file']
        file_data = file.read()
        filename = get_safe_filename(secure_filename(file.filename))

        # Valider l'image
        from PIL import Image
        image = Image.open(io.BytesIO(file_data))

        # Extraire métadonnées
        metadata = optimizer.extract_metadata(image, filename)

        logger.info(
            "Métadonnées extraites",
            filename=filename
        )

        return jsonify({
            'success': True,
            'metadata': metadata
        }), 200

    except Exception as e:
        logger.error(f"Erreur extraction métadonnées: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@image_bp.route('/remove-background', methods=['POST'])
def remove_background():
    """
    Supprime le fond d'une image

    Body (multipart/form-data):
        - file: Fichier image
        - output_format: Format de sortie (png, webp)

    Returns:
        Image sans fond
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Aucun fichier fourni'
            }), 400

        file = request.files['file']
        file_data = file.read()
        filename = get_safe_filename(secure_filename(file.filename))

        # Paramètres
        output_format = request.form.get('output_format', 'png')

        # Supprimer le fond
        result = optimizer.remove_background(
            image_data=file_data,
            output_format=output_format
        )

        if not result:
            return jsonify({
                'success': False,
                'error': 'Suppression de fond non disponible (rembg non installé)'
            }), 501

        logger.info(
            "Fond supprimé",
            filename=filename,
            output_format=output_format
        )

        # Retourner l'image
        return send_file(
            io.BytesIO(result),
            mimetype=f'image/{output_format}',
            as_attachment=True,
            download_name=f'no_bg_{filename.rsplit(".", 1)[0]}.{output_format}'
        )

    except Exception as e:
        logger.error(f"Erreur suppression fond: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@image_bp.route('/srcset', methods=['POST'])
def generate_srcset():
    """
    Génère un srcset responsive complet

    Body (multipart/form-data):
        - file: Fichier image
        - base_url: URL de base pour CDN

    Returns:
        JSON avec srcset pour tous les formats
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Aucun fichier fourni'
            }), 400

        file = request.files['file']
        file_data = file.read()
        filename = get_safe_filename(secure_filename(file.filename))

        # Paramètres
        base_url = request.form.get('base_url', request.host_url.rstrip('/'))

        # Générer srcset
        result = optimizer.generate_responsive_srcset(
            image_data=file_data,
            filename=filename,
            base_url=base_url
        )

        if not result['success']:
            return jsonify(result), 400

        logger.info(
            "Srcset généré",
            filename=filename
        )

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Erreur génération srcset: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@image_bp.route('/serve/<path:filename>', methods=['GET'])
def serve_image(filename: str):
    """
    Sert une image optimisée

    Args:
        filename: Nom du fichier avec extension

    Returns:
        Fichier image
    """
    try:
        # TODO: Implémenter selon votre système de stockage
        # (local, S3, etc.)

        return jsonify({
            'success': False,
            'error': 'Non implémenté'
        }), 501

    except Exception as e:
        logger.error(f"Erreur service image: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@image_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint de santé du service d'optimisation"""
    return jsonify({
        'success': True,
        'service': 'image_optimization',
        'status': 'healthy',
        'features': {
            'webp': optimizer.enable_webp,
            'avif': optimizer.enable_avif,
            'background_removal': True  # Vérifier si rembg est installé
        }
    }), 200
