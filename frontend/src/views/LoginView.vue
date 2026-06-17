<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth.js';
import { useRouter } from 'vue-router';

// STATE: Reactive input values
const username = ref('');
const password = ref('');
const errorMsg = ref('');

const authStore = useAuthStore();
const router = useRouter();

// ACTION: handles form submission and authenticates credentials
const handleLogin = async () => {
  try {
    errorMsg.value = '';
    await authStore.login(username.value, password.value);
    router.push('/');
  } catch (error) {
    if (error.response && error.response.data) {
      errorMsg.value = error.response.data.detail || 'Invalid username or password.';
    } else {
      errorMsg.value = 'Failed to login. Connection error or server issue.';
    }
  }
};
</script>

<template>
  <div style="max-width: 400px; margin: 50px auto;">
    <div class="card">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Username</label>
          <input v-model="username" class="form-control" placeholder="Enter username" required />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input v-model="password" type="password" class="form-control" placeholder="Enter password" required />
        </div>
        <button type="submit" class="btn" style="width: 100%;">Login</button>
      </form>
      <p v-if="errorMsg" style="color: #ef4444; margin-top: 15px; text-align: center;">{{ errorMsg }}</p>
      <p style="margin-top: 20px; text-align: center; font-size: 14px;">
        Don't have an account? <RouterLink to="/register">Register here</RouterLink>
      </p>
    </div>
  </div>
</template>