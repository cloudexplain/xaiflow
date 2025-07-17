// Development Rollup configuration
import svelte from 'rollup-plugin-svelte';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import typescript from '@rollup/plugin-typescript';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);

export default {
  input: 'dev/dev-entry.js',
  output: {
    file: 'dev/bundle.js',
    format: 'iife',
    name: 'DevBundle',
    sourcemap: true // Enable source maps for debugging
  },
  plugins: [
    svelte({
      compilerOptions: {
        // Enable dev mode for better debugging
        dev: true,
        // Use compatibility mode for Svelte 5
        compatibility: {
          componentApi: 5
        }
      },
      emitCss: false // Inline CSS for simplicity
    }),
    resolve({
      browser: true,
      dedupe: ['svelte'],
      exportConditions: ['svelte']
    }),
    commonjs(),
    typescript({
      sourceMap: true,
      inlineSources: true
    })
  ],
  watch: {
    clearScreen: false,
    include: [
      'dev/**',
      'src/xaiflow/templates/**'
    ]
  }
};
