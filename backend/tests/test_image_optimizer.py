"""
Tests unitaires pour le système d'optimisation d'images
"""
import pytest
import io
from pathlib import Path
from PIL import Image

from backend.services.image_optimizer import ImageOptimizer
from backend.utils.image_processing import (
    validate_image,
    calculate_optimal_quality,
    generate_blurhash,
    analyze_image_colors,
    calculate_sharpness,
    estimate_compression_ratio,
    get_safe_filename,
    ImageValidationError
)


# Fixtures

@pytest.fixture
def sample_image_data():
    """Crée une image de test en mémoire"""
    img = Image.new('RGB', (800, 600), color=(73, 109, 137))
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    return buffer.getvalue()


@pytest.fixture
def sample_png_data():
    """Crée une image PNG avec transparence"""
    img = Image.new('RGBA', (400, 300), color=(255, 0, 0, 128))
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()


@pytest.fixture
def optimizer():
    """Instance d'ImageOptimizer pour les tests"""
    return ImageOptimizer(
        storage_path='/tmp/test_images',
        enable_avif=True,
        enable_webp=True
    )


# Tests de validation

class TestImageValidation:
    """Tests de la validation d'images"""

    def test_validate_valid_jpeg(self, sample_image_data):
        """Test validation d'un JPEG valide"""
        result = validate_image(sample_image_data, 'test.jpg')

        assert result['valid'] is True
        assert result['format'] == 'jpeg'
        assert result['width'] == 800
        assert result['height'] == 600
        assert 'hash' in result

    def test_validate_valid_png(self, sample_png_data):
        """Test validation d'un PNG valide"""
        result = validate_image(sample_png_data, 'test.png')

        assert result['valid'] is True
        assert result['format'] == 'png'
        assert result['mode'] == 'RGBA'

    def test_validate_empty_file(self):
        """Test validation d'un fichier vide"""
        with pytest.raises(ImageValidationError, match="vide"):
            validate_image(b'', 'empty.jpg')

    def test_validate_too_large(self, sample_image_data):
        """Test validation d'un fichier trop grand"""
        with pytest.raises(ImageValidationError, match="trop grande"):
            validate_image(sample_image_data, 'large.jpg', max_size=100)

    def test_validate_unsupported_format(self, sample_image_data):
        """Test validation d'un format non supporté"""
        with pytest.raises(ImageValidationError, match="non supporté"):
            validate_image(sample_image_data, 'test.bmp')

    def test_validate_corrupted_data(self):
        """Test validation de données corrompues"""
        with pytest.raises(ImageValidationError, match="corrompue"):
            validate_image(b'not an image', 'corrupt.jpg')


# Tests d'optimisation

class TestImageOptimizer:
    """Tests du service ImageOptimizer"""

    def test_optimize_image_success(self, optimizer, sample_image_data):
        """Test optimisation réussie"""
        result = optimizer.optimize_image(
            image_data=sample_image_data,
            filename='test.jpg'
        )

        assert result['success'] is True
        assert 'optimized' in result
        assert 'webp' in result['optimized']
        assert 'jpeg' in result['optimized']
        assert result['optimized']['webp']['size'] < len(sample_image_data)

    def test_optimize_with_custom_quality(self, optimizer, sample_image_data):
        """Test optimisation avec qualité personnalisée"""
        result = optimizer.optimize_image(
            image_data=sample_image_data,
            filename='test.jpg',
            quality=90
        )

        assert result['success'] is True
        assert result['optimized']['jpeg']['quality'] == 90

    def test_optimize_png_with_transparency(self, optimizer, sample_png_data):
        """Test optimisation PNG avec transparence"""
        result = optimizer.optimize_image(
            image_data=sample_png_data,
            filename='test.png',
            generate_formats=['webp', 'png']
        )

        assert result['success'] is True
        assert 'webp' in result['optimized']
        assert 'png' in result['optimized']

    def test_generate_thumbnails(self, optimizer, sample_image_data):
        """Test génération de thumbnails"""
        result = optimizer.generate_thumbnails(
            image_data=sample_image_data,
            filename='test.jpg'
        )

        assert result['success'] is True
        assert 'thumbnails' in result
        assert 'thumbnail' in result['thumbnails']
        assert 'small' in result['thumbnails']
        assert 'medium' in result['thumbnails']
        assert 'large' in result['thumbnails']
        assert 'xl' in result['thumbnails']

    def test_thumbnail_dimensions(self, optimizer, sample_image_data):
        """Test que les thumbnails ont les bonnes dimensions"""
        result = optimizer.generate_thumbnails(
            image_data=sample_image_data,
            filename='test.jpg'
        )

        thumbnail = result['thumbnails']['thumbnail']['jpeg']
        assert thumbnail['dimensions']['width'] == 150
        assert thumbnail['dimensions']['height'] == 150

    def test_extract_metadata(self, optimizer, sample_image_data):
        """Test extraction de métadonnées"""
        img = Image.open(io.BytesIO(sample_image_data))
        metadata = optimizer.extract_metadata(img, 'test.jpg')

        assert 'dimensions' in metadata
        assert 'colors' in metadata
        assert 'blurhash' in metadata
        assert 'sharpness' in metadata
        assert metadata['dimensions']['width'] == 800
        assert metadata['dimensions']['height'] == 600

    def test_compress_smart(self, optimizer, sample_image_data):
        """Test compression intelligente"""
        result = optimizer.compress_smart(
            image_data=sample_image_data,
            filename='test.jpg',
            preserve_quality=True
        )

        assert result['success'] is True
        assert result['compressed_size'] < result['original_size']
        assert result['compression']['percentage'] > 0

    def test_compress_smart_with_target(self, optimizer, sample_image_data):
        """Test compression avec taille cible"""
        result = optimizer.compress_smart(
            image_data=sample_image_data,
            filename='test.jpg',
            target_size_kb=50,
            preserve_quality=False
        )

        assert result['success'] is True
        # La taille devrait être proche de 50KB
        assert result['compressed_size'] <= 60 * 1024  # Marge de 10KB

    def test_generate_responsive_srcset(self, optimizer, sample_image_data):
        """Test génération de srcset responsive"""
        result = optimizer.generate_responsive_srcset(
            image_data=sample_image_data,
            filename='test.jpg',
            base_url='https://cdn.example.com'
        )

        assert result['success'] is True
        assert 'srcset' in result
        assert 'webp' in result['srcset']
        assert 'jpeg' in result['srcset']
        assert '320w' in result['srcset']['webp']
        assert 'cdn.example.com' in result['srcset']['webp']


