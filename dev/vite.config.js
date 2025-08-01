import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig({
  plugins: [svelte()],
  server: {
    port: 3000,
    open: true
  },
  resolve: {
    alias: {
      '@components': '../src/xaiflow/templates/components'
    }
  }
})
