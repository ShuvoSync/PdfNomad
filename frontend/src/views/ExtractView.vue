<template>
  <div class="extract-page">
    <h1>Extract from PDF</h1>

    <div class="card">
      <form @submit.prevent="handleExtract">
        <div class="form-group">
          <label>PDF File</label>
          <input type="file" accept="application/pdf" @change="onFileChange" required />
        </div>

        <div class="form-group">
          <label>Template (optional)</label>
          <select v-model="selectedTemplate">
            <option value="">No template</option>
            <option v-for="t in templates" :key="t.id" :value="t.id">
              {{ t.name }}
            </option>
          </select>
        </div>

        <button type="submit" class="primary" :disabled="loading || !file">
          {{ loading ? 'Extracting...' : 'Extract' }}
        </button>
      </form>
    </div>

    <!-- Results -->
    <div v-if="result" class="card">
      <h3>Results</h3>
      <div class="result-section">
        <h4>Status</h4>
        <p>{{ result.extraction.status }}</p>
      </div>
      <div class="result-section">
        <h4>Total Pages</h4>
        <p>{{ result.extraction.total_pages }}</p>
      </div>
      <div class="result-section">
        <h4>Raw Text Snippet</h4>
        <pre>{{ result.extraction.raw_text_snippet }}</pre>
      </div>
      <div class="result-section">
        <h4>Extracted Fields</h4>
        <pre>{{ JSON.stringify(result.extraction.extracted_fields, null, 2) }}</pre>
      </div>
      <div class="result-section">
        <h4>Filename</h4>
        <p>{{ result.filename }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { generatorApi, templatesApi } from '../services/api'

const file = ref(null)
const selectedTemplate = ref('')
const templates = ref([])
const loading = ref(false)
const result = ref(null)
const error = ref(null)

function onFileChange(e) {
  file.value = e.target.files[0]
}

async function handleExtract() {
  if (!file.value) return
  loading.value = true
  error.value = null
  result.value = null

  try {
    const formData = new FormData()
    formData.append('file', file.value)
    if (selectedTemplate.value) {
      formData.append('template_id', selectedTemplate.value)
    }
    const res = await generatorApi.extract(formData)
    result.value = res.data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Extraction failed'
  } finally {
    loading.value = false
  }
}

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

.card {
  margin-bottom: 1.5rem;
}

.card h3 {
  margin-bottom: 1rem;
}

.result-section {
  margin-bottom: 1rem;
}

.result-section h4 {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.25rem;
}

pre {
  background: #f8fafc;
  padding: 0.75rem;
  border-radius: 0.375rem;
  overflow-x: auto;
  font-size: 0.875rem;
}
</style>
