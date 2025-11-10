/**
 * Optimized Image Component
 * Features:
 * - Lazy loading with IntersectionObserver
 * - Blur-up placeholder effect
 * - WebP/AVIF with fallback
 * - Responsive srcset
 * - Prevents CLS with aspect ratio
 */
import React, { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';

const OptimizedImage = ({
  src,
  alt,
  width,
  height,
  sizes = '100vw',
  className = '',
  blurDataURL,
  priority = false,
  onLoad,
  onClick,
  style = {},
  objectFit = 'cover',
  quality = 85
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isInView, setIsInView] = useState(priority);
  const [error, setError] = useState(false);
  const imgRef = useRef(null);

  // Calculate aspect ratio to prevent CLS
  const aspectRatio = width && height ? (height / width) * 100 : null;

  // IntersectionObserver for lazy loading
  useEffect(() => {
    if (priority || !imgRef.current) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsInView(true);
            observer.unobserve(entry.target);
          }
        });
      },
      {
        rootMargin: '50px 0px',
        threshold: 0.01
      }
    );

    observer.observe(imgRef.current);

    return () => {
      if (imgRef.current) {
        observer.unobserve(imgRef.current);
      }
    };
  }, [priority]);

  // Generate srcset for responsive images
  const generateSrcSet = (baseSrc) => {
    if (!baseSrc) return '';

    const widths = [320, 640, 768, 1024, 1280, 1536, 1920];
    const extension = baseSrc.split('.').pop();
    const baseUrl = baseSrc.replace(`.${extension}`, '');

    return widths
      .map((w) => {
        // Assume CDN supports size parameters
        return `${baseUrl}_${w}.${extension} ${w}w`;
      })
      .join(', ');
  };

  // Generate WebP srcset
  const generateWebPSrcSet = (baseSrc) => {
    if (!baseSrc) return '';

    const widths = [320, 640, 768, 1024, 1280, 1536, 1920];
    const extension = baseSrc.split('.').pop();
    const baseUrl = baseSrc.replace(`.${extension}`, '');

    return widths
      .map((w) => `${baseUrl}_${w}.webp ${w}w`)
      .join(', ');
  };

  // Generate AVIF srcset (best compression)
  const generateAVIFSrcSet = (baseSrc) => {
    if (!baseSrc) return '';

    const widths = [320, 640, 768, 1024, 1280, 1536, 1920];
    const extension = baseSrc.split('.').pop();
    const baseUrl = baseSrc.replace(`.${extension}`, '');

    return widths
      .map((w) => `${baseUrl}_${w}.avif ${w}w`)
      .join(', ');
  };

  const handleLoad = (e) => {
    setIsLoaded(true);
    if (onLoad) onLoad(e);
  };

  const handleError = () => {
    setError(true);
  };

  // Placeholder styles
  const placeholderStyle = {
    position: 'relative',
    overflow: 'hidden',
    backgroundColor: '#f0f0f0',
    ...(aspectRatio && {
      paddingBottom: `${aspectRatio}%`,
      height: 0
    }),
    ...(!aspectRatio && height && { height }),
    ...style
  };

  const imgStyle = {
    position: aspectRatio ? 'absolute' : 'relative',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    objectFit,
    transition: 'opacity 0.3s ease-in-out, filter 0.3s ease-in-out',
    opacity: isLoaded ? 1 : 0,
    filter: isLoaded ? 'blur(0)' : 'blur(10px)'
  };

  // Blur placeholder image (base64 encoded tiny image)
  const blurPlaceholder = blurDataURL || 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"%3E%3Crect fill="%23f0f0f0" width="400" height="300"/%3E%3C/svg%3E';

  if (error) {
    return (
      <div
        className={`optimized-image-error ${className}`}
        style={placeholderStyle}
      >
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            textAlign: 'center',
            color: '#999'
          }}
        >
          <svg
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
            <circle cx="8.5" cy="8.5" r="1.5" />
            <polyline points="21 15 16 10 5 21" />
          </svg>
          <p style={{ fontSize: '12px', marginTop: '8px' }}>Image unavailable</p>
        </div>
      </div>
    );
  }

  return (
    <div
      ref={imgRef}
      className={`optimized-image ${className} ${isLoaded ? 'loaded' : 'loading'}`}
      style={placeholderStyle}
      onClick={onClick}
    >
      {/* Blur placeholder (always show immediately) */}
      {!isLoaded && (
        <img
          src={blurPlaceholder}
          alt=""
          aria-hidden="true"
          style={{
            ...imgStyle,
            opacity: 1,
            filter: 'blur(10px)',
            transform: 'scale(1.1)'
          }}
        />
      )}

      {/* Actual image (load when in view) */}
      {isInView && (
        <picture>
          {/* AVIF - Best compression (40-50% smaller than WebP) */}
          <source
            type="image/avif"
            srcSet={generateAVIFSrcSet(src)}
            sizes={sizes}
          />

          {/* WebP - Good compression (25-35% smaller than JPEG) */}
          <source
            type="image/webp"
            srcSet={generateWebPSrcSet(src)}
            sizes={sizes}
          />

          {/* Fallback - Original format */}
          <img
            src={src}
            srcSet={generateSrcSet(src)}
            sizes={sizes}
            alt={alt}
            width={width}
            height={height}
            loading={priority ? 'eager' : 'lazy'}
            decoding="async"
            style={imgStyle}
            onLoad={handleLoad}
            onError={handleError}
          />
        </picture>
      )}

      {/* Loading spinner */}
      {!isLoaded && isInView && (
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)'
          }}
        >
          <div
            className="spinner-border"
            style={{
              width: '2rem',
              height: '2rem',
              borderWidth: '3px',
              color: '#6366f1'
            }}
          />
        </div>
      )}
    </div>
  );
};

