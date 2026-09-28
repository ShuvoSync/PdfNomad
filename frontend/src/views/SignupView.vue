<template>
  <div class="auth-page">
    <div class="card auth-card">
      <h2>Sign Up</h2>
      <p class="subtitle">Create your PDF Nomad account</p>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Email</label>
          <input v-model="form.email" type="email" required />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input v-model="form.password" type="password" required />
        </div>

        <div class="form-group">
          <label>Full Name</label>
          <input v-model="form.full_name" type="text" />
        </div>

        <div class="form-group">
          <label>Account Type</label>
          <select v-model="form.account_type">
            <option value="individual">Individual</option>
            <option value="business">Business</option>
          </select>
        </div>

        <div class="form-group" v-if="form.account_type === 'business'">
          <label>Company Name</label>
          <input v-model="form.company_name" type="text" />
        </div>

        <p v-if="authStore.error" class="error">{{ authStore.error }}</p>

        <button type="submit" class="primary full-width" :disabled="authStore.loading">
          {{ authStore.loading ? 'Creating account...' : 'Sign Up' }}
        </button>
      </form>

      <p class="switch-auth">
        Already have an account?
        <router-link to="/login">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const form = reactive({
  email: '',
  password: '',
  full_name: '',
  account_type: 'individual',
  company_name: '',
})

async function handleSubmit() {
  const success = await authStore.signup({
    email: form.email,
    password: form.password,
    full_name: form.full_name || undefined,
    account_type: form.account_type,
    company_name: form.company_name || undefined,
  })
  if (success) {
    router.push('/dashboard')
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  padding-top: 2rem;
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
