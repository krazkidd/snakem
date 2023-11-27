import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css';

import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faRankingStar, faTrophy, faMedal, faNewspaper } from '@fortawesome/free-solid-svg-icons'

const app = createApp(App);

app.config.errorHandler = (err) => {
  /* handle error */
  console.log(err);
}

library.add(faRankingStar, faTrophy, faMedal, faNewspaper)

app.mount('#app')
