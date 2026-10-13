import axios from 'axios';

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';
export const api = axios.create({ baseURL, headers: { 'Content-Type': 'application/json' } });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('crm_access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && !String(error.config?.url || '').includes('/auth/login') && !String(error.config?.url || '').includes('/auth/register')) {
      localStorage.removeItem('crm_access_token');
      localStorage.removeItem('crm_user');
      if (!window.location.pathname.startsWith('/login')) window.location.assign('/login?expired=1');
    }
    const payload = error.response?.data;
    const message = payload?.error?.message || payload?.detail || error.message || 'Request failed';
    return Promise.reject(new Error(message));
  }
);

export const endpoints = {
  auth: '/auth', users: '/users', companies: '/companies', contacts: '/contacts',
  leads: '/leads', deals: '/deals', activities: '/activities', tasks: '/tasks', dashboard: '/dashboard'
};
