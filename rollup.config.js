import svelte from 'rollup-plugin-svelte';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import terser from '@rollup/plugin-terser';

const production = !process.env.ROLLUP_WATCH;

export default {
  input: 'src/ce_mlflow_extension/templates/main.js',
  output: {
    sourcemap: true,
    format: 'iife',
    name: 'app',
    file: 'src/ce_mlflow_extension/templates/assets/bundle.js'
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
