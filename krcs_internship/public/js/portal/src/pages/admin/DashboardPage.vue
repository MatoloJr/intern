<template>
  <div>
    <h1 class="page-title">Dashboard</h1>

    <div v-if="loading" class="loading-msg">Loading…</div>
    <template v-else>
      <!-- Stat cards -->
      <div class="stat-grid">
        <div v-for="s in statCards" :key="s.label" class="stat-card">
          <span class="stat-icon">{{ s.icon }}</span>
          <span class="stat-value">{{ s.value }}</span>
          <span class="stat-label">{{ s.label }}</span>
        </div>
      </div>

      <!-- Charts row -->
      <div class="charts-row">
        <div class="chart-card">
          <h3>Applications by Department</h3>
          <div v-if="!deptData.length" class="empty-chart">No data yet</div>
          <div v-else class="bar-chart">
            <div
              v-for="d in deptData"
              :key="d.department"
              class="bar-row"
            >
              <span class="bar-label">{{ d.department }}</span>
              <div class="bar-track">
                <div
                  class="bar-fill"
                  :style="{ width: barWidth(d.count) + '%' }"
                ></div>
              </div>
              <span class="bar-count">{{ d.count }}</span>
            </div>
          </div>
        </div>

        <div class="chart-card">
          <h3>Status Breakdown</h3>
          <div class="status-breakdown">
            <div v-for="s in statusBreakdown" :key="s.label" class="status-row">
              <span class="status-dot" :style="{ background: s.color }"></span>
              <span class="status-lbl">{{ s.label }}</span>
              <span class="status-count">{{ s.value }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick actions -->
      <div class="quick-actions">
        <h3>Quick Actions</h3>
        <div class="action-btns">
          <RouterLink to="/admin/postings/new" class="action-btn">➕ New Posting</RouterLink>
          <RouterLink to="/admin/applications" class="action-btn">📁 Review Applications</RouterLink>
          <RouterLink to="/admin/reports" class="action-btn">📈 View Reports</RouterLink>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAdminStore } from '../../stores/admin'

const admin = useAdminStore()
const loading = ref(true)

const statCards = computed(() => [
  { icon: '📋', label: 'Active Postings',    value: admin.stats?.active_postings    ?? 0 },
  { icon: '📁', label: 'Total Applications', value: admin.stats?.total_applications ?? 0 },
  { icon: '🕐', label: 'Pending Review',     value: admin.stats?.pending_review     ?? 0 },
  { icon: '✅', label: 'Accepted',           value: admin.stats?.accepted           ?? 0 },
])

const deptData = computed(() => admin.deptBreakdown.slice(0, 6))
const maxDept = computed(() => Math.max(...deptData.value.map(d => d.count), 1))
const barWidth = (count) => Math.round((count / maxDept.value) * 100)

const statusBreakdown = computed(() => [
  { label: 'Pending / Under Review', value: admin.stats?.pending_review ?? 0,  color: '#f59e0b' },
  { label: 'Shortlisted',            value: admin.stats?.shortlisted    ?? 0,  color: '#3b82f6' },
  { label: 'Accepted',               value: admin.stats?.accepted       ?? 0,  color: '#10b981' },
  { label: 'Rejected',               value: admin.stats?.rejected       ?? 0,  color: '#ef4444' },
])

onMounted(async () => {
  await Promise.all([admin.fetchStats(), admin.fetchCharts()])
  loading.value = false
})
</script>

<style scoped>
.page-title { font-size: 1.5rem; font-weight: 700; color: #111; margin: 0 0 1.5rem; }
.loading-msg { text-align: center; color: #6b7280; padding: 2rem; }
.stat-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 1rem; margin-bottom: 1.75rem; }
.stat-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,.05); }
.stat-icon { display: block; font-size: 1.4rem; margin-bottom: .4rem; }
.stat-value { display: block; font-size: 1.75rem; font-weight: 800; color: #111; }
.stat-label { font-size: .78rem; color: #6b7280; }
.charts-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; margin-bottom: 1.75rem; }
@media (max-width: 768px) { .charts-row { grid-template-columns: 1fr; } }
.chart-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,.05); }
.chart-card h3 { font-size: .95rem; font-weight: 700; color: #111; margin: 0 0 1rem; }
.empty-chart { font-size: .85rem; color: #9ca3af; text-align: center; padding: 1rem 0; }
.bar-row { display: flex; align-items: center; gap: .6rem; margin-bottom: .6rem; font-size: .8rem; }
.bar-label { width: 120px; flex-shrink: 0; color: #374151; truncate: true; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bar-track { flex: 1; height: 8px; background: #f3f4f6; border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; background: #cc0000; border-radius: 4px; transition: width .3s; }
.bar-count { width: 28px; text-align: right; color: #6b7280; flex-shrink: 0; }
.status-row { display: flex; align-items: center; gap: .6rem; margin-bottom: .75rem; font-size: .85rem; }
.status-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.status-lbl { flex: 1; color: #374151; }
.status-count { font-weight: 700; color: #111; }
.quick-actions { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 1.25rem; }
.quick-actions h3 { font-size: .95rem; font-weight: 700; color: #111; margin: 0 0 .75rem; }
.action-btns { display: flex; flex-wrap: wrap; gap: .75rem; }
.action-btn { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: .6rem 1rem; font-size: .85rem; font-weight: 600; color: #374151; text-decoration: none; transition: border-color .15s, color .15s; }
.action-btn:hover { border-color: #cc0000; color: #cc0000; }
</style>