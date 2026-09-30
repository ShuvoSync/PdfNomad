<template>
  <div class="auth-page">
    <div class="card auth-card">
      <h2>Forgot Password</h2>
      <p class="subtitle">Enter your email to receive a password reset link</p>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" required placeholder="you@example.com" />
        </div>

        <p v-if="message" class="success">{{ message }}</p>
        <p v-if="error" class="error">{{ error }}</p>

        <button type="submit" class="primary full-width" :disabled="loading">
          {{ loading ? 'Sending...' : 'Send Reset Link' }}
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
import { useRouter } from 'vue-router'
import { authApi } from '../services/api'

const router = useRouter()

const email = ref('')
const loading = ref(false)
const error = ref(null)
const message = ref(null)

async function handleSubmit() {
  loading.value = true
  error.value = null
  message.value = null
  try {
    const res = await authApi.forgotPassword({ email: email.value })
    message.value = res.data.message
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to send reset link'
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

.success {
  color: #16a34a;
  font-size: 0.875rem;
  margin-bottom: 0.75rem;
}

.error {
  color: #dc2626;
  font-size: 0.875rem;
  margin-bottom: 0.75rem;
}
</style>
