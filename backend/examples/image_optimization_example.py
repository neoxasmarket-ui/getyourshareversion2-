"""
Exemples d'utilisation du système d'optimisation d'images
Démontre toutes les fonctionnalités du ImageOptimizer
"""
import asyncio
from pathlib import Path
from services.image_optimizer import ImageOptimizer
from utils.logger import logger


async def example_basic_optimization():
    """
    Exemple 1: Optimisation basique d'une image
    """
    logger.info("=== Exemple 1: Optimisation basique ===")

    # Initialiser le service
    optimizer = ImageOptimizer(
        storage_path='/tmp/optimized_images',
        enable_avif=True,
        enable_webp=True
    )

    # Charger une image
    with open('example.jpg', 'rb') as f:
        image_data = f.read()

    # Optimiser
    result = optimizer.optimize_image(
        image_data=image_data,
        filename='example.jpg',
        generate_formats=['webp', 'avif', 'jpeg']
    )

    if result['success']:
        logger.info("Optimisation réussie!")
        logger.info(f"Formats générés: {list(result['optimized'].keys())}")

        for fmt, data in result['optimized'].items():
            compression = data['compression']['percentage']
            size_kb = data['size'] / 1024
            logger.info(f"  {fmt}: {size_kb:.2f}KB (compression: {compression:.1f}%)")
    else:
        logger.error(f"Erreur: {result['error']}")


async def example_generate_thumbnails():
    """
    Exemple 2: Génération de thumbnails multiples
    """
    logger.info("=== Exemple 2: Génération de thumbnails ===")

    optimizer = ImageOptimizer()

    with open('example.jpg', 'rb') as f:
        image_data = f.read()

    # Générer tous les thumbnails
    result = optimizer.generate_thumbnails(
        image_data=image_data,
        filename='example.jpg',
        formats=['webp', 'jpeg']
    )

    if result['success']:
        logger.info(f"Tailles générées: {result['sizes_generated']}")

        for size_name, size_data in result['thumbnails'].items():
            for fmt, fmt_data in size_data.items():
                dims = fmt_data['dimensions']
                size_kb = fmt_data['size'] / 1024
                logger.info(
                    f"  {size_name}/{fmt}: {dims['width']}x{dims['height']} "
                    f"({size_kb:.2f}KB)"
                )


async def example_smart_compression():
    """
    Exemple 3: Compression intelligente
    """
    logger.info("=== Exemple 3: Compression intelligente ===")

    optimizer = ImageOptimizer()

    with open('example.jpg', 'rb') as f:
        image_data = f.read()

    # Compression avec taille cible
    result = optimizer.compress_smart(
        image_data=image_data,
        filename='example.jpg',
        target_size_kb=100,  # Maximum 100KB
        preserve_quality=True
    )

    if result['success']:
        stats = result['compression']
        logger.info(f"Format optimal: {result['format']}")
        logger.info(f"Qualité: {result['quality']}")
        logger.info(f"Taille originale: {stats['original_kb']:.2f}KB")
        logger.info(f"Taille compressée: {stats['compressed_kb']:.2f}KB")
        logger.info(f"Économie: {stats['percentage']:.1f}%")
        logger.info(f"Analyse: {result['analysis']}")


async def example_responsive_srcset():
    """
    Exemple 4: Génération de srcset responsive
    """
    logger.info("=== Exemple 4: Srcset responsive ===")

    optimizer = ImageOptimizer()

    with open('example.jpg', 'rb') as f:
        image_data = f.read()

    # Générer srcset complet
    result = optimizer.generate_responsive_srcset(
        image_data=image_data,
        filename='example.jpg',
        base_url='https://cdn.example.com/images'
    )

    if result['success']:
        logger.info("Srcset WebP:")
        logger.info(f"  {result['srcset']['webp']}")
        logger.info("\nSrcset JPEG:")
        logger.info(f"  {result['srcset']['jpeg']}")
        logger.info("\nTailles disponibles:")
        for size, dims in result['sizes'].items():
            if dims:
                logger.info(f"  {size}: {dims['width']}x{dims['height']}")


