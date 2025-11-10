/**
 * Webpack Optimization Configuration
 * Target: Lighthouse 98-100/100
 *
 * Use with: webpack --config webpack.config.optimization.js
 * Or merge into existing webpack.config.js
 */
const TerserPlugin = require('terser-webpack-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const CompressionPlugin = require('compression-webpack-plugin');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const { PurgeCSSPlugin } = require('purgecss-webpack-plugin');
const glob = require('glob');
const path = require('path');

// Environment
const isProduction = process.env.NODE_ENV === 'production';
const isAnalyze = process.env.ANALYZE === 'true';

module.exports = {
  mode: isProduction ? 'production' : 'development',

  // Source maps (faster alternatives for production)
  devtool: isProduction ? 'source-map' : 'eval-source-map',

  // Output configuration
  output: {
    path: path.resolve(__dirname, 'build'),
    filename: isProduction
      ? 'static/js/[name].[contenthash:8].js'
      : 'static/js/[name].bundle.js',
    chunkFilename: isProduction
      ? 'static/js/[name].[contenthash:8].chunk.js'
      : 'static/js/[name].chunk.js',
    assetModuleFilename: 'static/media/[name].[hash][ext]',
    clean: true, // Clean build folder before each build
    publicPath: '/'
  },

  // Performance hints
  performance: {
    hints: isProduction ? 'warning' : false,
    maxEntrypointSize: 300000,  // 300 KB
    maxAssetSize: 250000        // 250 KB
  },

  // Optimization strategies
  optimization: {
    minimize: isProduction,

    minimizer: [
      // JavaScript minification
      new TerserPlugin({
        terserOptions: {
          parse: {
            ecma: 2020
          },
          compress: {
            ecma: 2020,
            warnings: false,
            comparisons: false,
            inline: 2,
            drop_console: isProduction, // Remove console.log in production
            drop_debugger: isProduction,
            pure_funcs: isProduction ? ['console.log', 'console.info', 'console.debug'] : []
          },
          mangle: {
            safari10: true
          },
          output: {
            ecma: 2020,
            comments: false,
            ascii_only: true
          }
        },
        parallel: true,
        extractComments: false
      }),

      // CSS minification
      new CssMinimizerPlugin({
        minimizerOptions: {
          preset: [
            'default',
            {
              discardComments: { removeAll: true },
              normalizeUnicode: false
            }
          ]
        }
      })
    ],

    // Split chunks strategy
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        // Vendor chunk (node_modules)
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10,
          reuseExistingChunk: true,
          enforce: true
        },

        // React + React DOM (heavy, rarely changes)
        react: {
          test: /[\\/]node_modules[\\/](react|react-dom|scheduler)[\\/]/,
          name: 'react-vendors',
          priority: 20,
          reuseExistingChunk: true
        },

        // UI libraries
        ui: {
          test: /[\\/]node_modules[\\/](@headlessui|@heroicons|framer-motion)[\\/]/,
          name: 'ui-vendors',
          priority: 15,
          reuseExistingChunk: true
        },

        // Utilities (lodash, date-fns, etc.)
        utils: {
          test: /[\\/]node_modules[\\/](lodash|date-fns|axios|classnames)[\\/]/,
          name: 'utils-vendors',
          priority: 15,
          reuseExistingChunk: true
        },

        // Common code shared between pages
        common: {
          minChunks: 2,
          priority: 5,
          reuseExistingChunk: true,
          name: 'common'
        }
      }
    },

    // Runtime chunk for better caching
    runtimeChunk: {
      name: entrypoint => `runtime-${entrypoint.name}`
    },

    // Module IDs (deterministic for better caching)
    moduleIds: 'deterministic',
    chunkIds: 'deterministic',

    // Tree shaking
    usedExports: true,
    sideEffects: true
  },

  // Plugins
  plugins: [
    // Gzip compression
    isProduction && new CompressionPlugin({
      filename: '[path][base].gz',
      algorithm: 'gzip',
      test: /\.(js|css|html|svg)$/,
      threshold: 10240, // Only compress files > 10 KB
      minRatio: 0.8
    }),

    // Brotli compression (better than gzip)
    isProduction && new CompressionPlugin({
      filename: '[path][base].br',
      algorithm: 'brotliCompress',
      test: /\.(js|css|html|svg)$/,
      compressionOptions: {
        level: 11
      },
      threshold: 10240,
      minRatio: 0.8
    }),

    // Remove unused CSS
    isProduction && new PurgeCSSPlugin({
      paths: glob.sync(`${path.join(__dirname, 'src')}/**/*`, { nodir: true }),
      safelist: {
        standard: [/^modal/, /^toast/, /^dropdown/, /^animate-/],
        deep: [/^data-/, /^aria-/],
        greedy: [/^react-/]
      }
    }),

    // Bundle analyzer (run with ANALYZE=true)
    isAnalyze && new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      reportFilename: 'bundle-report.html',
      openAnalyzer: true,
      generateStatsFile: true,
      statsFilename: 'bundle-stats.json'
    })
  ].filter(Boolean),

  // Module resolution
  resolve: {
    extensions: ['.js', '.jsx', '.json'],
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@components': path.resolve(__dirname, 'src/components'),
      '@pages': path.resolve(__dirname, 'src/pages'),
      '@hooks': path.resolve(__dirname, 'src/hooks'),
      '@utils': path.resolve(__dirname, 'src/utils'),
      '@services': path.resolve(__dirname, 'src/services'),
      '@styles': path.resolve(__dirname, 'src/styles')
    }
  },

  // Module rules
  module: {
    rules: [
      // JavaScript/JSX
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              ['@babel/preset-env', {
                useBuiltIns: 'usage',
                corejs: 3,
                modules: false // Enable tree shaking
              }],
              ['@babel/preset-react', {
                runtime: 'automatic' // Use new JSX transform
              }]
            ],
            plugins: [
              '@babel/plugin-syntax-dynamic-import',
              isProduction && 'transform-react-remove-prop-types'
            ].filter(Boolean),
            cacheDirectory: true,
            cacheCompression: false
          }
        }
      },

      // CSS/SCSS
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
              modules: {
                auto: true,
                localIdentName: isProduction
                  ? '[hash:base64:8]'
                  : '[path][name]__[local]'
              }
            }
          },
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: [
                  'autoprefixer',
                  isProduction && 'cssnano'
                ].filter(Boolean)
              }
            }
          }
        ]
      },

      // Images
      {
        test: /\.(png|jpg|jpeg|gif|webp|avif)$/i,
        type: 'asset',
        parser: {
          dataUrlCondition: {
            maxSize: 8 * 1024 // Inline images < 8 KB
          }
        },
        generator: {
          filename: 'static/images/[name].[hash:8][ext]'
        }
      },

      // SVG (inline as React components)
      {
        test: /\.svg$/,
        use: ['@svgr/webpack', 'url-loader']
      },

      // Fonts
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/i,
        type: 'asset/resource',
        generator: {
          filename: 'static/fonts/[name].[hash:8][ext]'
        }
      }
    ]
  },

  // Development server
  devServer: {
    hot: true,
    compress: true,
    historyApiFallback: true,
    port: 3000,
    open: false,
    client: {
      overlay: {
        errors: true,
        warnings: false
      }
    }
  }
};

/**
 * Package.json scripts to add:
 *
 * "scripts": {
 *   "build": "webpack --config webpack.config.optimization.js --mode production",
 *   "build:analyze": "ANALYZE=true webpack --config webpack.config.optimization.js --mode production",
 *   "start": "webpack serve --config webpack.config.optimization.js --mode development"
 * }
 *
 * Required packages:
 * npm install --save-dev \
 *   terser-webpack-plugin \
 *   css-minimizer-webpack-plugin \
 *   compression-webpack-plugin \
 *   webpack-bundle-analyzer \
 *   purgecss-webpack-plugin \
 *   @babel/plugin-syntax-dynamic-import \
 *   transform-react-remove-prop-types
 */
