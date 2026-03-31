<template>
  <div class="page-wrap">
    <AppNavbar />

    <div v-if="loadingPosting" class="loading-state">Loading posting…</div>
    <div v-else-if="!posting && postingId !== 'WALK-IN'" class="loading-state">
      Posting not found.
      <RouterLink to="/internships" class="btn btn-primary" style="margin-top:1rem">Browse Internships</RouterLink>
    </div>

    <template v-else>
      <div class="page-header">
        <div class="page-header-inner">
          <RouterLink :to="postingId !== 'WALK-IN' ? '/internships/' + postingId : '/internships'" class="back-link">
            ← Back
          </RouterLink>
          <h1>{{ posting ? "Apply: " + posting.title : "General Application" }}</h1>
          <div v-if="posting" class="posting-meta">
            <span>📍 {{ posting.location }}</span>
            <span>⏱ {{ posting.duration }}</span>
            <span>📅 Deadline: {{ formatDate(posting.deadline) }}</span>
          </div>
        </div>
      </div>

      <div class="page-content">
        <ApplicationForm
          :postingId="postingId"
          @submitted="onSubmitted"
          @cancel="$router.back()"
        />
      </div>
    </template>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import { useRoute, RouterLink } from "vue-router"
import AppNavbar from "../components/AppNavbar.vue"
import AppFooter from "../components/AppFooter.vue"
import ApplicationForm from "../components/ApplicationForm.vue"
import { usePostingsStore } from "../stores/postings"

const route = useRoute()
const store = usePostingsStore()
const posting = ref(null)
const loadingPosting = ref(false)

const postingId = computed(() => route.params.id || "WALK-IN")

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString("en-KE", { day: "numeric", month: "long", year: "numeric" }) : ""
}

function onSubmitted(ref) {
  // Navigate to tracking page after successful submission
  // Small delay so the success screen in ApplicationForm is visible
}

onMounted(async () => {
  if (postingId.value && postingId.value !== "WALK-IN") {
    loadingPosting.value = true
    try {
      posting.value = await store.fetchPosting(postingId.value)
    } finally {
      loadingPosting.value = false
    }
  }
})
</script>

<style scoped>
.page-wrap { display: flex; flex-direction: column; min-height: 100vh; }
.loading-state {
  flex: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  color: #6b7280; padding: 4rem;
}
.page-header { background: #cc0000; padding: 2rem 1.25rem; color: #fff; }
.page-header-inner { max-width: 720px; margin: 0 auto; }
.back-link { color: rgba(255,255,255,.8); font-size: .85rem; text-decoration: none; display: inline-block; margin-bottom: .75rem; }
.back-link:hover { color: #fff; }
.page-header h1 { font-size: clamp(1.25rem, 3vw, 1.75rem); font-weight: 800; margin: 0 0 .75rem; }
.posting-meta { display: flex; flex-wrap: wrap; gap: 1rem; font-size: .82rem; opacity: .9; }
.page-content { max-width: 720px; margin: 0 auto; padding: 2.5rem 1.25rem; flex: 1; width: 100%; }
</style>