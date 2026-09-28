<template>
  <div class="dashboard">
    <h1>Dashboard</h1>

    <div class="stats-grid">
      <div class="card stat-card">
        <h3>Templates</h3>
        <p class="stat-value">{{ templates.length }}</p>
      </div>
      <div class="card stat-card">
        <h3>Email</h3>
        <p class="stat-value small">{{ authStore.user?.email }}</p>
      </div>
      <div class="card stat-card">
        <h3>Account Type</h3>
        <p class="stat-value small">{{ authStore.user?.profile?.account_type || 'individual' }}</p>
      </div>
    </div>

    <div class="card quick-actions">
      <h3>Quick Actions</h3>
      <div class="actions-grid">
        <router-link to="/extract" class="action-btn">
          Extract from PDF
        </router-link>
        <router-link to="/generate" class="action-btn">
          Generate PDF
        </router-link>
        <router-link to="/templates" class="action-btn">
          Manage Templates
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { templatesApi } from '../services/api'

const authStore = useAuthStore()
const templates = ref([])

onMounted(async () => {
  try {
    const res = await templatesApi.list()
    templates.value = res.data
  } catch (e) {
    // ignore
  }
})
</script>

<style scoped>
h1 {
  margin-bottom: 1.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card h3 {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
}

.stat-value.small {
  font-size: 1rem;
}

.quick-actions h3 {
  margin-bottom: 1rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.action-btn {
  display: block;
  text-align: center;
  padding: 1rem;
  background: #f1f5f9;
  border-radius: 0.375rem;
  color: #1e293b;
  font-weight: 500;
  text-decoration: none;
}

.action-btn:hover {
  background: #e2e8f0;
  text-decoration: none;
}
</style>
