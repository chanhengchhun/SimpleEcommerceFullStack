<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth.js';
import { useRouter } from 'vue-router';

// STATE: Reactive input values
const username = ref('');
const email = ref('');
const password = ref('');
const errorMsg = ref('');

const authStore = useAuthStore();
const router = useRouter();

// ACTION: sends registration details to Django and redirects on success
const handleRegister = async () => {
  try {
    errorMsg.value = '';
    await authStore.register(username.value, email.value, password.value);
    alert('Account created! Please log in.');
    router.push('/login');
  } catch (error) {
    // Check if the backend returned validation error fields
    if (error.response && error.response.data) {
      const data = error.response.data;
      // Map all field errors into a single readable string
      errorMsg.value = Object.keys(data)
        .map(key => `${key}: ${Array.isArray(data[key]) ? data[key].join(', ') : data[key]}`)
        .join(' | ');
    } else {
      errorMsg.value = 'Failed to register. Connection error or server issue.';
    }
  }
};
</script>


<template>
  <div style="max-width: 400px; margin: 50px auto;">
    <div class="card">
      <h2>Register</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Username</label>
          <input v-model="username" class="form-control" placeholder="Choose username" required />
        </div>
        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" class="form-control" placeholder="Enter email" />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input v-model="password" type="password" class="form-control" placeholder="Choose password" required />
        </div>
        <button type="submit" class="btn" style="width: 100%;">Create Account</button>
      </form>
      <p v-if="errorMsg" style="color: #ef4444; margin-top: 15px; text-align: center;">{{ errorMsg }}</p>
      <p style="margin-top: 20px; text-align: center; font-size: 14px;">
        Already have an account? <RouterLink to="/login">Login here</RouterLink>
      </p>
    </div>
  </div>
</template>