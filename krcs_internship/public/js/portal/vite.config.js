import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig(({ command }) => ({
  plugins: [vue()],
  root: '.',

  // Use / for dev, production path for build
  base: command === 'build'
    ? '/assets/krcs_internship/js/portal/dist/'
    : '/',

  build: {
    outDir: resolve(__dirname, 'dist'),
    emptyOutDir: true,
    cssCodeSplit: false,
    rollupOptions: {
      input: resolve(__dirname, 'index.html'),
      external: (id) => id.startsWith('/assets/'),
      output: {
        entryFileNames: 'portal.js',
        chunkFileNames: 'portal-[name].js',
        assetFileNames: (info) => {
          if (info.name?.endsWith('.css')) return 'portal.css'
          return '[name][extname]'
        }
      }
    }
  },

  server: {
    hmr: {
      overlay: false
    },
    proxy: {
      '/api': {
        target: 'http://intern.localhost:8006',
        changeOrigin: true,
        secure: false
      },
      '/assets': {
        target: 'http://intern.localhost:8006',
        changeOrigin: true,
        secure: false
      },
      '/files': {
        target: 'http://intern.localhost:8006',
        changeOrigin: true,
        secure: false
      }
    }
  },

  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  }
}))