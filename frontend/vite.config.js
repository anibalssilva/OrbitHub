import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      input: {
        main: './index.html',
        portal: './portal.html'
      }
    }
  },
  server: {
    proxy: {
      '/api': {
        // target: process.env.VITE_API_URL || 'http://localhost:8000',
        target: process.env.VITE_API_URL || 'https://orbithub-backend.onrender.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})

