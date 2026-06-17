import axios from "axios";

// 1. Create a custom Axios instance.
// We set baseURL to our Django API server. Note the trailing slash:
// by adding '/api/', Axios allows us to call endpoints relatively (e.g., 'auth/login/')
// without losing the '/api/' context path.
const api = axios.create({
    baseURL: 'http://localhost:8000/api/',
});

// 2. Request Interceptor:
// Think of this as a gateway check. Right before Axios sends a request to the backend,
// this function checks if we have a JWT token stored in the browser's localStorage.
// If we do, it automatically attaches it to the "Authorization" header.
// This way, we don't have to manually attach the token on every single API call!
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            // We use standard Bearer Token authorization
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        // If there's an error during request setup, pass it along
        return Promise.reject(error);
    }
);

export default api;