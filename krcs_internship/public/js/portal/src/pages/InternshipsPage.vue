<template>
  <div class="page-wrap">
    <AppNavbar />
    <div class="page-content">
      <div class="page-header">
        <h1>Browse Internships</h1>
        <div class="divider"></div>
      </div>

      <div class="layout">
        <!-- Filters sidebar -->
        <aside class="filters">
          <div class="filter-group">
            <label>Search</label>
            <input v-model="filters.search" placeholder="Keyword, location…" @input="applyFilters" />
          </div>
          <div class="filter-group">
            <label>Department</label>
            <select v-model="filters.department" @change="applyFilters">
              <option value="">All Departments</option>
              <option v-for="d in departments" :key="d" :value="d">{{ d }}</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Location</label>
            <select v-model="filters.location" @change="applyFilters">
              <option value="">All Locations</option>
              <option v-for="l in locations" :key="l" :value="l">{{ l }}</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Duration</label>
            <select v-model="filters.duration" @change="applyFilters">
              <option value="">Any Duration</option>
              <option>1 month</option>
              <option>3 months</option>
              <option>6 months</option>
              <option>1 year</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Stipend</label>
            <select v-model="filters.stipend_type" @change="applyFilters">
              <option value="">All</option>
              <option>Paid</option>
              <option>Unpaid</option>
            </select>
          </div>
          <button class="btn-clear" @click="clearFilters">Clear Filters</button>
        </aside>

        <!-- Results -->
        <div class="results">
          <div class="results-bar">
            <span>{{ filtered.length }} internship{{ filtered.length !== 1 ? 's' : '' }} found</span>
            <select v-model="sort">
              <option value="newest">Newest First</option>
              <option value="deadline">Deadline Soonest</option>
              <option value="popular">Most Applied</option>
            </select>
          </div>

          <div v-if="store.loading" class="loading-msg">Loading…</div>
          <div v-else-if="!filtered.length" class="empty-msg">
            <p>No internships match your filters.</p>
            <button class="btn-clear" @click="clearFilters">Clear Filters</button>
          </div>
          <div v-else class="cards-grid">
            <InternshipCard v-for="p in sorted" :key="p.name" :posting="p" />
          </div>
        </div>
      </div>
    </div>
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import AppNavbar from '../components/AppNavbar.vue'
import AppFooter from '../components/AppFooter.vue'
import InternshipCard from '../components/InternshipCard.vue'
import { usePostingsStore } from '../stores/postings'

const store = usePostingsStore()
const route = useRoute()
const sort = ref('newest')

const filters = ref({
  search: route.query.search || '',
  department: route.query.department || '',
  location: '',
  duration: '',
  stipend_type: ''
})

const departments = computed(() =>
  [...new Set(store.postings.map(p => p.department).filter(Boolean))]
)
const locations = computed(() =>
  [...new Set(store.postings.map(p => p.location).filter(Boolean))]
)

const filtered = computed(() =>
  store.postings.filter(p => {
    const s = filters.value.search.toLowerCase()
    return (
      (!s || p.title?.toLowerCase().includes(s) ||
             p.department?.toLowerCase().includes(s) ||
             p.location?.toLowerCase().includes(s)) &&
      (!filters.value.department || p.department === filters.value.department) &&
      (!filters.value.location   || p.location   === filters.value.location) &&
      (!filters.value.duration   || p.duration   === filters.value.duration) &&
      (!filters.value.stipend_type || p.stipend_type === filters.value.stipend_type)
    )
  })
)

const sorted = computed(() => {
  const list = [...filtered.value]
  if (sort.value === 'deadline') list.sort((a, b) => new Date(a.deadline) - new Date(b.deadline))
  else if (sort.value === 'popular') list.sort((a, b) => (b.applications_count || 0) - (a.applications_count || 0))
  else list.sort((a, b) => new Date(b.posted_date) - new Date(a.posted_date))
  return list
})

function applyFilters() {}
function clearFilters() {
  filters.value = { search: '', department: '', location: '', duration: '', stipend_type: '' }
}

onMounted(() => store.fetchPostings())

watch(() => route.query, (q) => {
  if (q.search) filters.value.search = q.search
  if (q.department) filters.value.department = q.department
})
</script>

<style scoped>
.page-wrap { display: flex; flex-direction: column; min-height: 100vh; }
.page-content { flex: 1; max-width: 1200px; margin: 0 auto; padding: 2rem 1.25rem; width: 100%; }
.page-header { margin-bottom: 2rem; }
.page-header h1 { font-size: 1.75rem; font-weight: 700; color: #111; margin: 0; }
.divider { width: 48px; height: 3px; background: #cc0000; margin-top: .5rem; border-radius: 2px; }
.layout { display: flex; gap: 1.75rem; align-items: flex-start; }
.filters {
  width: 220px;
  flex-shrink: 0;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.25rem;
  position: sticky;
  top: 80px;
}
.filter-group { margin-bottom: 1rem; }
.filter-group label { display: block; font-size: .78rem; font-weight: 600; color: #374151; margin-bottom: .35rem; }
.filter-group input,
.filter-group select {
  width: 100%;
  padding: .45rem .6rem;
  border: 1px solid #d1d5db;
  border-radius: 7px;
  font-size: .85rem;
  color: #374151;
  outline: none;
}
.filter-group input:focus, .filter-group select:focus { border-color: #cc0000; }
.btn-clear {
  width: 100%;
  padding: .5rem;
  background: none;
  border: 1px solid #d1d5db;
  border-radius: 7px;
  font-size: .82rem;
  color: #6b7280;
  cursor: pointer;
  transition: border-color .15s;
}
.btn-clear:hover { border-color: #cc0000; color: #cc0000; }
.results { flex: 1; min-width: 0; }
.results-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
  font-size: .85rem;
  color: #6b7280;
}
.results-bar select {
  padding: .35rem .6rem;
  border: 1px solid #d1d5db;
  border-radius: 7px;
  font-size: .82rem;
  outline: none;
}
.cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.25rem; }
.loading-msg, .empty-msg { text-align: center; padding: 3rem; color: #6b7280; }
.empty-msg p { margin-bottom: 1rem; }
@media (max-width: 640px) {
  .layout { flex-direction: column; }
  .filters { width: 100%; position: static; }
}
</style>