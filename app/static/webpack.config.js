const webpack = require('webpack');
var path = require('path');

const config = {
    entry:  path.normalize(__dirname + '/js/index.jsx'),
    output: {
        path: path.normalize(__dirname + '/dist'),
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },
    module: {
        rules: [
          {
            test: /\.jsx?/,
            exclude: /node_modules/,
            use: 'babel-loader'
          }
        ]
      }
};

module.exports = config;