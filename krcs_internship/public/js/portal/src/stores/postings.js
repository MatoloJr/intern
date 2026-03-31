import { defineStore } from 'pinia'
import { ref } from 'vue'
import { frappeCall } from '../lib/frappe'

export const usePostingsStore = defineStore('postings', () => {
  const postings = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchPostings(filters = {}) {
    loading.value = true
    error.value = null
    try {
      const res = await frappeCall(
        'krcs_internship.api.get_postings',
        filters
      )
      postings.value = res.message || []
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function fetchPosting(name) {
    const res = await frappeCall(
      'krcs_internship.api.get_posting',
      { name }
    )
    return res.message
  }

  async function fetchDepartments() {
    const res = await frappeCall(
      'krcs_internship.api.get_departments'
    )
    return res.message || []
  }

  return { postings, loading, error, fetchPostings, fetchPosting, fetchDepartments }
})