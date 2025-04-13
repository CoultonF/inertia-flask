import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'url'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    emptyOutDir: true,
    copyPublicDir: false,
    rollupOptions: {
      input: 'src/main.js',
      output: {
        entryFileNames: 'client/[name].js',
        chunkFileNames: 'client/[name].js',
        assetFileNames: 'client/[name].[ext]',
      }
    },
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  publicDir: path.resolve(__dirname, '../public'),
  base: '/public/'
})
