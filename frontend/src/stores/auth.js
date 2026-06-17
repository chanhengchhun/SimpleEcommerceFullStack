import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "../api/axios.js";

// Auth store to manage authentication state
export const useAuthStore = defineStore('auth', () => {
    // STATE: Holds the token or reads it from localStorage to persist user session on refresh
    const token = ref(localStorage.getItem('access_token') || null);

    // GETTER: Reactive helper returning true if a token exists
    const isLoggedIn = computed(() => !!token.value);

    // ACTION: Performs POST request to register account
    const register = (username, email, password) => 
        api.post('auth/register/', { username, email, password });

    // ACTION: Logs the user in, sets token state, and saves tokens in browser localStorage
    const login = async (username, password) => {
        const res = await api.post('auth/token/', { username, password });
        token.value = res.data.access;
        localStorage.setItem('access_token', res.data.access);
        localStorage.setItem('refresh_token', res.data.refresh);
    };

    // ACTION: Resets token state and clears credentials from storage
    const logout = () => {
        token.value = null;
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    };

    return { token, isLoggedIn, register, login, logout };
});