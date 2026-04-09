import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig(({ command }) => ({
	plugins: [vue()],
	root: '.',

	base: command === 'build'
		? '/assets/krcs_internship/js/portal/dist/'
		: '/',

	build: {
		outDir: resolve(__dirname, 'dist'),
		emptyOutDir: true,
		cssCodeSplit: false,
		// Target older browsers to avoid module syntax in output
		target: 'es2015',
		rollupOptions: {
			input: resolve(__dirname, 'index.html'),
			output: {
				format: 'iife',
				name: 'KRCSPortal',
				// This is the critical flag — without it, lazy router imports
				// generate separate ES module chunks that contain "export" statements,
				// which crash when loaded as a plain <script> tag in Frappe
				inlineDynamicImports: true,
				entryFileNames: 'portal.js',
				assetFileNames: (info) => {
					if (info.name?.endsWith('.css')) return 'portal.css'
					return '[name][extname]'
				}
			}
		}
	},

	server: {
		hmr: { overlay: false },
		proxy: {
			'/api': {
				// Use 127.0.0.1 NOT intern.localhost — the custom domain does not
				// resolve from Node.js DNS resolver outside the bench nginx context
				target: 'http://127.0.0.1:8006',
				changeOrigin: true,
				secure: false,
				configure: (proxy) => {
					proxy.on('error', (err) => {
						console.log('[vite proxy error]', err.message)
					})
					proxy.on('proxyReq', (proxyReq) => {
						// Set Host header so Frappe's site routing works
						proxyReq.setHeader('Host', 'intern.localhost')
					})
					proxy.on('proxyRes', (proxyRes, req) => {
						if (proxyRes.statusCode >= 400) {
							console.log('[vite proxy]', proxyRes.statusCode, req.url)
						}
					})
				}
			},
			'/assets': {
				target: 'http://127.0.0.1:8006',
				changeOrigin: true,
				secure: false,
				configure: (proxy) => {
					proxy.on('proxyReq', (proxyReq) => {
						proxyReq.setHeader('Host', 'intern.localhost')
					})
				}
			},
			'/files': {
				target: 'http://127.0.0.1:8006',
				changeOrigin: true,
				secure: false,
				configure: (proxy) => {
					proxy.on('proxyReq', (proxyReq) => {
						proxyReq.setHeader('Host', 'intern.localhost')
					})
				}
			}
		}
	},

	resolve: {
		alias: { '@': resolve(__dirname, 'src') }
	}
}))