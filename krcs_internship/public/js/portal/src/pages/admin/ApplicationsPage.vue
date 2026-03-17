<template>
  <div>
    <h1 class="page-title">Applications</h1>

    <div class="toolbar">
      <input v-model="search" placeholder="Search by name or email…" class="search-input" />
      <select v-model="statusFilter" @change="load">
        <option value="">All Statuses</option>
        <option>Pending</option><option>Under Review</option>
        <option>Shortlisted</option><option>Accepted</option><option>Rejected</option>
      </select>
      <button class="btn-export" @click="exportCsv">↓ Export CSV</button>
    </div>

    <!-- Bulk actions bar -->
    <div v-if="selected.length" class="bulk-bar">
      <span>{{ selected.length }} selected</span>
      <button @click="bulkUpdate('Under Review')">→ Under Review</button>
      <button @click="bulkUpdate('Shortlisted')">Shortlist</button>
      <button @click="bulkUpdate('Accepted')">Accept</button>
      <button class="btn-reject" @click="bulkUpdate('Rejected')">Reject</button>
    </div>

    <div v-if="store.loading" class="loading-msg">Loading…</div>
    <div v-else class="table-card">
      <table>
        <thead>
          <tr>
            <th><input type="checkbox" @change="toggleAll" :checked="allSelected" /></th>
            <th>Name</th>
            <th>Email</th>
            <th>Posting</th>
            <th>University</th>
            <th>Date</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="app in filtered" :key="app.name">
            <tr :class="expanded === app.name ? 'row-expanded' : ''">
              <td><input type="checkbox" :value="app.name" v-model="selected" /></td>
              <td class="td-name">{{ app.applicant_name }}</td>
              <td>{{ app.email }}</td>
              <td>{{ app.title || app.posting }}</td>
              <td>{{ app.university || '—' }}</td>
              <td>{{ formatDate(app.date_applied) }}</td>
              <td><StatusBadge :status="app.status" /></td>
              <td>
                <div class="action-row">
                  <button class="btn-action" @click="toggleExpand(app.name)">
                    {{ expanded === app.name ? 'Collapse' : 'View' }}
                  </button>
                  <select
                    :value="app.status"
                    @change="updateStatus(app, $event.target.value)"
                    class="status-select"
                  >
                    <option>Pending</option>
                    <option>Under Review</option>
                    <option>Shortlisted</option>
                    <option>Accepted</option>
                    <option>Rejected</option>
                  </select>
                </div>
              </td>
            </tr>
            <!-- Expanded detail row -->
            <tr v-if="expanded === app.name" class="detail-row">
              <td colspan="8">
                <div class="detail-panel">
                  <div class="detail-cols">
                    <div>
                      <strong>Course:</strong> {{ app.course || '—' }}<br/>
                      <strong>Year:</strong> {{ app.year_of_study || '—' }}<br/>
                      <strong>Phone:</strong> {{ app.phone || '—' }}
                    </div>
                    <div v-if="app.timeline?.length">
                      <strong>Timeline:</strong>
                      <div v-for="t in app.timeline" :key="t.date + t.action" class="timeline-entry">
                        <span class="tl-dot">●</span>
                        <span>{{ t.action }}</span>
                        <span class="tl-date">{{ t.date }}</span>
                      </div>
                    </div>
                  </div>
                  <div class="detail-actions">
                    <button class="btn-msg" @click="openMessage(app)">✉ Send Message</button>
                  </div>
                </div>
              </td>
            </tr>
          </template>
          <tr v-if="!filtered.length">
            <td colspan="8" class="empty-row">No applications found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Message modal -->
    <div v-if="msgTarget" class="modal-overlay" @click.self="msgTarget = null">
      <div class="modal">
        <h3>Message to {{ msgTarget.applicant_name }}</h3>
        <div class="form-group">
          <label>Subject</label>
          <input v-model="msgForm.subject" />
        </div>
        <div class="form-group">
          <label>Body</label>
          <textarea v-model="msgForm.body" rows="5"></textarea>
        </div>
        <div class="modal-actions">
          <button @click="msgTarget = null" class="btn-cancel">Cancel</button>
          <button @click="sendMsg" class="btn-send">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApplicationsStore } from '../../stores/applications'
import { useMessagesStore } from '../../stores/messages'
import StatusBadge from '../../components/StatusBadge.vue'

const store = useApplicationsStore()
const messages = useMessagesStore()
const search = ref('')
const statusFilter = ref('')
const selected = ref([])
const expanded = ref(null)
const msgTarget = ref(null)
const msgForm = ref({ subject: '', body: '' })

const filtered = computed(() => {
  const s = search.value.toLowerCase()
  return store.applications.filter(a =>
    (!s || a.applicant_name?.toLowerCase().includes(s) || a.email?.toLowerCase().includes(s)) &&
    (!statusFilter.value || a.status === statusFilter.value)
  )
})

const allSelected = computed(() =>
  filtered.value.length > 0 && filtered.value.every(a => selected.value.includes(a.name))
)

function toggleAll(e) {
  selected.value = e.target.checked ? filtered.value.map(a => a.name) : []
}
function toggleExpand(name) {
  expanded.value = expanded.value === name ? null : name
}
function formatDate(d) { return d ? new Date(d).toLocaleDateString('en-KE') : '—' }

