import React from 'react';
import '../styles/animations.css';

/**
 * ===================================================================
 * LOADING SKELETON - COMPOSANT SKELETON LOADING ÉLÉGANT
 * - Shimmer animation fluide
 * - Multiple variants (card, list, grid)
 * - Customizable dimensions
 * - Accessible
 * ===================================================================
 */

const LoadingSkeleton = ({
  variant = 'card',
  count = 1,
  width = '100%',
  height = '100px',
  borderRadius = '12px',
  className = '',
  style = {},
  dark = false,
}) => {
  const skeletonClass = `skeleton ${dark ? 'skeleton-dark' : ''} ${className}`;

  /**
   * Variante: Carte
   */
  const CardSkeleton = () => (
    <div className="skeleton-card-wrapper">
      <div
        className={`${skeletonClass} skeleton-card`}
        style={{
          borderRadius,
          ...style,
        }}
      />
    </div>
  );

  /**
   * Variante: Texte
   */
  const TextSkeleton = () => (
    <div className="skeleton-text-wrapper">
      <div
        className={`${skeletonClass} skeleton-text`}
        style={{
          borderRadius,
          width,
          height,
          ...style,
        }}
      />
    </div>
  );

  /**
   * Variante: Avatar
   */
  const AvatarSkeleton = () => (
    <div className="skeleton-avatar-wrapper">
      <div
        className={`${skeletonClass} skeleton-avatar`}
        style={{
          width: width || '48px',
          height: height || '48px',
          borderRadius: '50%',
          ...style,
        }}
      />
    </div>
  );

  /**
   * Variante: Titre
   */
  const TitleSkeleton = () => (
    <div className="skeleton-title-wrapper">
      <div
        className={`${skeletonClass} skeleton-title`}
        style={{
          borderRadius,
          width: width || '70%',
          ...style,
        }}
      />
    </div>
  );

  /**
   * Variante: Liste avec avatar + texte
   */
  const ListItemSkeleton = () => (
    <div className="skeleton-list-item">
      <div className="skeleton-list-item__avatar">
        <div
          className={`${skeletonClass} skeleton-avatar`}
          style={{
            width: '40px',
            height: '40px',
            borderRadius: '50%',
            ...style,
          }}
        />
      </div>
      <div className="skeleton-list-item__content">
        <div
          className={`${skeletonClass} skeleton-title`}
          style={{
            borderRadius,
            width: '60%',
            marginBottom: '8px',
            ...style,
          }}
        />
        <div
          className={`${skeletonClass} skeleton-text`}
          style={{
            borderRadius,
            width: '80%',
            ...style,
          }}
        />
      </div>
    </div>
  );

  /**
   * Variante: Grille d'images
   */
  const GridSkeleton = () => (
    <div className="skeleton-grid">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className={`${skeletonClass} skeleton-card`}
          style={{
            borderRadius,
            aspectRatio: '1/1',
            ...style,
          }}
        />
      ))}
    </div>
  );

  /**
   * Variante: Contenu texte multiple lignes
   */
  const TextBlockSkeleton = () => (
    <div className="skeleton-text-block">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className={`${skeletonClass} skeleton-text`}
          style={{
            borderRadius,
            width: i === count - 1 ? '60%' : '100%',
            marginBottom: i === count - 1 ? 0 : '8px',
            ...style,
          }}
        />
      ))}
    </div>
  );

  /**
   * Variante: Produit (image + titre + prix)
   */
  const ProductSkeleton = () => (
    <div className="skeleton-product">
      <div
        className={`${skeletonClass} skeleton-product__image`}
        style={{
          borderRadius,
          aspectRatio: '1/1',
          marginBottom: '12px',
          ...style,
        }}
      />
      <div
        className={`${skeletonClass} skeleton-title`}
        style={{
          borderRadius,
          width: '80%',
          marginBottom: '8px',
          ...style,
        }}
      />
      <div
        className={`${skeletonClass} skeleton-text`}
        style={{
          borderRadius,
          width: '40%',
          ...style,
        }}
      />
    </div>
  );

  /**
   * Render du composant selon la variante
   */
  const renderSkeleton = () => {
    switch (variant) {
      case 'card':
        return <CardSkeleton />;
      case 'text':
        return <TextSkeleton />;
      case 'avatar':
        return <AvatarSkeleton />;
      case 'title':
        return <TitleSkeleton />;
      case 'list-item':
        return <ListItemSkeleton />;
      case 'grid':
        return <GridSkeleton />;
      case 'text-block':
        return <TextBlockSkeleton />;
      case 'product':
        return <ProductSkeleton />;
      default:
        return <CardSkeleton />;
    }
  };

  return <div className="loading-skeleton">{renderSkeleton()}</div>;
};

