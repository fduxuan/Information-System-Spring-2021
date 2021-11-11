/*
 * Created on 2021/4/4 5:36 下午
 *
 * @Author: fduxuan
 *
 * Desc:
 */
module.exports = {
    devServer: {
        proxy: {
            '^/api': {
                target: 'http://106.14.244.24:8080/',
                // target: 'http://localhost:8000/',
                changeOrigin: true,
                ws: true,
                pathRewrite: {
                    '^/api': '/api'
                }
            },
        }
    },
    css: {
        loaderOptions: {
            less: {
                lessOptions: {
                    // If you are using less-loader@5 please spread the lessOptions to options directly
                    modifyVars: {
                        // 'primary-color': '#9cd1d0',
                        'primary-color': '#4785ac',
                        'link-color': '#ff2e63',
                        'border-radius-base': '2px',
                    },
                    javascriptEnabled: true,
                },
            },
        },
    },
};
