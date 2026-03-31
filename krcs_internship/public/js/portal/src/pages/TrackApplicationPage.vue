<template>
  <div class="page">
    <h1>Track My Applications</h1>

    <form @submit.prevent="lookUp" class="lookup-form">
      <input v-model="email" type="email" placeholder="Enter your email address" required />
      <button type="submit">Look Up</button>
    </form>

    <div v-if="applications.length" class="applications">
      <div v-for="app in applications" :key="app.name" class="app-card">
        <h3>{{ app.title }}</h3>
        <p>{{ app.department }}</p>
        <span :class="['status-badge', app.status.toLowerCase().replace(' ', '-')]">
          {{ app.status }}
        </span>
        <p class="date">Applied: {{ formatDate(app.creation) }}</p>
      </div>
    </div>

    <p v-else-if="searched" class="no-results">
      No applications found for {{ email }}
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { frappeCall } from '../lib/frappe'

const email = ref('')
const applications = ref([])
const searched = ref(false)

async function lookUp() {
  const res = await frappeCall(
    'krcs_internship.api.get_application_status',
    { email: email.value }
  )
  applications.value = res.message || []
  searched.value = true
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-KE')
}
</script>