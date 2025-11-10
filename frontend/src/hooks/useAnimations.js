import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * ===================================================================
 * SYSTEM D'ANIMATIONS PREMIUM - REACT HOOKS
 * - Intersection Observer for scroll animations
 * - Performance optimized
 * - Support prefers-reduced-motion
 * ===================================================================
 */

/**
 * Hook: useInView
 * Déclenche une animation quand l'élément entre dans la vue
 *
 * @param {Object} options - Options Intersection Observer
 * @param {number} options.threshold - Seuil de visibilité (0-1)
 * @param {string} options.rootMargin - Marge autour de la racine
 * @returns {Object} { ref, isVisible }
 */
export const useInView = (options = {}) => {
  const {
    threshold = 0.1,
    rootMargin = '0px',
    triggerOnce = true,
  } = options;

  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef(null);
  const hasBeenVisible = useRef(false);

  useEffect(() => {
    // Respecter les préférences de réduction de mouvement
    const prefersReducedMotion = window.matchMedia(
      '(prefers-reduced-motion: reduce)'
    ).matches;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          hasBeenVisible.current = true;

          if (triggerOnce) {
            observer.unobserve(entry.target);
          }
        } else if (!triggerOnce) {
          setIsVisible(false);
        }
      },
      {
        threshold,
        rootMargin,
      }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => {
      if (ref.current) {
        observer.unobserve(ref.current);
      }
    };
  }, [threshold, rootMargin, triggerOnce]);

  return { ref, isVisible };
};

/**
 * Hook: useHover
 * Gère les effets de survol avec animations
 *
 * @param {Object} options - Configuration
 * @returns {Object} { ref, isHovered }
 */
export const useHover = (options = {}) => {
  const { onEnter = null, onLeave = null } = options;

  const [isHovered, setIsHovered] = useState(false);
  const ref = useRef(null);

  const handleMouseEnter = useCallback(() => {
    setIsHovered(true);
    onEnter && onEnter();
  }, [onEnter]);

  const handleMouseLeave = useCallback(() => {
    setIsHovered(false);
    onLeave && onLeave();
  }, [onLeave]);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    element.addEventListener('mouseenter', handleMouseEnter);
    element.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      element.removeEventListener('mouseenter', handleMouseEnter);
      element.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, [handleMouseEnter, handleMouseLeave]);

  return { ref, isHovered };
};

/**
 * Hook: useSpring
 * Animation basée sur la physique (spring physics)
 *
 * @param {number} from - Valeur de départ
 * @param {number} to - Valeur cible
 * @param {Object} options - Configuration spring
 * @returns {number} Valeur animée
 */
