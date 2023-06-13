import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App);

app.config.errorHandler = (err) => {
  /* handle error */
  console.log(err);
}

app.mount('#app')
