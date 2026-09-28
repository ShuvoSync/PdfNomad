<template>
  <nav class="navbar">
    <div class="nav-inner">
      <router-link to="/dashboard" class="brand">PDF Nomad</router-link>
      <div class="nav-links">
        <router-link to="/dashboard">Dashboard</router-link>
        <router-link to="/templates">Templates</router-link>
        <router-link to="/extract">Extract</router-link>
        <router-link to="/generate">Generate</router-link>
      </div>
      <div class="nav-user">
        <span v-if="authStore.user">{{ authStore.user.email }}</span>
        <button @click="handleLogout" class="logout-btn">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

function handleLogin() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  z-index: 100;
  height: 4rem;
}

.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-links a {
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 500;
}

.nav-links a.router-link-active {
  color: #3b82f6;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
  color: #64748b;
}

.logout-btn {
  background: none;
  color: #ef4444;
  padding: 0.25rem 0.5rem;
}
</style>
