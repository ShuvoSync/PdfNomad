import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor — attach JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor — handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// ── Auth ──────────────────────────────────────────────
export const authApi = {
  signup: (data) => api.post('/api/v1/auth/signup', data),
  login: (data) => api.post('/api/v1/auth/login', data),
  me: () => api.get('/api/v1/auth/me'),
}

// ── Templates ─────────────────────────────────────────
export const templatesApi = {
  list: () => api.get('/api/v1/templates/'),
  get: (id) => api.get(`/api/v1/templates/${id}`),
  create: (data) => api.post('/api/v1/templates/', data),
  delete: (id) => api.delete(`/api/v1/templates/${id}`),
}

// ── Generator ─────────────────────────────────────────
export const generatorApi = {
  extract: (formData) =>
    api.post('/api/v1/generator/extract', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  render: (formData) =>
    api.post('/api/v1/generator/render', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      responseType: 'blob',
    }),
}

export default api
