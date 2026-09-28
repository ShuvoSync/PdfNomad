<template>
  <div class="generate-page">
    <h1>Generate PDF</h1>

    <div class="card">
      <form @submit.prevent="handleGenerate">
        <div class="form-group">
          <label>Template</label>
          <select v-model="selectedTemplate" required>
            <option value="" disabled>Select a template</option>
            <option v-for="t in templates" :key="t.id" :value="t.id">
              {{ t.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Data Payload (JSON)</label>
          <textarea
            v-model="dataPayload"
            rows="8"
            required
            placeholder='{"supplier": "Acme", "amount": "100.00", "date": "2026-01-15"}'
          ></textarea>
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <button type="submit" class="primary" :disabled="loading || templates.length === 0">
          {{ loading ? 'Generating...' : 'Generate PDF' }}
        </button>
      </form>
    </div>

    <div v-if="pdfUrl" class="card">
      <h3>Generated PDF</h3>
      <p>
        <a :href="pdfUrl" download="generated.pdf" class="download-link">Download PDF</a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { generatorApi, templatesApi } from '../services/api'

const templates = ref([])
const selectedTemplate = ref('')
const dataPayload = ref('')
const loading = ref(false)
const error = ref(null)
const pdfUrl = ref(null)

async function handleGenerate() {
  loading.value = true
  error.value = null
  pdfUrl.value = null

  try {
    const formData = new FormData()
    formData.append('template_id', selectedTemplate.value)
    formData.append('data_payload_json', dataPayload.value)

    const res = await generatorApi.render(formData)
    const blob = new Blob([res.data], { type: 'application/pdf' })
    pdfUrl.value = URL.createObjectURL(blob)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Generation failed'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    const res = await templatesApi.list()
    templates.value = res.data
  } catch (e) {
    error.value = 'Failed to load templates'
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

.download-link {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border-radius: 0.375rem;
}
</style>