# Tests des utilitaires

class TestImageProcessingUtils:
    """Tests des fonctions utilitaires"""

    def test_calculate_optimal_quality_jpeg(self):
        """Test calcul qualité optimale JPEG"""
        img = Image.new('RGB', (800, 600), color=(100, 100, 100))
        quality = calculate_optimal_quality(img, 'jpeg')

        assert 50 <= quality <= 100
        assert isinstance(quality, int)

    def test_calculate_optimal_quality_webp(self):
        """Test calcul qualité optimale WebP"""
        img = Image.new('RGB', (800, 600))
        quality = calculate_optimal_quality(img, 'webp')

        assert 50 <= quality <= 100

    def test_generate_blurhash(self):
        """Test génération blurhash"""
        img = Image.new('RGB', (100, 100), color=(255, 0, 0))
        blurhash = generate_blurhash(img)

        assert blurhash is not None
        assert blurhash.startswith('#')  # Format hex
        assert len(blurhash) == 7  # #RRGGBB

    def test_analyze_image_colors(self):
        """Test analyse palette de couleurs"""
        img = Image.new('RGB', (100, 100), color=(255, 0, 0))
        colors = analyze_image_colors(img, num_colors=3)

        assert len(colors) <= 3
        assert all('hex' in c for c in colors)
        assert all('rgb' in c for c in colors)
        assert all('hsl' in c for c in colors)

    def test_calculate_sharpness(self):
        """Test calcul de netteté"""
        img = Image.new('RGB', (100, 100), color=(128, 128, 128))
        sharpness = calculate_sharpness(img)

        assert isinstance(sharpness, float)
        assert sharpness >= 0

    def test_estimate_compression_ratio(self):
        """Test calcul ratio de compression"""
        stats = estimate_compression_ratio(1000, 500)

        assert stats['ratio'] == 0.5
        assert stats['percentage'] == 50.0
        assert stats['saved_bytes'] == 500
        assert stats['saved_kb'] == 0.49  # Arrondi

    def test_estimate_compression_ratio_zero(self):
        """Test ratio avec taille nulle"""
        stats = estimate_compression_ratio(0, 0)

        assert stats['ratio'] == 0
        assert stats['percentage'] == 0

    def test_get_safe_filename(self):
        """Test nettoyage nom de fichier"""
        safe = get_safe_filename('Mon Fichier (2023)!.jpg')

        assert ' ' not in safe
        assert '(' not in safe
        assert ')' not in safe
        assert '!' not in safe
        assert safe.endswith('.jpg')

    def test_get_safe_filename_long(self):
        """Test nom de fichier trop long"""
        long_name = 'a' * 300 + '.jpg'
        safe = get_safe_filename(long_name, max_length=100)

        assert len(safe) <= 100
        assert safe.endswith('.jpg')


# Tests d'intégration

class TestIntegration:
    """Tests d'intégration end-to-end"""

    def test_full_pipeline(self, optimizer, sample_image_data):
        """Test pipeline complet d'optimisation"""
        # 1. Valider
        validation = validate_image(sample_image_data, 'test.jpg')
        assert validation['valid']

        # 2. Optimiser
        optimized = optimizer.optimize_image(
            image_data=sample_image_data,
            filename='test.jpg'
        )
        assert optimized['success']

        # 3. Générer thumbnails
        thumbnails = optimizer.generate_thumbnails(
            image_data=sample_image_data,
            filename='test.jpg'
        )
        assert thumbnails['success']

        # 4. Générer srcset
        srcset = optimizer.generate_responsive_srcset(
            image_data=sample_image_data,
            filename='test.jpg'
        )
        assert srcset['success']

    def test_error_handling_invalid_image(self, optimizer):
        """Test gestion d'erreur avec image invalide"""
        result = optimizer.optimize_image(
            image_data=b'invalid data',
            filename='test.jpg'
        )

        assert result['success'] is False
        assert 'error' in result
        assert result['error_type'] == 'validation'


# Tests de performance

class TestPerformance:
    """Tests de performance"""

    def test_large_image_optimization(self, optimizer):
        """Test optimisation d'une grande image"""
        # Créer une grande image
        img = Image.new('RGB', (4000, 3000), color=(255, 0, 0))
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        large_data = buffer.getvalue()

        import time
        start = time.time()

        result = optimizer.optimize_image(
            image_data=large_data,
            filename='large.jpg'
        )

        duration = time.time() - start

        assert result['success']
        assert duration < 5.0  # Devrait prendre moins de 5 secondes

    def test_batch_processing_performance(self, optimizer, sample_image_data):
        """Test performance traitement par lot"""
        import time

        start = time.time()

        # Traiter 10 images
        for i in range(10):
            optimizer.optimize_image(
                image_data=sample_image_data,
                filename=f'test_{i}.jpg'
            )

        duration = time.time() - start

        # 10 images en moins de 10 secondes
        assert duration < 10.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
