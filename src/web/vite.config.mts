import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import {BootstrapVueNextResolver} from 'unplugin-vue-components/resolvers'

// https://vitejs.dev/config/
export default defineConfig(({ command }) => {
  return {
    define: {
      SERVER_HOST: JSON.stringify(command === 'serve' ? 'localhost' : ''),
      SERVER_PORT: JSON.stringify(command === 'serve' ? 9000 : 80)
    },
    plugins: [
      vue(),
      Components({
        resolvers: [BootstrapVueNextResolver()],
      }),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
  };
})
