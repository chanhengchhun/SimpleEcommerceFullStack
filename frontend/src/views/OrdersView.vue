<script setup>
import { ref, onMounted } from 'vue';
import api from '../api/axios.js';

// STATE: Reactive order history list
const orders = ref([]);

// LIFECYCLE: Fetch order history on mount
onMounted(() => {
  api.get('cart/orders/')
    .then(res => orders.value = res.data)
    .catch(err => console.error("Error loading orders:", err));
});

// HELPER: Formats timestamp string to a readable format
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
  });
};
</script>

<template>
  <div>
    <h1>Order History</h1>
    <div v-if="orders.length === 0" style="text-align: center; margin: 40px;">
      <p>No orders placed yet.</p>
      <RouterLink to="/" class="btn">Shop Products</RouterLink>
    </div>
    <div v-else class="orders-list">
      <div v-for="order in orders" :key="order.id" class="card">
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap; margin-bottom: 15px; font-size: 14px; color: #64748b;">
          <span><strong>Order #{{ order.id }}</strong></span>
          <span>Date: {{ formatDate(order.created_at) }}</span>
          <span style="background-color: #f1f5f9; padding: 2px 8px; border-radius: 12px; font-weight: bold; color: #475569;">
            {{ order.status }}
          </span>
        </div>

        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 14px;">
          <thead>
            <tr style="border-bottom: 1px solid #e2e8f0; color: #64748b;">
              <th style="padding: 8px 0;">Item Name</th>
              <th style="padding: 8px 0; text-align: right;">Price</th>
              <th style="padding: 8px 0; text-align: center;">Quantity</th>
              <th style="padding: 8px 0; text-align: right;">Subtotal</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in order.items" :key="item.id" style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 10px 0;">{{ item.product_name }}</td>
              <td style="padding: 10px 0; text-align: right;">${{ item.product_price }}</td>
              <td style="padding: 10px 0; text-align: center;">{{ item.quantity }}</td>
              <td style="padding: 10px 0; text-align: right;">${{ (parseFloat(item.product_price) * item.quantity).toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
        
        <div style="display: flex; justify-content: flex-end; margin-top: 15px; font-size: 16px; font-weight: bold;">
          <span>Total: ${{ order.total }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
</style>
