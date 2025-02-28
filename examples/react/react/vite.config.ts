import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    emptyOutDir: true,
    copyPublicDir: false,
    rollupOptions: {
      input: '/src/main.tsx',
      output: {
        entryFileNames: 'client/[name].js',
        chunkFileNames: 'client/[name].js',
        assetFileNames: 'client/[name].[ext]',
      }
    },
  }
})
