<template>
  <div class="templates-page">
    <h1>Templates</h1>

    <!-- Create Form -->
    <div class="card">
      <h3>Create Template</h3>
      <form @submit.prevent="handleCreate">
        <div class="form-group">
          <label>Name</label>
          <input v-model="form.name" type="text" required placeholder="Invoice Template" />
        </div>
        <div class="form-group">
          <label>Layout Schema (JSON)</label>
          <textarea
            v-model="form.layout_schema"
            rows="4"
            required
            placeholder='{"title": "Invoice", "font_size": 12}'
          ></textarea>
        </div>
        <div class="form-group">
          <label>Extraction Schema (JSON, optional)</label>
          <textarea
            v-model="form.extraction_schema"
            rows="3"
            placeholder='{"invoice_number": "regex:INV-\\d+"}'
          ></textarea>
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" class="primary" :disabled="loading">
          {{ loading ? 'Creating...' : 'Create Template' }}
        </button>
      </form>
    </div>

    <!-- Template List -->
    <div class="card">
      <h3>Your Templates</h3>
      <p v-if="templates.length === 0" class="empty">No templates yet.</p>
      <ul class="template-list">
        <li v-for="t in templates" :key="t.id" class="template-item">
          <div>
            <strong>{{ t.name }}</strong>
            <small>{{ t.id }}</small>
          </div>
          <button @click="handleDelete(t.id)" class="danger">Delete</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { templatesApi } from '../services/api'

const templates = ref([])
const loading = ref(false)
const error = ref(null)

const form = reactive({
  name: '',
  layout_schema: '',
  extraction_schema: '',
})

async function fetchTemplates() {
  try {
    const res = await templatesApi.list()
    templates.value = res.data
  } catch (e) {
    error.value = 'Failed to load templates'
  }
}

async function handleCreate() {
  loading.value = true
  error.value = null
  try {
    const payload = {
      name: form.name,
      layout_schema: JSON.parse(form.layout_schema),
    }
    if (form.extraction_schema.trim()) {
      payload.extraction_schema = JSON.parse(form.extraction_schema)
    }
    await templatesApi.create(payload)
    form.name = ''
    form.layout_schema = ''
    form.extraction_schema = ''
    await fetchTemplates()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to create template'
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  try {
    await templatesApi.delete(id)
    await fetchTemplates()
  } catch (e) {
    error.value = 'Failed to delete template'
  }
}

onMounted(fetchTemplates)
</script>

<style scoped>
h1 {
  margin-bottom: 1.5rem;
}

.card {
  margin-bottom: 1.5rem;
}

.card h3 {
  margin-bottom: 1rem;
}

.template-list {
  list-style: none;
}

.template-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e2e8f0;
}

.template-item small {
  display: block;
  color: #64748b;
  font-size: 0.75rem;
}

.empty {
  color: #64748b;
}
</style>
