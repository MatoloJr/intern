import { defineStore } from 'pinia'
import { ref } from 'vue'
import { frappeCall } from '../lib/frappe'

export const useAdminStore = defineStore('admin', () => {
  const stats = ref(null)
  const deptBreakdown = ref([])
  const uniBreakdown = ref([])

  async function fetchStats() {
    const res = await frappeCall(
      'krcs_internship.api.get_dashboard_stats'
    )
    stats.value = res.message
  }

  async function fetchCharts() {
    const [deptRes, uniRes] = await Promise.all([
      frappeCall('krcs_internship.api.get_applications_by_department'),
      frappeCall('krcs_internship.api.get_applications_by_university')
    ])
    deptBreakdown.value = deptRes.message || []
    uniBreakdown.value = uniRes.message || []
  }

  async function createPosting(payload) {
    const res = await frappeCall(
      'krcs_internship.api.create_posting',
      payload
    )
    return res.message
  }

  async function updatePosting(name, payload) {
    return frappeCall(
      'krcs_internship.api.update_posting',
      { name, ...payload }
    )
  }

  async function deletePosting(name) {
    return frappeCall(
      'krcs_internship.api.delete_posting',
      { name }
    )
  }

  return {
    stats, deptBreakdown, uniBreakdown,
    fetchStats, fetchCharts,
    createPosting, updatePosting, deletePosting
  }
})