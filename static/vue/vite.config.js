import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  root: resolve('./src'),
  base: '/static/',
  server: {
    host: '0.0.0.0',
    port: 5173,
    open: false,
    cors: {
      origin: 'http://localhost:8000',
      credentials: true,
    },
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  build: {
    outDir: resolve('../dist'),
    assetsDir: '',
    manifest: true,
    emptyOutDir: true,
    target: 'es2015',
    rollupOptions: {
      input: {
        main: resolve('./src/main.js'),
      },
      output: {
        chunkFileNames: undefined,
      },
    },
  },
  optimizeDeps: {
    include: ['vue'],
  },
})
