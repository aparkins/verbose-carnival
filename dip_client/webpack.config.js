const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const env = process.env.NODE_ENV;
const prod = env === 'production';

// remove hmr plugin and 'react-hot' from your production js loader config
// OPTIMIZE: For improvement to build times, use PrefetchPlugin and DLLPlugin
// OPTIMIZE: http://frontendtest.com/checklist/
// OPTIMIZE: https://www.smashingmagazine.com/2016/12/front-end-performance-checklist-2017-pdf-pages/
// OPTIMIZE: https://www.npmjs.com/package/webpack-visualizer-plugin
// OPTIMIZE: https://www.npmjs.com/package/webpack-bundle-analyzer
// OPTIMIZE: https://github.com/robertknight/webpack-bundle-size-analyzer
let context = path.resolve(__dirname, 'src');

let config = {
  context,

  entry: {
    app: ['./index.js'],
  },

  output: {
    path: path.resolve(__dirname, 'dist'),
    // Not using a hash here, improves performance of incremental builds
    filename: '[name].js',
    publicPath: '/',
  },

  plugins: [
    new HtmlWebpackPlugin({
      template: 'index.html',
      minify: {
        collapseWhitespace: true,
      },
    }),
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify(env),
      },
    })
  ],

  module: {
    rules: [
      {
        test: /\.js/,
        include: [
          context,
          path.resolve('node_modules/preact-compat/src'),
        ],
        loader: 'babel-loader',
        options: {
          cacheDirectory: true,
        }
      }
    ]
  },

  performance: {
    hints: false,
  },

  devtool: 'eval',

  devServer: {
    contentBase: path.resolve(__dirname, 'src'),
    historyApiFallback: true,
  },
};

if (prod) {
  config.devtool = 'nosources-source-map';
  config.output.filename = '[name]-[hash].js';

  config.resolve = {
    alias: {
      react: 'preact-compat',
      'react-dom': 'preact-compat',
    }
  };

  config.performance = {
    hints: 'error',
  };

  config.plugins.push(new webpack.optimize.UglifyJsPlugin({}));
}

module.exports = config;

