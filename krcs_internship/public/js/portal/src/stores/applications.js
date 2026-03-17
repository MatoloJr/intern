import { defineStore } from 'pinia'
import { ref } from 'vue'
import { frappeCall } from '../lib/frappe'

export const useApplicationsStore = defineStore('applications', () => {
  const applications = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function submitApplication(payload) {
    const res = await frappeCall(
      'krcs_internship.krcs_internship.api.submit_application',
      payload
    )
    return res.message
  }

  async function trackByEmail(email) {
    loading.value = true
    try {
      const res = await frappeCall(
        'krcs_internship.krcs_internship.api.get_application_status',
        { email }
      )
      applications.value = res.message || []
    } finally {
      loading.value = false
    }
  }

  // Admin only
  async function fetchAll(filters = {}) {
    loading.value = true
    try {
      const res = await frappeCall(
        'krcs_internship.krcs_internship.api.admin_get_applications',
        filters
      )
      applications.value = res.message || []
    } finally {
      loading.value = false
    }
  }

  async function updateStatus(name, status, note = '') {
    const res = await frappeCall(
      'krcs_internship.krcs_internship.api.update_application_status',
      { name, status, note }
    )
    // Update locally so the UI reflects immediately without a re-fetch
    const idx = applications.value.findIndex(a => a.name === name)
    if (idx !== -1) applications.value[idx].status = status
    return res.message
  }

  return { applications, loading, error,
           submitApplication, trackByEmail, fetchAll, updateStatus }
})