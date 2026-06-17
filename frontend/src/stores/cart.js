import { defineStore } from "pinia";
import { ref } from "vue";
import api from "../api/axios.js";

// Cart store to manage the user's shopping basket
export const useCartStore = defineStore('cart', () => {
    // STATE: Reactive object matching the serialized cart structure from Django
    const cart = ref({ items: [] });

    // ACTION: Fetches user's cart from Django and stores it in state
    const fetchCart = () => 
        api.get('cart/').then(res => cart.value = res.data);

    // ACTION: Adds or increments an item in the cart using product ID
    const addToCart = (productId, quantity = 1) => 
        api.post('cart/', { product: productId, quantity }).then(res => cart.value = res.data);

    // ACTION: Deletes a specific cart item from database using its item ID
    const removeFromCart = (itemId) => 
        api.delete(`cart/item/${itemId}/`).then(res => cart.value = res.data);

    // ACTION: Places an order based on current cart and clears cart locally
    const checkout = () => 
        api.post('cart/checkout/').then(res => {
            cart.value = { items: [] };
            return res.data;
        });

    return { cart, fetchCart, addToCart, removeFromCart, checkout };
});