export const useSpring = (from, to, options = {}) => {
  const {
    tension = 170,
    friction = 26,
    mass = 1,
    clamp = false,
  } = options;

  const [value, setValue] = useState(from);
  const velocityRef = useRef(0);
  const positionRef = useRef(from);
  const animationRef = useRef(null);

  const update = useCallback(() => {
    const displacement = to - positionRef.current;
    const springForce = (-tension * displacement) / 100;
    const dampingForce = (-friction * velocityRef.current) / 100;
    const acceleration = (springForce + dampingForce) / mass;

    velocityRef.current += acceleration;
    positionRef.current += velocityRef.current;

    // Arrêter l'animation si assez proche
    if (
      Math.abs(displacement) < 0.01 &&
      Math.abs(velocityRef.current) < 0.01
    ) {
      positionRef.current = to;
      velocityRef.current = 0;
      setValue(to);
      return false;
    }

    if (clamp) {
      positionRef.current = Math.max(
        Math.min(positionRef.current, Math.max(from, to)),
        Math.min(from, to)
      );
    }

    setValue(positionRef.current);
    return true;
  }, [to, tension, friction, mass, clamp, from]);

  useEffect(() => {
    const animate = () => {
      if (update()) {
        animationRef.current = requestAnimationFrame(animate);
      }
    };

    animationRef.current = requestAnimationFrame(animate);

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [update]);

  return value;
};

/**
 * Hook: useGesture
 * Détecte les gestes (swipe, pinch, etc.)
 *
 * @param {Object} handlers - Fonctions de callback
 * @returns {Object} { ref }
 */
export const useGesture = (handlers = {}) => {
  const {
    onSwipeLeft = null,
    onSwipeRight = null,
    onSwipeUp = null,
    onSwipeDown = null,
    onPinch = null,
    threshold = 50,
  } = handlers;

  const ref = useRef(null);
  const touchStartRef = useRef({ x: 0, y: 0 });
  const distanceRef = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const handleTouchStart = (e) => {
      if (e.touches.length === 1) {
        touchStartRef.current = {
          x: e.touches[0].clientX,
          y: e.touches[0].clientY,
        };
      } else if (e.touches.length === 2 && onPinch) {
        // Pinch detection
        const touch1 = e.touches[0];
        const touch2 = e.touches[1];
        touchStartRef.current.distance = Math.hypot(
          touch1.clientX - touch2.clientX,
          touch1.clientY - touch2.clientY
        );
      }
    };

    const handleTouchMove = (e) => {
      if (e.touches.length === 1) {
        distanceRef.current = {
          x: e.touches[0].clientX - touchStartRef.current.x,
          y: e.touches[0].clientY - touchStartRef.current.y,
        };
      } else if (e.touches.length === 2 && onPinch) {
        const touch1 = e.touches[0];
        const touch2 = e.touches[1];
        const currentDistance = Math.hypot(
          touch1.clientX - touch2.clientX,
          touch1.clientY - touch2.clientY
        );
        const scale =
          currentDistance / touchStartRef.current.distance;
        onPinch(scale);
      }
    };

    const handleTouchEnd = (e) => {
      const { x, y } = distanceRef.current;
      const absX = Math.abs(x);
      const absY = Math.abs(y);

      if (absX > threshold && absX > absY) {
        if (x > 0 && onSwipeRight) onSwipeRight();
        if (x < 0 && onSwipeLeft) onSwipeLeft();
      } else if (absY > threshold && absY > absX) {
        if (y > 0 && onSwipeDown) onSwipeDown();
        if (y < 0 && onSwipeUp) onSwipeUp();
      }

      touchStartRef.current = { x: 0, y: 0 };
      distanceRef.current = { x: 0, y: 0 };
    };

    element.addEventListener('touchstart', handleTouchStart);
    element.addEventListener('touchmove', handleTouchMove);
    element.addEventListener('touchend', handleTouchEnd);

    return () => {
      element.removeEventListener('touchstart', handleTouchStart);
      element.removeEventListener('touchmove', handleTouchMove);
      element.removeEventListener('touchend', handleTouchEnd);
    };
  }, [onSwipeLeft, onSwipeRight, onSwipeUp, onSwipeDown, onPinch, threshold]);

  return { ref };
};

/**
 * Hook: useAnimationFrame
 * Wrapper pour requestAnimationFrame avec nettoyage
 *
 * @param {Function} callback - Fonction à exécuter chaque frame
 * @param {boolean} shouldAnimate - Condition pour animer
 */
export const useAnimationFrame = (callback, shouldAnimate = true) => {
  const animationRef = useRef(null);

  useEffect(() => {
    if (!shouldAnimate) return;

    const animate = () => {
      callback();
      animationRef.current = requestAnimationFrame(animate);
    };

    animationRef.current = requestAnimationFrame(animate);

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [callback, shouldAnimate]);
};

/**
 * Hook: usePrefersReducedMotion
 * Détecte les préférences de réduction de mouvement
 *
 * @returns {boolean} true si mouvement réduit préféré
 */
export const usePrefersReducedMotion = () => {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);

    const handler = (e) => {
      setPrefersReducedMotion(e.matches);
    };

    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  return prefersReducedMotion;
};

/**
 * Hook: useScrollAnimation
 * Déclenche une animation basée sur la position du scroll
 *
 * @param {Object} options - Configuration
 * @returns {Object} { ref, progress }
 */
