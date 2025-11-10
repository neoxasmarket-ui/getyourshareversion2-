/**
 * Composant Image Optimisée avec support responsive et lazy loading
 * Features: WebP/AVIF avec fallback, blur placeholder, intersection observer
 */
import React, { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';

/**
 * Composant OptimizedImage
 * Gère le chargement optimisé d'images avec multiple formats et srcset
 */
const OptimizedImage = ({
  src,
  alt,
  width,
  height,
  sizes,
  srcSetWebP,
  srcSetJpeg,
  srcSetAvif,
  blurhash,
  className = '',
  objectFit = 'cover',
  objectPosition = 'center',
  loading = 'lazy',
  priority = false,
  onLoad,
  onError,
  fallbackSrc,
  showSkeleton = true,
  skeletonColor = '#e0e0e0',
  blurAmount = 20,
  threshold = 0.01,
  rootMargin = '50px',
  quality = 85,
}) => {
  // États
  const [isLoaded, setIsLoaded] = useState(false);
  const [isInView, setIsInView] = useState(priority || loading !== 'lazy');
  const [hasError, setHasError] = useState(false);
  const [currentSrc, setCurrentSrc] = useState(null);

  // Refs
  const imgRef = useRef(null);
  const observerRef = useRef(null);

  /**
   * Intersection Observer pour lazy loading
   */
  useEffect(() => {
    if (priority || loading !== 'lazy' || !imgRef.current) {
      return;
    }

    // Créer l'observer
    observerRef.current = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsInView(true);
            // Arrêter d'observer une fois visible
            if (observerRef.current && imgRef.current) {
              observerRef.current.unobserve(imgRef.current);
            }
          }
        });
      },
      {
        threshold,
        rootMargin,
      }
    );

    // Observer l'élément
    observerRef.current.observe(imgRef.current);

    // Cleanup
    return () => {
      if (observerRef.current && imgRef.current) {
        observerRef.current.unobserve(imgRef.current);
      }
    };
  }, [priority, loading, threshold, rootMargin]);

  /**
   * Gestion du chargement de l'image
   */
  const handleLoad = (e) => {
    setIsLoaded(true);
    setHasError(false);
    if (onLoad) {
      onLoad(e);
    }
  };

  /**
   * Gestion des erreurs de chargement
   */
  const handleError = (e) => {
    setHasError(true);
    if (fallbackSrc && currentSrc !== fallbackSrc) {
      setCurrentSrc(fallbackSrc);
    } else if (onError) {
      onError(e);
    }
  };

  /**
   * Styles du conteneur
   */
  const containerStyle = {
    position: 'relative',
    width: width || '100%',
    height: height || 'auto',
    overflow: 'hidden',
    backgroundColor: skeletonColor,
  };

  /**
   * Styles de l'image
   */
  const imgStyle = {
    width: '100%',
    height: '100%',
    objectFit,
    objectPosition,
    transition: 'opacity 0.3s ease-in-out',
    opacity: isLoaded ? 1 : 0,
  };

  /**
   * Styles du placeholder blur
   */
  const blurPlaceholderStyle = {
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    backgroundColor: blurhash || skeletonColor,
    filter: `blur(${blurAmount}px)`,
    transform: 'scale(1.1)',
    transition: 'opacity 0.3s ease-in-out',
    opacity: isLoaded ? 0 : 1,
    pointerEvents: 'none',
  };

  /**
   * Skeleton loading animation
   */
  const skeletonStyle = {
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    background: `linear-gradient(90deg, ${skeletonColor} 25%, #f0f0f0 50%, ${skeletonColor} 75%)`,
    backgroundSize: '200% 100%',
    animation: 'skeleton-loading 1.5s ease-in-out infinite',
    opacity: isLoaded ? 0 : 1,
    transition: 'opacity 0.3s ease-in-out',
  };

  /**
   * Styles de l'overlay d'erreur
   */
  const errorStyle = {
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f5f5f5',
    color: '#999',
    fontSize: '14px',
    fontFamily: 'system-ui, -apple-system, sans-serif',
  };

  /**
   * Déterminer quelle source utiliser
   */
  useEffect(() => {
    if (hasError && fallbackSrc) {
      setCurrentSrc(fallbackSrc);
    } else {
      setCurrentSrc(src);
    }
  }, [src, fallbackSrc, hasError]);

  /**
   * Rendu du skeleton pendant le chargement
   */
  const renderSkeleton = () => {
    if (!showSkeleton || isLoaded) {
      return null;
    }

    return (
      <>
        <div style={skeletonStyle} aria-hidden="true" />
        <style>
          {`
            @keyframes skeleton-loading {
              0% {
                background-position: 200% 0;
              }
              100% {
                background-position: -200% 0;
              }
            }
          `}
        </style>
      </>
    );
  };

  /**
   * Rendu du placeholder blur
   */
  const renderBlurPlaceholder = () => {
    if (!blurhash || isLoaded) {
      return null;
    }

    return <div style={blurPlaceholderStyle} aria-hidden="true" />;
  };

  /**
   * Rendu de l'overlay d'erreur
   */
  const renderError = () => {
    if (!hasError || fallbackSrc) {
      return null;
    }

    return (
      <div style={errorStyle} role="alert">
        <svg
          width="48"
          height="48"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
          <circle cx="8.5" cy="8.5" r="1.5" />
          <polyline points="21 15 16 10 5 21" />
        </svg>
        <p style={{ marginTop: '8px', fontSize: '12px' }}>Image indisponible</p>
      </div>
    );
  };

  /**
   * Rendu conditionnel - ne charge pas l'image si pas visible
   */
  if (!isInView) {
    return (
      <div ref={imgRef} style={containerStyle} className={className}>
        {renderSkeleton()}
        {renderBlurPlaceholder()}
      </div>
    );
  }

  return (
    <div ref={imgRef} style={containerStyle} className={className}>
      {renderSkeleton()}
      {renderBlurPlaceholder()}
      {renderError()}

      <picture>
        {/* Format AVIF (meilleure compression) */}
        {srcSetAvif && (
          <source type="image/avif" srcSet={srcSetAvif} sizes={sizes} />
        )}

        {/* Format WebP (bon support) */}
        {srcSetWebP && (
          <source type="image/webp" srcSet={srcSetWebP} sizes={sizes} />
        )}

        {/* Format JPEG (fallback) */}
        {srcSetJpeg && (
          <source type="image/jpeg" srcSet={srcSetJpeg} sizes={sizes} />
        )}

        {/* Image par défaut */}
        <img
          src={currentSrc || src}
          alt={alt}
          width={width}
          height={height}
          style={imgStyle}
          onLoad={handleLoad}
          onError={handleError}
          loading={priority ? 'eager' : loading}
          decoding={priority ? 'sync' : 'async'}
          fetchpriority={priority ? 'high' : 'auto'}
          draggable="false"
        />
      </picture>
    </div>
  );
};

