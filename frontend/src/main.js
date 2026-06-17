import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router/index.js';

// 1. Create a Vue App instance
const app = createApp(App);

// 2. Register the Pinia global state store
app.use(createPinia());

// 3. Register the router mapping
app.use(router);

// 4. Mount/Bootstrap the application to index.html (inside <div id="app">)
app.mount('#app');
