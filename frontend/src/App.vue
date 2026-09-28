<template>
  <div id="app">
    <Navbar v-if="authStore.isAuthenticated" />
    <main :class="{ 'with-nav': authStore.isAuthenticated }">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'
import Navbar from './components/Navbar.vue'

const authStore = useAuthStore()

onMounted(() => {
  authStore.initAuth()
})
</script>

<style>
#app {
  min-height: 100vh;
}

main.with-nav {
  padding-top: 4rem;
  padding-left: 1.5rem;
  padding-right: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

main {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}
</style>
