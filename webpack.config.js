var debug = process.env.NODE_ENV !== "production";
var webpack = require('webpack');
var path = require('path');
var ExtractTextPlugin = require("extract-text-webpack-plugin");
var autoprefixer = require('autoprefixer');

module.exports = {
  context: path.join(__dirname, "src"),
  devtool: debug ? "inline-sourcemap" : null,
  entry: "./js/index.js",
  module: {
    loaders: [
      {
        test: /\.js?$/,
        exclude: /(node_modules|bower_components)/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'stage-0'],
          plugins: ['transform-class-properties', 'transform-decorators-legacy']
        }
      },
      { test: /\.scss$/, loader: ExtractTextPlugin.extract("style-loader", ["css-loader", "postcss-loader", "sass-loader"]) },
      { test: /\.json$/, loader: 'json' }
    ]
  },
  postcss: [ autoprefixer({ browsers: ['last 2 versions'] }) ],
  output: {
    path: __dirname + "/assets/",
    filename: "build.min.js"
  },
  externals: {
      "jquery": "jQuery"
  },
  plugins: [
        new webpack.optimize.DedupePlugin(),
        new webpack.optimize.OccurenceOrderPlugin(),
        new webpack.optimize.UglifyJsPlugin({
          debug: false,
          minimize: true,
          sourceMap: false,
          output: {
            comments: false
          },
          compressor: {
            warnings: false
          }
        }),
        new ExtractTextPlugin("style.css"),
        new webpack.ProvidePlugin({
          $: "jquery",
          jQuery: "jquery",
          "window.jQuery": "jquery"
        })
      ]
};