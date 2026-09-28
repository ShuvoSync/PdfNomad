<template>
  <div class="auth-page">
    <div class="card auth-card">
      <h2>Login</h2>
      <p class="subtitle">Welcome back to PDF Nomad</p>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" required placeholder="you@example.com" />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input v-model="password" type="password" required placeholder="Your password" />
        </div>

        <p v-if="authStore.error" class="error">{{ authStore.error }}</p>

        <button type="submit" class="primary full-width" :disabled="authStore.loading">
          {{ authStore.loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <p class="switch-auth">
        Don't have an account?
        <router-link to="/signup">Sign up</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const email = ref('')
const password = ref('')

async function handleSubmit() {
  const success = await authStore.login(email.value, password.value)
  if (success) {
    router.push('/dashboard')
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
</style>
