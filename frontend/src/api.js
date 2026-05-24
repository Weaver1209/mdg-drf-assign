// src/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  withCredentials: true, // Needed for Django Session Auth
});

// Add this interceptor to handle CSRF for Django if you use session auth
api.interceptors.request.use(config => {
  const csrfToken = document.cookie.split(' ').find(c => c.startsWith('csrftoken='));
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken.split('=')[1];
  }
  return config;
});

export default api;