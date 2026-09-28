<template>
  <div class="home">
    <div class="hero card">
      <h1>PDF Nomad</h1>
      <p>Extract, process, and generate PDF documents with ease.</p>
      <div class="hero-actions">
        <router-link to="/signup" class="cta-btn">Get Started</router-link>
        <router-link to="/login" class="cta-btn secondary">Login</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  display: flex;
  justify-content: center;
  padding-top: 4rem;
}

.hero {
  text-align: center;
  max-width: 600px;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.hero p {
  color: #64748b;
  margin-bottom: 2rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.cta-btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border-radius: 0.375rem;
  font-weight: 500;
  text-decoration: none;
}

.cta-btn.secondary {
  background: #e2e8f0;
  color: #1e293b;
}
</style>
