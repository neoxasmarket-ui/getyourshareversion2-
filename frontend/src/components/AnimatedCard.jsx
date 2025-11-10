import React, { useRef, useState, useCallback } from 'react';
import '../styles/animations.css';

/**
 * ===================================================================
 * ANIMATED CARD - COMPOSANT CARD AVEC ANIMATIONS PREMIUM
 * - Hover 3D tilt effect
 * - Glow effect
 * - Smooth shadow transitions
 * - Scale on hover
 * - Content reveal animation
 * ===================================================================
 */

const AnimatedCard = ({
  children,
  variant = 'default',
  hoverable = true,
  glowEffect = true,
  tiltEffect = true,
  onClick = null,
  className = '',
  style = {},
  animationDelay = 0,
}) => {
  const cardRef = useRef(null);
  const [isHovered, setIsHovered] = useState(false);
  const [tilt, setTilt] = useState({ x: 0, y: 0 });

  /**
   * Gère le mouvement de la souris pour le tilt 3D
   */
  const handleMouseMove = useCallback((e) => {
    if (!tiltEffect || !hoverable) return;

    const card = cardRef.current;
    if (!card) return;

    const rect = card.getBoundingClientRect();
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const x = (e.clientX - rect.left - centerX) / centerX;
    const y = (e.clientY - rect.top - centerY) / centerY;

    // Limiter l'angle de tilt (max 15 degrés)
    const tiltX = -y * 15;
    const tiltY = x * 15;

    setTilt({ x: tiltX, y: tiltY });
  }, [hoverable, tiltEffect]);

  /**
   * Réinitialise le tilt au départ de la souris
   */
  const handleMouseLeave = useCallback(() => {
    setTilt({ x: 0, y: 0 });
    setIsHovered(false);
  }, []);

  /**
   * Gère l'entrée de la souris
   */
  const handleMouseEnter = useCallback(() => {
    setIsHovered(true);
  }, []);

  // Styles inline pour le tilt 3D
  const tiltStyle = tiltEffect
    ? {
        transform: `perspective(1000px) rotateX(${tilt.x}deg) rotateY(${tilt.y}deg)`,
        transition: isHovered ? 'transform 0.1s ease-out' : 'transform 0.6s ease-out',
      }
    : {};

  // Classe CSS conditionnelle
  const baseClasses = [
    'animated-card',
    `animated-card--${variant}`,
    hoverable && 'animated-card--hoverable',
    glowEffect && isHovered && 'animated-card--glow',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div
      ref={cardRef}
      className={baseClasses}
      style={{
        ...style,
        ...tiltStyle,
        animationDelay: `${animationDelay}ms`,
      }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      onMouseEnter={handleMouseEnter}
      onClick={onClick}
      role={onClick ? 'button' : 'article'}
      tabIndex={onClick ? 0 : -1}
    >
      <div className="animated-card__content">
        {children}
      </div>
    </div>
  );
};

/**
 * ===================================================================
 * STYLES INJECTÉS
 * ===================================================================
 */

// Créer les styles si pas déjà présents
const insertAnimatedCardStyles = () => {
  if (document.getElementById('animated-card-styles')) return;

  const styles = document.createElement('style');
  styles.id = 'animated-card-styles';
  styles.textContent = `
    /* ===== ANIMATED CARD COMPONENT ===== */
    .animated-card {
      position: relative;
      border-radius: 16px;
      background: white;
      overflow: hidden;
      will-change: transform, box-shadow;
      transition: box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                  transform 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
      .animated-card {
        background: #1a1a1a;
      }
    }

    /* ===== VARIANTS ===== */

    /* Default variant */
    .animated-card--default {
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .animated-card--default:hover {
      box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
    }

    /* Elevated variant */
    .animated-card--elevated {
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }

    .animated-card--elevated:hover {
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.16);
    }

    /* Ghost variant - minimal shadow */
    .animated-card--ghost {
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
      border: 1px solid rgba(0, 0, 0, 0.08);
    }

    @media (prefers-color-scheme: dark) {
      .animated-card--ghost {
        border: 1px solid rgba(255, 255, 255, 0.1);
      }
    }

    .animated-card--ghost:hover {
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    /* Interactive variant */
    .animated-card--interactive {
      cursor: pointer;
      border: 2px solid transparent;
      transition: border-color 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .animated-card--interactive:hover {
      border-color: rgba(59, 130, 246, 0.3);
    }

    .animated-card--interactive:focus-visible {
      outline: 2px solid #3b82f6;
      outline-offset: 2px;
    }

    /* ===== HOVERABLE STATE ===== */
    .animated-card--hoverable:hover {
      transform: translateY(-8px);
    }

    /* ===== GLOW EFFECT ===== */
    .animated-card--glow {
      box-shadow:
        0 12px 24px rgba(0, 0, 0, 0.12),
        0 0 20px rgba(59, 130, 246, 0.3);
    }

    /* ===== CONTENT ===== */
    .animated-card__content {
      position: relative;
      z-index: 1;
      padding: 24px;
      width: 100%;
      height: 100%;
      animation: fadeIn 0.6s cubic-bezier(0.0, 0, 0.2, 1) forwards;
    }

    /* ===== PSEUDO-ELEMENT GRADENT OVERLAY ===== */
    .animated-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.1) 0%,
        rgba(255, 255, 255, 0) 50%
      );
      opacity: 0;
      transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      pointer-events: none;
      border-radius: 16px;
      z-index: 2;
    }

    .animated-card:hover::before {
      opacity: 1;
    }

    /* ===== ANIMATION ENTRY ===== */
    .animated-card {
      animation: slideInUp 0.6s cubic-bezier(0.0, 0, 0.2, 1) forwards;
    }

    /* Stagger for multiple cards */
    @for $i from 1 through 8 {
      .animated-card:nth-child(#{$i}) {
        animation-delay: #{$i * 100}ms;
      }
    }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
      .animated-card {
        border-radius: 12px;
      }

      .animated-card__content {
        padding: 16px;
      }

      .animated-card:hover {
        transform: translateY(-4px);
      }
    }

    /* ===== REDUCED MOTION SUPPORT ===== */
    @media (prefers-reduced-motion: reduce) {
      .animated-card {
        animation: none;
        opacity: 1;
        transform: none;
        transition: none;
      }

      .animated-card:hover {
        transform: none;
        transition: box-shadow 0.2s ease-in-out;
      }

      .animated-card__content {
        animation: none;
        opacity: 1;
      }
    }
  `;

  document.head.appendChild(styles);
};

// Injecter les styles au chargement du module
insertAnimatedCardStyles();

export default AnimatedCard;

/**
 * ===================================================================
 * USAGE EXAMPLES
 * ===================================================================
 *
 * // Simple card
 * <AnimatedCard>
 *   <h3>Title</h3>
 *   <p>Content</p>
 * </AnimatedCard>
 *
 * // Elevated variant with glow
 * <AnimatedCard variant="elevated" glowEffect={true}>
 *   <img src="..." alt="..." />
 *   <h3>Product</h3>
 * </AnimatedCard>
 *
 * // Interactive card with click handler
 * <AnimatedCard
 *   variant="interactive"
 *   onClick={() => navigate('/details')}
 * >
 *   <span>Click me</span>
 * </AnimatedCard>
 *
 * // Multiple cards with staggered animation
 * {items.map((item, index) => (
 *   <AnimatedCard
 *     key={item.id}
 *     animationDelay={index * 100}
 *   >
 *     {item.content}
 *   </AnimatedCard>
 * ))}
 */
