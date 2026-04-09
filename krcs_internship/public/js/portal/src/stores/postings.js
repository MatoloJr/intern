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
			const params = {
				limit: filters.limit || 50,
				offset: filters.offset || 0,
			}

			// Only add status if explicitly passed; default to "Published" for public portal
			if ("status" in filters) {
				params.status = filters.status
			} else {
				params.status = "Published"
			}

			if (filters.department) params.department = filters.department
			if (filters.location) params.location = filters.location
			if (filters.duration) params.duration = filters.duration
			if (filters.stipend_type) params.stipend_type = filters.stipend_type
			if (filters.search) params.search = filters.search

			const res = await frappeCall("krcs_internship.api.get_postings", params)

			// Frappe wraps all responses in { message: <actual data> }
			const data = res.message
			if (Array.isArray(data)) {
				postings.value = data
			} else if (data && typeof data === 'object') {
				// Unexpected shape — log and use empty
				console.warn('get_postings returned unexpected shape:', data)
				postings.value = []
			} else {
				postings.value = []
			}
		} catch (e) {
			error.value = e.message || "Failed to load postings"
			console.error("fetchPostings error:", e)
			postings.value = []
		} finally {
			loading.value = false
		}
	}

	async function fetchPosting(name) {
		try {
			const res = await frappeCall("krcs_internship.api.get_posting", { name })
			return res.message || null
		} catch (e) {
			console.error("fetchPosting error:", e)
			return null
		}
	}

	async function fetchDepartments() {
		try {
			const res = await frappeCall("krcs_internship.api.get_departments")
			return res.message || []
		} catch (e) {
			console.error("fetchDepartments error:", e)
			return []
		}
	}

	async function fetchUniversities() {
		try {
			const res = await frappeCall("krcs_internship.api.get_universities")
			return res.message || []
		} catch (e) {
			console.error("fetchUniversities error:", e)
			return []
		}
	}

	async function fetchCourses() {
		try {
			const res = await frappeCall("krcs_internship.api.get_courses")
			return res.message || []
		} catch (e) {
			console.error("fetchCourses error:", e)
			return []
		}
	}

	return {
		postings, loading, error,
		fetchPostings, fetchPosting, fetchDepartments,
		fetchUniversities, fetchCourses
	}
})