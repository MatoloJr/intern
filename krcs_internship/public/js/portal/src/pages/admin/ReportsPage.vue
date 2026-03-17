<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Reports & Analytics</h1>
      <button class="btn-export" @click="exportAll">↓ Export CSV</button>
    </div>

    <div v-if="loading" class="loading-msg">Loading…</div>
    <template v-else>
      <div class="stat-grid">
        <div v-for="s in summary" :key="s.label" class="stat-card">
          <span class="stat-icon">{{ s.icon }}</span>
          <span class="stat-value">{{ s.value }}</span>
          <span class="stat-label">{{ s.label }}</span>
        </div>
      </div>

      <div class="charts-row">
        <div class="chart-card">
          <h3>Applications by Department</h3>
          <div v-if="!admin.deptBreakdown.length" class="empty-chart">No data yet</div>
          <div v-else class="bar-chart">
            <div v-for="d in admin.deptBreakdown" :key="d.department" class="bar-row">
              <span class="bar-label">{{ d.department }}</span>
              <div class="bar-track">
                <div class="bar-fill" :style="{ width: pct(d.count, maxDept) + '%' }"></div>
              </div>
              <span class="bar-count">{{ d.count }}</span>
            </div>
          </div>
        </div>

        <div class="chart-card">
          <h3>Applications by University</h3>
          <div v-if="!admin.uniBreakdown.length" class="empty-chart">No data yet</div>
          <table v-else class="mini-table">
            <thead><tr><th>University</th><th>Total</th><th>Accepted</th></tr></thead>
            <tbody>
              <tr v-for="u in admin.uniBreakdown" :key="u.university">
                <td>{{ u.university }}</td>
                <td>{{ u.total }}</td>
                <td>{{ u.accepted }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'

const admin = useAdminStore()
const loading = ref(true)

const summary = computed(() => [
  { icon: '📁', label: 'Total Applications', value: admin.stats?.total_applications ?? 0 },
  { icon: '📋', label: 'Active Postings',    value: admin.stats?.active_postings    ?? 0 },
  { icon: '✅', label: 'Accepted',           value: admin.stats?.accepted           ?? 0 },
  { icon: '❌', label: 'Rejected',           value: admin.stats?.rejected           ?? 0 },
])

const maxDept = computed(() =>
  Math.max(...admin.deptBreakdown.map(d => d.count), 1)
)

const pct = (count, max) => Math.round((count / max) * 100)

function exportAll() {
  const rows = [
    ['Department', 'Applications'],
    ...admin.deptBreakdown.map(d => [d.department, d.count])
  ]
  const csv = rows.map(r => r.join(',')).join('\n')
  const a = document.createElement('a')
  a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }))
  a.download = 'krcs-report.csv'
  a.click()
}

onMounted(async () => {
  await Promise.all([admin.fetchStats(), admin.fetchCharts()])
  loading.value = false
})
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; }
.page-title { font-size: 1.5rem; font-weight: 700; color: #111; margin: 0; }
.btn-export { padding: .5rem 1rem; background: #f9fafb; border: 1px solid #d1d5db; border-radius: 7px; font-size: .82rem; cursor: pointer; }
.loading-msg { text-align: center; color: #6b7280; padding: 2rem; }
.stat-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
.stat-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 1.25rem; }
.stat-icon { display: block; font-size: 1.4rem; margin-bottom: .4rem; }
.stat-value { display: block; font-size: 1.75rem; font-weight: 800; color: #111; }
.stat-label { font-size: .78rem; color: #6b7280; }
.charts-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
@media (max-width: 768px) { .charts-row { grid-template-columns: 1fr; } }
.chart-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 1.25rem; }
.chart-card h3 { font-size: .95rem; font-weight: 700; color: #111; margin: 0 0 1rem; }
.empty-chart { font-size: .85rem; color: #9ca3af; text-align: center; padding: 1rem 0; }
.bar-row { display: flex; align-items: center; gap: .6rem; margin-bottom: .6rem; font-size: .8rem; }
.bar-label { width: 130px; flex-shrink: 0; color: #374151; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bar-track { flex: 1; height: 8px; background: #f3f4f6; border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; background: #cc0000; border-radius: 4px; }
.bar-count { width: 28px; text-align: right; color: #6b7280; }
.mini-table { width: 100%; border-collapse: collapse; font-size: .82rem; }
.mini-table th { background: #f9fafb; padding: .5rem .75rem; text-align: left; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb; }
.mini-table td { padding: .5rem .75rem; border-bottom: 1px solid #f3f4f6; color: #374151; }
</style>