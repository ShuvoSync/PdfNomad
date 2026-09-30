<template>
  <div class="auth-page">
    <div class="card auth-card">
      <h2>Reset Password</h2>
      <p class="subtitle">Enter your new password</p>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>New Password</label>
          <input v-model="password" type="password" required placeholder="Minimum 8 characters" />
        </div>

        <div class="form-group">
          <label>Confirm Password</label>
          <input v-model="confirmPassword" type="password" required placeholder="Confirm new password" />
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <button type="submit" class="primary full-width" :disabled="loading">
          {{ loading ? 'Resetting...' : 'Reset Password' }}
        </button>
      </form>

      <p class="switch-auth">
        Remember your password?
        <router-link to="/login">Log in</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authApi } from '../services/api'

const router = useRouter()
const route = useRoute()

const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref(null)

async function handleSubmit() {
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  if (password.value.length < 8) {
    error.value = 'Password must be at least 8 characters long'
    return
  }

  loading.value = true
  error.value = null
  try {
    await authApi.resetPassword({
      token: route.query.token,
      new_password: password.value,
    })
    router.push('/login')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to reset password'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  padding-top: 4rem;
}

.auth-card {
  width: 100%;
  max-width: 400px;
}

h2 {
  margin-bottom: 0.25rem;
}

.subtitle {
  color: #64748b;
  margin-bottom: 1.5rem;
}

.full-width {
  width: 100%;
}

.switch-auth {
  margin-top: 1rem;
  text-align: center;
  font-size: 0.875rem;
  color: #64748b;
}

.error {
  color: #dc2626;
  font-size: 0.875rem;
  margin-bottom: 0.75rem;
}
</style>