async def example_metadata_extraction():
    """
    Exemple 5: Extraction de métadonnées complètes
    """
    logger.info("=== Exemple 5: Extraction de métadonnées ===")

    from PIL import Image
    import io

    optimizer = ImageOptimizer()

    with open('example.jpg', 'rb') as f:
        image_data = f.read()

    image = Image.open(io.BytesIO(image_data))
    metadata = optimizer.extract_metadata(image, 'example.jpg')

    logger.info(f"Format: {metadata['format']}")
    logger.info(f"Dimensions: {metadata['dimensions']}")
    logger.info(f"Ratio: {metadata['aspect_ratio']}")
    logger.info(f"Netteté: {metadata['sharpness']:.2f}")
    logger.info(f"Blurhash: {metadata['blurhash']}")
    logger.info(f"Nombre de visages détectés: {len(metadata['faces'])}")
    logger.info("\nCouleurs dominantes:")
    for i, color in enumerate(metadata['colors'][:3], 1):
        logger.info(f"  {i}. {color['hex']} (luminance: {color['luminance']:.2f})")


async def example_background_removal():
    """
    Exemple 6: Suppression de fond (nécessite rembg)
    """
    logger.info("=== Exemple 6: Suppression de fond ===")

    optimizer = ImageOptimizer()

    with open('example.jpg', 'rb') as f:
        image_data = f.read()

    # Supprimer le fond
    result = optimizer.remove_background(
        image_data=image_data,
        output_format='png'
    )

    if result:
        logger.info("Fond supprimé avec succès!")
        logger.info(f"Taille du résultat: {len(result) / 1024:.2f}KB")

        # Sauvegarder
        with open('example_no_bg.png', 'wb') as f:
            f.write(result)
    else:
        logger.warning("Suppression de fond non disponible (rembg non installé)")


async def example_batch_processing():
    """
    Exemple 7: Traitement par lot
    """
    logger.info("=== Exemple 7: Traitement par lot ===")

    optimizer = ImageOptimizer()

    # Liste d'images à traiter
    image_files = [
        'image1.jpg',
        'image2.png',
        'image3.jpg'
    ]

    results = []

    for filename in image_files:
        try:
            with open(filename, 'rb') as f:
                image_data = f.read()

            result = optimizer.optimize_image(
                image_data=image_data,
                filename=filename
            )

            results.append({
                'filename': filename,
                'success': result['success'],
                'formats': list(result.get('optimized', {}).keys()) if result['success'] else [],
                'processing_time': result.get('processing_time', 0)
            })

        except FileNotFoundError:
            logger.warning(f"Fichier non trouvé: {filename}")
            results.append({
                'filename': filename,
                'success': False,
                'error': 'File not found'
            })

    # Résumé
    total = len(results)
    successful = sum(1 for r in results if r['success'])
    total_time = sum(r.get('processing_time', 0) for r in results)

    logger.info(f"\nTraitement terminé:")
    logger.info(f"  Total: {total}")
    logger.info(f"  Réussis: {successful}")
    logger.info(f"  Échoués: {total - successful}")
    logger.info(f"  Temps total: {total_time:.2f}s")


async def example_cdn_ready_urls():
    """
    Exemple 8: Génération d'URLs CDN-ready
    """
    logger.info("=== Exemple 8: URLs CDN-ready ===")

    from utils.image_processing import get_safe_filename

    optimizer = ImageOptimizer()

    with open('Mon Image (2023).jpg', 'rb') as f:
        image_data = f.read()

    # Nom de fichier sécurisé
    safe_name = get_safe_filename('Mon Image (2023).jpg')
    logger.info(f"Nom sécurisé: {safe_name}")

    # Optimiser
    result = optimizer.optimize_image(
        image_data=image_data,
        filename=safe_name
    )

    if result['success']:
        base_url = "https://cdn.example.com"

        logger.info("\nURLs générées:")
        for fmt in result['optimized'].keys():
            url = f"{base_url}/images/{Path(safe_name).stem}.{fmt}"
            logger.info(f"  {fmt}: {url}")


async def main():
    """
    Exécute tous les exemples
    """
    examples = [
        example_basic_optimization,
        example_generate_thumbnails,
        example_smart_compression,
        example_responsive_srcset,
        example_metadata_extraction,
        example_background_removal,
        example_batch_processing,
        example_cdn_ready_urls
    ]

    for example in examples:
        try:
            await example()
            logger.info("\n" + "="*60 + "\n")
        except Exception as e:
            logger.error(f"Erreur dans {example.__name__}: {str(e)}")


if __name__ == "__main__":
    # Exécuter les exemples
    asyncio.run(main())
