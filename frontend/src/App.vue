<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router';
import { useAuthStore } from './stores/auth.js';

// Access the global Auth Store
const authStore = useAuthStore();
// Access the router to perform redirects
const router = useRouter();

// Logout Action
const handleLogout = () => {
  // Clear token state and localStorage
  authStore.logout();
  // Redirect back to login page
  router.push('/login');
};
</script>

<template>
  <div id="app-layout">
    <nav class="navbar">
      <RouterLink to="/" class="brand-link">Simple E-Shop</RouterLink>
      <div class="nav-links">
        <RouterLink to="/" class="nav-link">Products</RouterLink>
        <span v-if="authStore.isLoggedIn" class="auth-group">
          <RouterLink to="/cart" class="nav-link">Cart</RouterLink>
          <RouterLink to="/orders" class="nav-link">Orders</RouterLink>
          <button @click="handleLogout" class="btn btn-danger btn-sm">Logout</button>
        </span>
        <span v-else class="auth-group">
          <RouterLink to="/login" class="nav-link">Login</RouterLink>
          <RouterLink to="/register" class="nav-link btn-register">Register</RouterLink>
        </span>
      </div>
    </nav>
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body {
  margin: 0;
  background-color: #f8fafc;
  color: #1e293b;
  font-family: 'Inter', sans-serif;
}

/* Navbar Layout */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff;
  padding: 16px 30px;
  border-bottom: 1px solid #e2e8f0;
}

.brand-link {
  color: #0f172a;
  text-decoration: none;
  font-weight: 700;
  font-size: 18px;
}

.nav-links, .auth-group {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-link {
  color: #64748b;
  text-decoration: none;
  font-weight: 500;
  font-size: 14px;
}

.nav-link:hover, .router-link-active:not(.brand-link) {
  color: #0f172a;
}

.btn-register {
  background-color: #0f172a;
  color: white !important;
  padding: 6px 12px;
  border-radius: 6px;
}

.main-content {
  padding: 30px;
  max-width: 1000px;
  margin: 0 auto;
}

/* Global MVP Utility Styles (to keep View components tiny) */
.card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.btn {
  background-color: #0f172a;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  font-size: 14px;
  display: inline-block;
  text-decoration: none;
  text-align: center;
}

.btn:hover {
  background-color: #334155;
}

.btn-danger {
  background-color: #ef4444;
}

.btn-danger:hover {
  background-color: #dc2626;
}

.btn-sm {
  padding: 4px 10px;
  font-size: 12px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 6px;
  font-size: 14px;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  box-sizing: border-box;
  font-size: 14px;
}

.form-control:focus {
  border-color: #0f172a;
  outline: none;
}
</style>
