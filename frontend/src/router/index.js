import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth.js';
import ProductsView from '../views/ProductsView.vue';

// 1. Define routes mapping URLs to Page Components
const routes = [
    {
        path: '/',
        name: 'products',
        component: ProductsView
    },
    {
        path: '/login',
        name: 'login',
        // Lazy-load login for performance
        component: () => import('../views/LoginView.vue')
    },
    {
        path: '/register',
        name: 'register',
        // Lazy-load register for performance
        component: () => import('../views/RegisterView.vue')
    },
    {
        path: '/cart',
        name: 'cart',
        component: () => import('../views/CartView.vue'),
        // Meta field to mark this route as authenticated-only
        meta: { requiresAuth: true }
    },
    {
        path: '/orders',
        name: 'orders',
        component: () => import('../views/OrdersView.vue'),
        meta: { requiresAuth: true }
    }
];

// 2. Instantiate Vue Router
const router = createRouter({
    history: createWebHistory(),
    routes
});

// 3. Navigation Guard (Middleware check)
// Right before moving to a new page, this code checks if the target route requires authentication.
// If it does, and the user does NOT have a token (isLoggedIn is false), it redirects them to the /login page.
router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    
    // Check if the route has the meta 'requiresAuth' rule
    if (to.meta.requiresAuth && !authStore.isLoggedIn) {
        // Redirect to login page
        next({ name: 'login' });
    } else {
        // Let the navigation proceed normally
        next();
    }
});

export default router;
