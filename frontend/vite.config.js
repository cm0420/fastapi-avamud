import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Dev proxy: forward API calls starting with /api to backend on :8080
    // this helps avoid CORS during development. Remove or adjust in production.
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        secure: false,
        // rewrite: path => path.replace(/^\/api/, '') // uncomment if backend doesn't use /api prefix
      }
    }
  }
})
