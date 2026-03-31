<template>
  <div class="page apply-page">
    <div v-if="submitted" class="success-card">
      <div class="check-icon">✓</div>
      <h2>Application Submitted!</h2>
      <p>Reference: <strong>{{ refNumber }}</strong></p>
      <p>A confirmation has been sent to {{ form.email }}</p>
      <button @click="$router.push('/track')">Track My Applications</button>
    </div>

    <form v-else @submit.prevent="handleSubmit">
      <h1>Apply: {{ posting?.title }}</h1>

      <div class="steps">
        <div :class="['step', step >= 1 ? 'active' : '']">1. Personal</div>
        <div :class="['step', step >= 2 ? 'active' : '']">2. Documents</div>
        <div :class="['step', step >= 3 ? 'active' : '']">3. Review</div>
      </div>

      <!-- Step 1 -->
      <div v-if="step === 1" class="form-step">
        <label>Full Name<input v-model="form.applicant_name" required /></label>
        <label>Email<input v-model="form.email" type="email" required /></label>
        <label>Phone<input v-model="form.phone" /></label>
        <label>University<input v-model="form.university" /></label>
        <label>Course<input v-model="form.course" /></label>
        <label>Year of Study
          <select v-model="form.year_of_study">
            <option>First</option><option>Second</option>
            <option>Third</option><option>Fourth</option><option>Graduate</option>
          </select>
        </label>
        <button type="button" @click="step = 2">Next →</button>
      </div>

      <!-- Step 2 -->
      <div v-if="step === 2" class="form-step">
        <label>Cover Letter
          <textarea v-model="form.cover_letter" rows="6"
            placeholder="Tell us why you want this internship..." />
        </label>
        <label>Upload CV (PDF)
          <input type="file" accept=".pdf" @change="handleFile" />
        </label>
        <div class="nav">
          <button type="button" @click="step = 1">← Back</button>
          <button type="button" @click="step = 3">Next →</button>
        </div>
      </div>

      <!-- Step 3 review -->
      <div v-if="step === 3" class="form-step">
        <h3>Review your application</h3>
        <dl>
          <dt>Name</dt><dd>{{ form.applicant_name }}</dd>
          <dt>Email</dt><dd>{{ form.email }}</dd>
          <dt>University</dt><dd>{{ form.university }}</dd>
          <dt>Course</dt><dd>{{ form.course }}</dd>
          <dt>Year</dt><dd>{{ form.year_of_study }}</dd>
        </dl>
        <div class="nav">
          <button type="button" @click="step = 2">← Back</button>
          <button type="submit" :disabled="submitting">
            {{ submitting ? 'Submitting...' : 'Submit Application' }}
          </button>
        </div>
        <p v-if="submitError" class="error">{{ submitError }}</p>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePostingsStore } from '../stores/postings'
import { frappeCall } from '../lib/frappe'

const route = useRoute()
const store = usePostingsStore()
const posting = ref(null)
const step = ref(1)
const submitted = ref(false)
const submitting = ref(false)
const submitError = ref('')
const refNumber = ref('')

const form = ref({
  applicant_name: '', email: '', phone: '',
  university: '', course: '', year_of_study: 'First',
  cover_letter: ''
})

onMounted(async () => {
  posting.value = await store.fetchPosting(route.params.id)
})

async function handleSubmit() {
  submitting.value = true
  submitError.value = ''
  try {
    const res = await frappeCall(
      'krcs_internship.api.submit_application',
      { posting: route.params.id, ...form.value }
    )
    refNumber.value = res.message.name
    submitted.value = true
  } catch (e) {
    submitError.value = e.message || 'Submission failed. Please try again.'
  } finally {
    submitting.value = false
  }
}
</script>