import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import '../styles/animations.css';

/**
 * ===================================================================
 * PAGE TRANSITION - COMPOSANT TRANSITIONS ENTRE PAGES
 * - Fade, slide, zoom effects
 * - Route change animations
 * - Smooth et rapide
 * - Support transitions de sortie
 * ===================================================================
 */

const PageTransition = ({
  children,
  effect = 'fade',
  duration = 300,
  className = '',
}) => {
  const location = useLocation();
  const [displayLocation, setDisplayLocation] = useState(location);
  const [transitionStage, setTransitionStage] = useState('enter');

  useEffect(() => {
    // Si la location a changé
    if (location !== displayLocation) {
      setTransitionStage('exit');

      const timer = setTimeout(() => {
        setDisplayLocation(location);
        setTransitionStage('enter');
      }, duration / 2);

      return () => clearTimeout(timer);
    }
  }, [location, displayLocation, duration]);

  // Classes d'animation
  const getAnimationClass = () => {
    const baseClass = `page-transition page-transition--${effect}`;

    if (transitionStage === 'enter') {
      return `${baseClass} page-transition--enter`;
    } else {
      return `${baseClass} page-transition--exit`;
    }
  };

  return (
    <div className={`${getAnimationClass()} ${className}`}>
      {children}
    </div>
  );
};

/**
 * ===================================================================
 * LAYOUT TRANSITION - WRAPPER POUR ROUTES
 * ===================================================================
 */

export const LayoutTransition = ({ children, effect = 'fade' }) => {
  return <PageTransition effect={effect}>{children}</PageTransition>;
};

/**
 * ===================================================================
 * STYLES INJECTÉS
 * ===================================================================
 */

const insertPageTransitionStyles = () => {
  if (document.getElementById('page-transition-styles')) return;

  const styles = document.createElement('style');
  styles.id = 'page-transition-styles';
  styles.textContent = `
    /* ===== PAGE TRANSITION COMPONENT ===== */
    .page-transition {
      width: 100%;
      min-height: 100vh;
      animation-duration: 300ms;
      animation-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
      will-change: opacity, transform;
    }

    /* ===== FADE EFFECT ===== */
    .page-transition--fade.page-transition--enter {
      animation: fadeIn 300ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    .page-transition--fade.page-transition--exit {
      animation: fadeOut 150ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    /* ===== SLIDE UP EFFECT ===== */
    .page-transition--slide-up.page-transition--enter {
      animation: slideInUp 300ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    .page-transition--slide-up.page-transition--exit {
      animation: slideOutDown 150ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    /* ===== SLIDE DOWN EFFECT ===== */
    .page-transition--slide-down.page-transition--enter {
      animation: slideInDown 300ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    .page-transition--slide-down.page-transition--exit {
      animation: slideOutUp 150ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    /* ===== SLIDE LEFT EFFECT ===== */
    .page-transition--slide-left.page-transition--enter {
      animation: slideInRight 300ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    .page-transition--slide-left.page-transition--exit {
      animation: slideOutLeft 150ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    /* ===== SLIDE RIGHT EFFECT ===== */
    .page-transition--slide-right.page-transition--enter {
      animation: slideInLeft 300ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    .page-transition--slide-right.page-transition--exit {
      animation: slideOutRight 150ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    /* ===== ZOOM IN EFFECT ===== */
    .page-transition--zoom.page-transition--enter {
      animation: zoomIn 300ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    .page-transition--zoom.page-transition--exit {
      animation: zoomOut 150ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    /* ===== BOUNCE EFFECT ===== */
    .page-transition--bounce.page-transition--enter {
      animation: bounceIn 400ms cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
    }

    .page-transition--bounce.page-transition--exit {
      animation: fadeOut 150ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    /* ===== SCALE UP EFFECT ===== */
    .page-transition--scale-up.page-transition--enter {
      animation: scaleUp 300ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    .page-transition--scale-up.page-transition--exit {
      animation: zoomOut 150ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    /* ===== FLIP EFFECT ===== */
    .page-transition--flip.page-transition--enter {
      animation: flipInY 400ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    .page-transition--flip.page-transition--exit {
      animation: fadeOut 150ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    /* ===== REDUCED MOTION SUPPORT ===== */
    @media (prefers-reduced-motion: reduce) {
      .page-transition {
        animation: none !important;
        opacity: 1 !important;
        transform: none !important;
      }
    }

    /* ===== FADE OUT ANIMATION ===== */
    @keyframes fadeOut {
      from {
        opacity: 1;
      }
      to {
        opacity: 0;
      }
    }

    @keyframes zoomOut {
      from {
        opacity: 1;
        transform: scale3d(1, 1, 1);
      }
      50% {
        opacity: 0;
      }
      to {
        opacity: 0;
        transform: scale3d(0.3, 0.3, 0.3);
      }
    }
  `;

  document.head.appendChild(styles);
};

// Injecter les styles
insertPageTransitionStyles();

/**
 * ===================================================================
 * ROUTE TRANSITION HOOK
 * Utilisé avec React Router
 * ===================================================================
 */

export const usePageTransition = (effect = 'fade', duration = 300) => {
  const [isTransitioning, setIsTransitioning] = React.useState(false);
  const location = useLocation();

  React.useEffect(() => {
    setIsTransitioning(true);
    const timer = setTimeout(() => setIsTransitioning(false), duration);
    return () => clearTimeout(timer);
  }, [location, duration]);

  return { isTransitioning, effect };
};

export default PageTransition;

/**
 * ===================================================================
 * USAGE EXAMPLES
 * ===================================================================
 *
 * // Dans App.js avec React Router
 * import { PageTransition } from './components/PageTransition';
 *
 * function App() {
 *   return (
 *     <PageTransition effect="slide-up">
 *       <Routes>
 *         <Route path="/" element={<Home />} />
 *         <Route path="/about" element={<About />} />
 *         ...
 *       </Routes>
 *     </PageTransition>
 *   );
 * }
 *
 * // Utiliser avec différents effets:
 * - 'fade': Fade in/out (par défaut)
 * - 'slide-up': Slide up on enter, down on exit
 * - 'slide-down': Slide down on enter, up on exit
 * - 'slide-left': Slide right on enter, left on exit
 * - 'slide-right': Slide left on enter, right on exit
 * - 'zoom': Zoom in/out effect
 * - 'bounce': Bounce effect
 * - 'scale-up': Scale animation
 * - 'flip': Flip Y effect
 */
