<script setup>
import { onMounted, computed } from 'vue';
import { useCartStore } from '../stores/cart.js';
import { useRouter } from 'vue-router';

const cartStore = useCartStore();
const router = useRouter();

// LIFECYCLE: Fetch cart data from the backend as soon as the page loads
// Look up: 'Vue onMounted lifecycle hook'
onMounted(() => {
  cartStore.fetchCart();
});

// COMPUTED: Reactive values derived from state. They auto-recalculate whenever the cart updates.
// Look up: 'Vue Computed Properties'
const totalItems = computed(() => {
  return cartStore.cart.items.reduce((sum, item) => sum + item.quantity, 0);
});

const totalPrice = computed(() => {
  return cartStore.cart.items.reduce((sum, item) => sum + (parseFloat(item.product_price) * item.quantity), 0).toFixed(2);
});

// ACTION: Initiates checkout, resets the cart local state, and routes to order history
const placeOrder = async () => {
  try {
    await cartStore.checkout();
    router.push('/orders');
  } catch (err) {
    alert('Failed to place order.');
  }
};
</script>

<template>
  <div>
    <h1>Shopping Cart</h1>
    
    <!-- Empty State -->
    <div v-if="!cartStore.cart.items || cartStore.cart.items.length === 0" style="text-align: center; margin: 40px;">
      <p>Your cart is empty.</p>
      <RouterLink to="/" class="btn">Shop Products</RouterLink>
    </div>
    
    <!-- Cart Content Layout -->
    <div v-else class="cart-layout">
      <!-- Items List -->
      <div style="flex: 2;">
        <div v-for="item in cartStore.cart.items" :key="item.id" class="card" style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3>{{ item.product_name }}</h3>
            <p style="color: #10b981; font-weight: bold; margin: 5px 0;">${{ item.product_price }}</p>
            <p style="margin: 0; color: #64748b; font-size: 14px;">Qty: {{ item.quantity }}</p>
          </div>
          <button @click="cartStore.removeFromCart(item.id)" class="btn btn-danger btn-sm">Remove</button>
        </div>
      </div>
      
      <!-- Order Summary Summary -->
      <div style="flex: 1;">
        <div class="card" style="background-color: #f8fafc;">
          <h3>Summary</h3>
          <p>Total Items: {{ totalItems }}</p>
          <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 15px 0;" />
          <p style="font-size: 18px; font-weight: bold;">
            Total: ${{ totalPrice }}
          </p>
          <button @click="placeOrder" class="btn" style="width: 100%; margin-top: 15px; background-color: #10b981;">Place Order</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cart-layout {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
@media (min-width: 768px) {
  .cart-layout {
    flex-direction: row;
    align-items: flex-start;
  }
}
</style>