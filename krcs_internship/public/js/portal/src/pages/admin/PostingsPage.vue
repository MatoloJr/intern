<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Manage Postings</h1>
      <RouterLink to="/admin/postings/new" class="btn-primary">+ New Posting</RouterLink>
    </div>

    <div class="toolbar">
      <input v-model="search" placeholder="Search postings…" class="search-input" />
      <select v-model="statusFilter" @change="applyFilter">
        <option value="">All Statuses</option>
        <option>Draft</option>
        <option>Published</option>
        <option>Closed</option>
      </select>
    </div>

    <div v-if="store.loading" class="loading-msg">Loading…</div>
    <div v-else class="table-card">
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Department</th>
            <th>Deadline</th>
            <th>Apps</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in filtered" :key="p.name">
            <td class="td-title">{{ p.title }}</td>
            <td>{{ p.department }}</td>
            <td>{{ formatDate(p.deadline) }}</td>
            <td>{{ p.applications_count || 0 }}</td>
            <td><StatusBadge :status="p.status" /></td>
            <td>
              <div class="action-row">
                <RouterLink :to="'/admin/postings/' + p.name + '/edit'" class="btn-action">Edit</RouterLink>
                <button
                  class="btn-action btn-action-toggle"
                  @click="toggleStatus(p)"
                >{{ p.status === "Published" ? "Close" : "Publish" }}</button>
                <button class="btn-action btn-action-del" @click="confirmDelete(p)">Delete</button>
              </div>
            </td>
          </tr>
          <tr v-if="!filtered.length">
            <td colspan="6" class="empty-row">No postings found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Delete confirm modal -->
    <div v-if="toDelete" class="modal-overlay" @click.self="toDelete = null">
      <div class="modal">
        <h3>Delete Posting?</h3>
        <p>Are you sure you want to delete "<strong>{{ toDelete.title }}</strong>"? This cannot be undone.</p>
        <div class="modal-actions">
          <button @click="toDelete = null" class="btn-cancel">Cancel</button>
          <button @click="doDelete" class="btn-del-confirm" :disabled="deleting">
            {{ deleting ? "Deleting…" : "Delete" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { RouterLink } from "vue-router"
import { useAdminStore } from "../../stores/admin"
import { usePostingsStore } from "../../stores/postings"
import StatusBadge from "../../components/StatusBadge.vue"

const admin = useAdminStore()
const store = usePostingsStore()
const search = ref("")
const statusFilter = ref("")
const toDelete = ref(null)
const deleting = ref(false)

const filtered = computed(() =>
  store.postings.filter((p) => {
    const s = search.value.toLowerCase()
    return (
      (!s || p.title?.toLowerCase().includes(s)) &&
      (!statusFilter.value || p.status === statusFilter.value)
    )
  })
)

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString("en-KE") : "—"
}

function applyFilter() {
  // Refetch with the status filter — admin needs to see all statuses
  store.fetchPostings({ status: statusFilter.value || "" })
}

async function toggleStatus(p) {
  const newStatus = p.status === "Published" ? "Closed" : "Published"
  await admin.updatePosting(p.name, { status: newStatus })
  p.status = newStatus
}

function confirmDelete(p) {
  toDelete.value = p
}

async function doDelete() {
  deleting.value = true
  try {
    await admin.deletePosting(toDelete.value.name)
    store.postings = store.postings.filter((p) => p.name !== toDelete.value.name)
    toDelete.value = null
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  // Admin should see all postings regardless of status
  store.fetchPostings({ status: "" })
})
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; }
.page-title { font-size: 1.5rem; font-weight: 700; color: #111; margin: 0; }
.btn-primary { background: #cc0000; color: #fff; text-decoration: none; padding: .55rem 1.1rem; border-radius: 8px; font-weight: 600; font-size: .875rem; }
.toolbar { display: flex; gap: .75rem; margin-bottom: 1.25rem; flex-wrap: wrap; }
.search-input { flex: 1; min-width: 180px; padding: .5rem .75rem; border: 1px solid #d1d5db; border-radius: 7px; font-size: .875rem; outline: none; }
.search-input:focus { border-color: #cc0000; }
.toolbar select { padding: .5rem .75rem; border: 1px solid #d1d5db; border-radius: 7px; font-size: .875rem; outline: none; }
.loading-msg { text-align: center; color: #6b7280; padding: 2rem; }
.table-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; overflow: auto; }
table { width: 100%; border-collapse: collapse; font-size: .875rem; }
th { background: #f9fafb; padding: .75rem 1rem; text-align: left; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb; white-space: nowrap; }
td { padding: .75rem 1rem; border-bottom: 1px solid #f3f4f6; color: #374151; }
tr:last-child td { border-bottom: none; }
.td-title { font-weight: 600; color: #111; max-width: 220px; }
.action-row { display: flex; gap: .4rem; flex-wrap: wrap; }
.btn-action { padding: .3rem .7rem; border-radius: 6px; font-size: .78rem; font-weight: 600; cursor: pointer; border: 1px solid #d1d5db; background: #fff; color: #374151; text-decoration: none; transition: all .15s; }
.btn-action:hover { border-color: #cc0000; color: #cc0000; }
.btn-action-toggle { border-color: #10b981; color: #065f46; }
.btn-action-toggle:hover { background: #d1fae5; }
.btn-action-del { border-color: #ef4444; color: #991b1b; }
.btn-action-del:hover { background: #fee2e2; }
.empty-row { text-align: center; color: #9ca3af; padding: 2rem; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.4); z-index: 200; display: flex; align-items: center; justify-content: center; }
.modal { background: #fff; border-radius: 12px; padding: 2rem; max-width: 420px; width: 90%; }
.modal h3 { margin: 0 0 .75rem; font-size: 1.1rem; }
.modal p { font-size: .875rem; color: #374151; margin: 0 0 1.5rem; }
.modal-actions { display: flex; gap: .75rem; justify-content: flex-end; }
.btn-cancel { padding: .55rem 1.1rem; border: 1px solid #d1d5db; border-radius: 7px; background: #fff; cursor: pointer; font-size: .875rem; }
.btn-del-confirm { padding: .55rem 1.1rem; background: #cc0000; color: #fff; border: none; border-radius: 7px; cursor: pointer; font-weight: 600; font-size: .875rem; }
.btn-del-confirm:disabled { opacity: .6; cursor: default; }
</style>