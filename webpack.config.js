const path = require('path');

var json = require('./version.json');
console.log("js:", json);

const webpack = require('webpack');


module.exports = {
    entry: {
        home: './halal/jsx/home.jsx',

        // put other jsx "main" files here
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env': {
                'NODE_ENV': JSON.stringify('production')
            }
        }),
        new webpack.optimize.UglifyJsPlugin()

    ],
    output: {
        path: path.join(__dirname, '/halal/static/js_bundles/'),
        filename: '[name]_bundle.' + json['version'] + '.js',
    },
    module: {
        loaders: [
            {
                // Test for js or jsx files
                test: /\.jsx?$/,
                loader: 'babel-loader',
                query: {
                    // Convert ES6 syntax to ES5 for browser compatibility
                    presets: ['es2015', 'react'],
                },
            },
        ],
    },
    resolve: {
        extensions: ['.js', '.jsx'],
    },
};
