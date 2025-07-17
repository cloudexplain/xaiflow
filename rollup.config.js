import svelte from 'rollup-plugin-svelte';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import terser from '@rollup/plugin-terser';
import typescript from '@rollup/plugin-typescript';

const production = !process.env.ROLLUP_WATCH;

export default {
  input: 'src/xaiflow/templates/main.js',
  output: {
    sourcemap: true,
    format: 'iife',
    name: 'app',
    file: 'src/xaiflow/templates/assets/bundle.js'
  },
  plugins: [
    svelte({
      compilerOptions: {
        dev: !production,
        // Enable legacy mode for Svelte 5 to maintain Svelte 4 compatibility
        compatibility: {
          componentApi: 4
        }
      },
      emitCss: false
    }),
    typescript({
      sourceMap: !production,
      inlineSources: !production
    }),
    resolve({
      browser: true,
      dedupe: ['svelte']
    }),
    commonjs(),
    production && terser()
  ],
  watch: {
    clearScreen: false
  }
};