export const useScrollAnimation = (options = {}) => {
  const { threshold = 0.1 } = options;

  const [progress, setProgress] = useState(0);
  const ref = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          const rect = entry.boundingClientRect;
          const elementHeight = rect.height;
          const elementTop = rect.top;
          const windowHeight = window.innerHeight;

          const progress = Math.max(
            0,
            Math.min(1, 1 - (elementTop + elementHeight) / windowHeight)
          );

          setProgress(progress);
        }
      },
      { threshold }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    const handleScroll = () => {
      if (ref.current) {
        const rect = ref.current.getBoundingClientRect();
        const elementHeight = rect.height;
        const elementTop = rect.top;
        const windowHeight = window.innerHeight;

        const progress = Math.max(
          0,
          Math.min(1, 1 - (elementTop + elementHeight) / windowHeight)
        );

        setProgress(progress);
      }
    };

    window.addEventListener('scroll', handleScroll);

    return () => {
      if (ref.current) {
        observer.unobserve(ref.current);
      }
      window.removeEventListener('scroll', handleScroll);
    };
  }, [threshold]);

  return { ref, progress };
};

/**
 * Hook: useElementSize
 * Mesure les dimensions d'un élément avec animations
 *
 * @returns {Object} { ref, width, height }
 */
export const useElementSize = () => {
  const [size, setSize] = useState({ width: 0, height: 0 });
  const ref = useRef(null);

  useEffect(() => {
    const resizeObserver = new ResizeObserver((entries) => {
      for (let entry of entries) {
        const { width, height } = entry.contentRect;
        setSize({ width, height });
      }
    });

    if (ref.current) {
      resizeObserver.observe(ref.current);
    }

    return () => {
      if (ref.current) {
        resizeObserver.unobserve(ref.current);
      }
    };
  }, []);

  return { ref, ...size };
};

/**
 * Hook: useTransitionAnimation
 * Gère les transitions entre états
 *
 * @param {any} value - Valeur à animer
 * @param {number} delay - Délai de transition
 * @returns {any} Valeur animée
 */
export const useTransitionAnimation = (value, delay = 300) => {
  const [displayValue, setDisplayValue] = useState(value);
  const timeoutRef = useRef(null);

  useEffect(() => {
    timeoutRef.current = setTimeout(() => {
      setDisplayValue(value);
    }, delay);

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [value, delay]);

  return displayValue;
};

/**
 * Hook: useDebounceAnimation
 * Débounce une animation
 *
 * @param {Function} callback - Fonction à débouncer
 * @param {number} wait - Délai d'attente en ms
 * @returns {Function} Fonction débouncer
 */
export const useDebounceAnimation = (callback, wait = 300) => {
  const timeoutRef = useRef(null);

  const debouncedCallback = useCallback((...args) => {
    if (timeoutRef.current) {
      cancelAnimationFrame(timeoutRef.current);
    }

    timeoutRef.current = setTimeout(() => {
      callback(...args);
    }, wait);
  }, [callback, wait]);

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return debouncedCallback;
};

/**
 * Hook: useMountAnimation
 * Animation au montage du composant
 *
 * @param {string} animationClass - Classe CSS d'animation
 * @param {number} duration - Durée en ms
 * @returns {Object} { ref, isAnimating }
 */
export const useMountAnimation = (
  animationClass = 'animate-fade-in',
  duration = 300
) => {
  const [isAnimating, setIsAnimating] = useState(true);
  const ref = useRef(null);

  useEffect(() => {
    if (ref.current) {
      ref.current.classList.add(animationClass);

      const timer = setTimeout(() => {
        setIsAnimating(false);
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [animationClass, duration]);

  return { ref, isAnimating };
};

export default {
  useInView,
  useHover,
  useSpring,
  useGesture,
  useAnimationFrame,
  usePrefersReducedMotion,
  useScrollAnimation,
  useElementSize,
  useTransitionAnimation,
  useDebounceAnimation,
  useMountAnimation,
};
