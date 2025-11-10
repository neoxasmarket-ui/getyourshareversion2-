/**
 * Lighthouse CI Configuration
 * Target: 98-100 score on all categories
 *
 * Run with: npx @lhci/cli autorun
 */

module.exports = {
  ci: {
    collect: {
      // URLs to test
      url: [
        'http://localhost:3000/',
        'http://localhost:3000/products',
        'http://localhost:3000/dashboard',
        'http://localhost:3000/contact'
      ],

      // Number of runs (median will be used)
      numberOfRuns: 3,

      // Start server if needed
      startServerCommand: 'npm run start',
      startServerReadyPattern: 'webpack compiled',
      startServerReadyTimeout: 30000,

      // Lighthouse settings
      settings: {
        // Use desktop config for faster CI
        preset: 'desktop',

        // Throttling (simulate real conditions)
        throttling: {
          rttMs: 40,
          throughputKbps: 10240,
          cpuSlowdownMultiplier: 1
        },

        // Only collect what we need
        onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],

        // Skip PWA for faster runs (test separately)
        skipAudits: ['uses-http2']
      }
    },

    assert: {
      // Performance assertions
      assertions: {
        'categories:performance': ['error', { minScore: 0.98 }],
        'categories:accessibility': ['error', { minScore: 0.98 }],
        'categories:best-practices': ['error', { minScore: 0.98 }],
        'categories:seo': ['error', { minScore: 0.98 }],

        // Core Web Vitals
        'first-contentful-paint': ['error', { maxNumericValue: 1800 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['error', { maxNumericValue: 300 }],
        'speed-index': ['error', { maxNumericValue: 3400 }],

        // Resource optimization
        'unused-javascript': ['warn', { maxLength: 0 }],
        'unused-css-rules': ['warn', { maxLength: 0 }],
        'modern-image-formats': ['error', { maxLength: 0 }],
        'uses-responsive-images': ['error', { maxLength: 0 }],
        'offscreen-images': ['warn', { maxLength: 0 }],

        // Best practices
        'uses-https': 'error',
        'is-on-https': 'error',
        'uses-http2': 'off', // Skip in local dev
        'uses-passive-event-listeners': 'error',
        'no-document-write': 'error',
        'external-anchors-use-rel-noopener': 'error',

        // Accessibility
        'aria-allowed-attr': 'error',
        'aria-required-attr': 'error',
        'aria-valid-attr': 'error',
        'button-name': 'error',
        'color-contrast': 'error',
        'image-alt': 'error',
        'label': 'error',
        'link-name': 'error',

        // SEO
        'document-title': 'error',
        'meta-description': 'error',
        'http-status-code': 'error',
        'crawlable-anchors': 'error'
      }
    },

    upload: {
      // Store reports locally
      target: 'filesystem',
      outputDir: './lighthouse-reports',
      reportFilenamePattern: '%%PATHNAME%%-%%DATETIME%%.report.%%EXTENSION%%'
    },

    server: {
      // Optional: Run Lighthouse CI server for historical tracking
      // Uncomment when deploying to production
      // target: 'lhci',
      // serverBaseUrl: 'https://lighthouse.getyourshare.ma',
      // token: process.env.LHCI_TOKEN
    }
  }
};

/**
 * Performance Budget Configuration
 * Enforces strict limits on resource sizes
 */
module.exports.budget = [
  {
    resourceSizes: [
      {
        resourceType: 'script',
        budget: 300 // 300 KB max for JS (gzip)
      },
      {
        resourceType: 'stylesheet',
        budget: 50 // 50 KB max for CSS (gzip)
      },
      {
        resourceType: 'image',
        budget: 500 // 500 KB max per image
      },
      {
        resourceType: 'font',
        budget: 100 // 100 KB max for fonts
      },
      {
        resourceType: 'document',
        budget: 25 // 25 KB max for HTML
      },
      {
        resourceType: 'total',
        budget: 1000 // 1 MB max total page weight
      },
      {
        resourceType: 'third-party',
        budget: 200 // 200 KB max for third-party scripts
      }
    ],

    resourceCounts: [
      {
        resourceType: 'script',
        budget: 10 // Max 10 JS files
      },
      {
        resourceType: 'stylesheet',
        budget: 5 // Max 5 CSS files
      },
      {
        resourceType: 'image',
        budget: 20 // Max 20 images per page
      },
      {
        resourceType: 'font',
        budget: 4 // Max 4 font files
      },
      {
        resourceType: 'third-party',
        budget: 5 // Max 5 third-party requests
      }
    ],

    timings: [
      {
        metric: 'first-contentful-paint',
        budget: 1800 // 1.8s FCP
      },
      {
        metric: 'largest-contentful-paint',
        budget: 2500 // 2.5s LCP
      },
      {
        metric: 'cumulative-layout-shift',
        budget: 0.1 // 0.1 CLS
      },
      {
        metric: 'total-blocking-time',
        budget: 300 // 300ms TBT
      },
      {
        metric: 'speed-index',
        budget: 3400 // 3.4s SI
      },
      {
        metric: 'interactive',
        budget: 3800 // 3.8s TTI
      }
    ]
  }
];

/**
 * Recommended package.json scripts:
 *
 * "scripts": {
 *   "lighthouse": "lhci autorun",
 *   "lighthouse:ci": "lhci autorun --config=.lighthouserc.js",
 *   "lighthouse:desktop": "lighthouse http://localhost:3000 --preset=desktop --view",
 *   "lighthouse:mobile": "lighthouse http://localhost:3000 --preset=mobile --view",
 *   "lighthouse:pwa": "lighthouse http://localhost:3000 --only-categories=pwa --view"
 * }
 */