OptimizedImage.propTypes = {
  src: PropTypes.string.isRequired,
  alt: PropTypes.string.isRequired,
  width: PropTypes.number,
  height: PropTypes.number,
  sizes: PropTypes.string,
  className: PropTypes.string,
  blurDataURL: PropTypes.string,
  priority: PropTypes.bool,
  onLoad: PropTypes.func,
  onClick: PropTypes.func,
  style: PropTypes.object,
  objectFit: PropTypes.oneOf(['cover', 'contain', 'fill', 'none', 'scale-down']),
  quality: PropTypes.number
};

export default OptimizedImage;

/**
 * Hook for generating blur placeholder
 * Usage: const blurDataURL = useBlurPlaceholder(imageUrl);
 */
export const useBlurPlaceholder = (src) => {
  const [blurDataURL, setBlurDataURL] = useState(null);

  useEffect(() => {
    if (!src) return;

    // Generate tiny placeholder (10px width)
    const img = new Image();
    img.crossOrigin = 'anonymous';

    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');

      // Very small size for blur effect
      canvas.width = 10;
      canvas.height = 10;

      ctx.drawImage(img, 0, 0, 10, 10);

      try {
        setBlurDataURL(canvas.toDataURL('image/jpeg', 0.1));
      } catch (error) {
        console.error('Failed to generate blur placeholder:', error);
      }
    };

    img.src = src;
  }, [src]);

  return blurDataURL;
};

/**
 * Preload critical images
 */
export const preloadImage = (src, priority = false) => {
  const link = document.createElement('link');
  link.rel = priority ? 'preload' : 'prefetch';
  link.as = 'image';
  link.href = src;

  // Add WebP/AVIF support
  if (src.endsWith('.jpg') || src.endsWith('.png')) {
    const webpSrc = src.replace(/\.(jpg|png)$/, '.webp');
    link.imagesrcset = webpSrc;
    link.imageSizes = '100vw';
  }

  document.head.appendChild(link);
};
