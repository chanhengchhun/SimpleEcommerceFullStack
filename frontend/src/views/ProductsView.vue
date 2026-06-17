<script setup>
import { ref, onMounted } from 'vue';
import { useCartStore } from '../stores/cart.js';
import { useAuthStore } from '../stores/auth.js';
import api from '../api/axios.js';

// STATE: Reactive products array populated from Django backend API
const products = ref([]);
const cartStore = useCartStore();
const authStore = useAuthStore();

// LIFECYCLE: Triggers once as soon as the component is mounted on screen
onMounted(() => {
  api.get('products/')
    .then(res => products.value = res.data)
    .catch(err => console.error("Error loading products:", err));
});
</script>

<template>
  <div>
    <h1>Products</h1>
    
    <!-- Empty state check -->
    <div v-if="products.length === 0">No products available.</div>
    
    <!-- Products list layout -->
    <div v-else class="products-list">
      <div v-for="product in products" :key="product.id" class="card">
        <h3>{{ product.name }}</h3>
        <p>{{ product.description }}</p>
        <p><strong>${{ product.price }}</strong></p>
        
        <!-- Conditional button rendering based on authentication state -->
        <button 
          v-if="authStore.isLoggedIn" 
          @click="cartStore.addToCart(product.id, 1)"
          class="btn"
        >
          Add to Cart
        </button>
        <p v-else style="color: #64748b; font-size: 14px;">
          <em>Login to add to cart</em>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.products-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
</style>