async function updateStatus(app, status) {
  await store.updateStatus(app.name, status)
}

async function bulkUpdate(status) {
  await Promise.all(selected.value.map(name => store.updateStatus(name, status)))
  selected.value = []
}

function openMessage(app) {
  msgTarget.value = app
  msgForm.value = { subject: 'Your Application Update', body: '' }
}

async function sendMsg() {
  await messages.adminSend(msgTarget.value.email, msgForm.value.subject, msgForm.value.body, msgTarget.value.name)
  msgTarget.value = null
}

function exportCsv() {
  const rows = [
    ['Name', 'Email', 'Posting', 'University', 'Course', 'Status', 'Date'],
    ...store.applications.map(a => [
      a.applicant_name, a.email, a.title || a.posting,
      a.university, a.course, a.status, a.date_applied
    ])
  ]
  const csv = rows.map(r => r.join(',')).join('\n')
  const a = document.createElement('a')
  a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }))
  a.download = 'applications.csv'
  a.click()
}

function load() { store.fetchAll({ status: statusFilter.value || undefined }) }
onMounted(load)
</script>

<style scoped>
.page-title { font-size: 1.5rem; font-weight: 700; color: #111; margin: 0 0 1.25rem; }
.toolbar { display: flex; gap: .75rem; margin-bottom: 1rem; flex-wrap: wrap; }
.search-input { flex: 1; min-width: 200px; padding: .5rem .75rem; border: 1px solid #d1d5db; border-radius: 7px; font-size: .875rem; outline: none; }
.toolbar select { padding: .5rem .75rem; border: 1px solid #d1d5db; border-radius: 7px; font-size: .875rem; outline: none; }
.btn-export { padding: .5rem 1rem; background: #f9fafb; border: 1px solid #d1d5db; border-radius: 7px; font-size: .82rem; cursor: pointer; }
.bulk-bar { background: #fef2f2; border: 1px solid #fca5a5; border-radius: 8px; padding: .65rem 1rem; display: flex; align-items: center; gap: .75rem; font-size: .85rem; margin-bottom: 1rem; flex-wrap: wrap; }
.bulk-bar button { padding: .35rem .75rem; border-radius: 6px; border: 1px solid #d1d5db; background: #fff; cursor: pointer; font-size: .8rem; font-weight: 600; }
.btn-reject { border-color: #ef4444 !important; color: #991b1b; }
.loading-msg { text-align: center; color: #6b7280; padding: 2rem; }
.table-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; overflow: auto; }
table { width: 100%; border-collapse: collapse; font-size: .82rem; }
th { background: #f9fafb; padding: .65rem .85rem; text-align: left; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb; white-space: nowrap; }
td { padding: .65rem .85rem; border-bottom: 1px solid #f3f4f6; color: #374151; vertical-align: top; }
.td-name { font-weight: 600; color: #111; }
.row-expanded td { background: #fef2f2; }
.action-row { display: flex; gap: .4rem; align-items: center; }
.btn-action { padding: .28rem .65rem; border-radius: 5px; font-size: .75rem; font-weight: 600; border: 1px solid #d1d5db; background: #fff; cursor: pointer; }
.btn-action:hover { border-color: #cc0000; color: #cc0000; }
.status-select { padding: .28rem .4rem; border: 1px solid #d1d5db; border-radius: 5px; font-size: .75rem; outline: none; }
.detail-row td { background: #fafafa; }
.detail-panel { padding: .75rem; }
.detail-cols { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: .82rem; color: #374151; line-height: 1.8; margin-bottom: .75rem; }
.timeline-entry { display: flex; align-items: baseline; gap: .4rem; font-size: .78rem; }
.tl-dot { color: #cc0000; font-size: .6rem; }
.tl-date { color: #9ca3af; margin-left: auto; }
.detail-actions { display: flex; gap: .5rem; }
.btn-msg { padding: .35rem .85rem; background: #fff; border: 1px solid #d1d5db; border-radius: 6px; font-size: .8rem; cursor: pointer; }
.btn-msg:hover { border-color: #cc0000; color: #cc0000; }
.empty-row { text-align: center; color: #9ca3af; padding: 2rem; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.4); z-index: 200; display: flex; align-items: center; justify-content: center; }
.modal { background: #fff; border-radius: 12px; padding: 2rem; max-width: 480px; width: 90%; }
.modal h3 { margin: 0 0 1rem; font-size: 1.05rem; }
.form-group { margin-bottom: .85rem; }
.form-group label { display: block; font-size: .8rem; font-weight: 600; color: #374151; margin-bottom: .3rem; }
.form-group input, .form-group textarea { width: 100%; padding: .5rem .7rem; border: 1px solid #d1d5db; border-radius: 7px; font-size: .875rem; outline: none; font-family: inherit; box-sizing: border-box; resize: vertical; }
.modal-actions { display: flex; gap: .6rem; justify-content: flex-end; margin-top: 1rem; }
.btn-cancel { padding: .55rem 1rem; border: 1px solid #d1d5db; border-radius: 7px; background: #fff; cursor: pointer; font-size: .85rem; }
.btn-send { padding: .55rem 1.1rem; background: #cc0000; color: #fff; border: none; border-radius: 7px; cursor: pointer; font-weight: 600; font-size: .85rem; }
</style>