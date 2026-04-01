import { defineStore } from "pinia"
import { ref } from "vue"
import { frappeCall } from "../lib/frappe"

export const usePostingsStore = defineStore("postings", () => {
  const postings = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchPostings(filters = {}) {
    loading.value = true
    error.value = null
    try {
      // Build params — only include status if explicitly set
      // Empty string "" → no status filter (admin sees all)
      // "Published" (default) → public view
      const params = {
        limit: filters.limit || 50,
        offset: filters.offset || 0,
      }

      // Only add status if it's defined in the filters arg
      if ("status" in filters) {
        params.status = filters.status  // may be "" (all) or "Published" etc.
      } else {
        params.status = "Published"     // default for public portal
      }

      if (filters.department) params.department = filters.department
      if (filters.location) params.location = filters.location
      if (filters.duration) params.duration = filters.duration
      if (filters.stipend_type) params.stipend_type = filters.stipend_type
      if (filters.search) params.search = filters.search

      const res = await frappeCall("krcs_internship.api.get_postings", params)
      // Frappe returns data in res.message
      postings.value = res.message || []
    } catch (e) {
      error.value = e.message || "Failed to load postings"
      postings.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchPosting(name) {
    const res = await frappeCall("krcs_internship.api.get_posting", { name })
    return res.message || null
  }

  async function fetchDepartments() {
    const res = await frappeCall("krcs_internship.api.get_departments")
    return res.message || []
  }

  async function fetchUniversities() {
    const res = await frappeCall("krcs_internship.api.get_universities")
    return res.message || []
  }

  async function fetchCourses() {
    const res = await frappeCall("krcs_internship.api.get_courses")
    return res.message || []
  }

  return {
    postings, loading, error,
    fetchPostings, fetchPosting, fetchDepartments,
    fetchUniversities, fetchCourses
  }
})