/**
 * ===================================================================
 * STYLES INJECTÉS
 * ===================================================================
 */

const insertSkeletonStyles = () => {
  if (document.getElementById('skeleton-styles')) return;

  const styles = document.createElement('style');
  styles.id = 'skeleton-styles';
  styles.textContent = `
    /* ===== LOADING SKELETON COMPONENT ===== */
    .loading-skeleton {
      width: 100%;
    }

    /* ===== WRAPPERS ===== */
    .skeleton-card-wrapper {
      width: 100%;
    }

    .skeleton-text-wrapper {
      width: 100%;
    }

    .skeleton-avatar-wrapper {
      width: fit-content;
    }

    .skeleton-title-wrapper {
      width: 100%;
    }

    /* ===== LIST ITEM SKELETON ===== */
    .skeleton-list-item {
      display: flex;
      gap: 12px;
      align-items: flex-start;
      padding: 12px;
      border-radius: 8px;
      background: transparent;
    }

    .skeleton-list-item__avatar {
      flex-shrink: 0;
    }

    .skeleton-list-item__content {
      flex: 1;
      width: 100%;
    }

    /* ===== GRID SKELETON ===== */
    .skeleton-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
      gap: 16px;
      width: 100%;
    }

    @media (max-width: 768px) {
      .skeleton-grid {
        grid-template-columns: repeat(2, 1fr);
      }
    }

    @media (max-width: 480px) {
      .skeleton-grid {
        grid-template-columns: 1fr;
      }
    }

    /* ===== TEXT BLOCK SKELETON ===== */
    .skeleton-text-block {
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    /* ===== PRODUCT SKELETON ===== */
    .skeleton-product {
      width: 100%;
    }

    .skeleton-product__image {
      display: block;
      width: 100%;
      margin-bottom: 12px;
    }

    /* ===== ANIMATION DELAYS ===== */
    .skeleton-list-item:nth-child(2) {
      animation-delay: 100ms;
    }

    .skeleton-list-item:nth-child(3) {
      animation-delay: 200ms;
    }

    .skeleton-list-item:nth-child(4) {
      animation-delay: 300ms;
    }

    /* ===== LOADING STATES ===== */
    .loading-skeleton.is-loading {
      pointer-events: none;
    }

    .loading-skeleton.is-loaded {
      animation: fadeOut 0.3s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    /* ===== SKELETON BASE STYLES ===== */
    .skeleton {
      background-clip: padding-box;
      will-change: background-position;
    }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
      .skeleton {
        animation-duration: 2.5s;
      }

      .skeleton-card {
        height: auto;
        min-height: 200px;
      }

      .skeleton-text {
        height: 14px;
      }

      .skeleton-title {
        height: 20px;
      }
    }

    /* ===== REDUCED MOTION SUPPORT ===== */
    @media (prefers-reduced-motion: reduce) {
      .skeleton {
        animation: none !important;
        opacity: 0.5;
      }

      .skeleton-list-item {
        animation: none !important;
        opacity: 0.5;
      }
    }
  `;

  document.head.appendChild(styles);
};

// Injecter les styles au chargement
insertSkeletonStyles();

export default LoadingSkeleton;

/**
 * ===================================================================
 * USAGE EXAMPLES
 * ===================================================================
 *
 * // Single card skeleton
 * <LoadingSkeleton variant="card" />
 *
 * // Text skeleton
 * <LoadingSkeleton variant="text" height="20px" width="80%" />
 *
 * // Avatar skeleton
 * <LoadingSkeleton variant="avatar" width="64px" height="64px" />
 *
 * // List items with staggered animation
 * <LoadingSkeleton variant="list-item" count={3} />
 *
 * // Product grid
 * <LoadingSkeleton variant="product" count={6} />
 *
 * // Text block (multiple lines)
 * <LoadingSkeleton variant="text-block" count={4} />
 *
 * // Grid of images
 * <LoadingSkeleton variant="grid" count={9} />
 */
