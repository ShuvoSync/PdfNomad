import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  function initAuth() {
    if (token.value && !user.value) {
      fetchUser()
    }
  }

  async function fetchUser() {
    try {
      const res = await authApi.me()
      user.value = res.data
    } catch (e) {
      logout()
    }
  }

  async function login(email, password) {
    loading.value = true
    error.value = null
    try {
      const res = await authApi.login({ email, password })
      token.value = res.data.access_token
      localStorage.setItem('token', token.value)
      await fetchUser()
      return true
    } catch (e) {
      error.value = e.response?.data?.detail || 'Login failed'
      return false
    } finally {
      loading.value = false
    }
  }

  async function signup(payload) {
    loading.value = true
    error.value = null
    try {
      await authApi.signup(payload)
      await login(payload.email, payload.password)
      return true
    } catch (e) {
      error.value = e.response?.data?.detail || 'Signup failed'
      return false
    } finally {
      loading.value = false
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    initAuth,
    login,
    signup,
    logout,
    fetchUser,
  }
})