OptimizedImage.propTypes = {
  /** URL source de l'image */
  src: PropTypes.string.isRequired,

  /** Texte alternatif pour l'accessibilité */
  alt: PropTypes.string.isRequired,

  /** Largeur de l'image */
  width: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),

  /** Hauteur de l'image */
  height: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),

  /** Tailles responsive (attribut sizes) */
  sizes: PropTypes.string,

  /** Srcset pour format WebP */
  srcSetWebP: PropTypes.string,

  /** Srcset pour format JPEG */
  srcSetJpeg: PropTypes.string,

  /** Srcset pour format AVIF */
  srcSetAvif: PropTypes.string,

  /** Blurhash ou couleur de placeholder */
  blurhash: PropTypes.string,

  /** Classes CSS additionnelles */
  className: PropTypes.string,

  /** Comportement object-fit CSS */
  objectFit: PropTypes.oneOf(['cover', 'contain', 'fill', 'none', 'scale-down']),

  /** Position de l'objet CSS */
  objectPosition: PropTypes.string,

  /** Type de chargement (lazy/eager) */
  loading: PropTypes.oneOf(['lazy', 'eager']),

  /** Image prioritaire (désactive lazy loading) */
  priority: PropTypes.bool,

  /** Callback lors du chargement */
  onLoad: PropTypes.func,

  /** Callback lors d'une erreur */
  onError: PropTypes.func,

  /** URL de fallback en cas d'erreur */
  fallbackSrc: PropTypes.string,

  /** Afficher le skeleton pendant le chargement */
  showSkeleton: PropTypes.bool,

  /** Couleur du skeleton */
  skeletonColor: PropTypes.string,

  /** Intensité du blur du placeholder */
  blurAmount: PropTypes.number,

  /** Seuil de l'intersection observer (0-1) */
  threshold: PropTypes.number,

  /** Marge de l'intersection observer */
  rootMargin: PropTypes.string,

  /** Qualité de l'image (non utilisé directement, pour documentation) */
  quality: PropTypes.number,
};

OptimizedImage.defaultProps = {
  width: undefined,
  height: undefined,
  sizes: '100vw',
  srcSetWebP: undefined,
  srcSetJpeg: undefined,
  srcSetAvif: undefined,
  blurhash: undefined,
  className: '',
  objectFit: 'cover',
  objectPosition: 'center',
  loading: 'lazy',
  priority: false,
  onLoad: undefined,
  onError: undefined,
  fallbackSrc: undefined,
  showSkeleton: true,
  skeletonColor: '#e0e0e0',
  blurAmount: 20,
  threshold: 0.01,
  rootMargin: '50px',
  quality: 85,
};

export default OptimizedImage;
