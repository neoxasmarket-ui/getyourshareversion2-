import React from 'react';

/**
 * LazyImage Component - Optimized Image Loading
 *
 * Features:
 * - Automatic lazy loading with native loading="lazy"
 * - Responsive image support with srcSet
 * - Aspect ratio support
 * - Error handling with fallback
 * - SEO-friendly with proper alt attributes
 * - Performance optimized with async decoding
 *
 * Usage:
 * <LazyImage
 *   src="/image.jpg"
 *   alt="Image description"
 *   className="w-full h-auto"
 *   width={800}
 *   height={600}
 *   srcSet="/image-320w.jpg 320w, /image-800w.jpg 800w"
 *   sizes="(max-width: 600px) 320px, 800px"
 * />
 */
const LazyImage = ({
  src,
  alt = 'Image',
  className = '',
  width,
  height,
  srcSet,
  sizes,
  onError,
  onLoad,
  aspectRatio,
  placeholder = 'blur',
  ...props
}) => {
  const [isLoaded, setIsLoaded] = React.useState(false);
  const [hasError, setHasError] = React.useState(false);

  const handleLoad = (e) => {
    setIsLoaded(true);
    onLoad?.(e);
  };

  const handleError = (e) => {
    setHasError(true);
    onError?.(e);
  };

  const containerStyle = aspectRatio
    ? { aspectRatio, overflow: 'hidden' }
    : {};

  const imageClass = [
    className,
    'transition-opacity duration-300',
    isLoaded ? 'opacity-100' : 'opacity-75'
  ].filter(Boolean).join(' ');

  return (
    <div style={containerStyle}>
      {hasError ? (
        <div
          className="w-full h-full bg-gray-200 flex items-center justify-center"
          style={{ aspectRatio }}
        >
          <span className="text-gray-400 text-sm">Image non disponible</span>
        </div>
      ) : (
        <img
          src={src}
          alt={alt}
          className={imageClass}
          width={width}
          height={height}
          srcSet={srcSet}
          sizes={sizes}
          loading="lazy"
          decoding="async"
          onLoad={handleLoad}
          onError={handleError}
          {...props}
        />
      )}
    </div>
  );
};

export default LazyImage;
