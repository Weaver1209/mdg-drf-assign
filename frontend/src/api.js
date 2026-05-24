import axios from 'axios';
const api = axios.create({
  baseURL: '/api/',
  withCredentials: true,
});

api.interceptors.request.use(config => {
  const csrfToken = document.cookie.split('; ').find(c => c.startsWith('csrftoken='));
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken.split('=')[1];
  }
  return config;
});

export default api;