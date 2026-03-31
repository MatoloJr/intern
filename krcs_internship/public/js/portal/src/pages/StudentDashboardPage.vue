<!-- krcs_internship/public/js/portal/src/pages/StudentDashboardPage.vue -->
<template>
  <div class="dashboard-page">
    <!-- Header -->
    <header class="dash-header">
      <div class="dash-header-inner container">
        <div class="dash-brand">
          <img :src="logo" alt="KRCS" class="dash-logo" />
          <span class="dash-brand-name">Student Portal</span>
        </div>
        <div class="dash-header-right">
          <button class="btn btn-ghost btn-icon notif-btn">
            <Bell :size="18" />
            <span class="notif-dot"></span>
          </button>
          <div class="user-avatar"><User :size="16" /></div>
          <RouterLink to="/" class="btn btn-ghost btn-sm">
            <LogOut :size="16" /> Logout
          </RouterLink>
        </div>
      </div>
    </header>

    <!-- Show application form -->
    <template v-if="showForm">
      <div class="container" style="padding: 2.5rem 1.25rem;">
        <h2 style="font-size:1.5rem; font-family:'Merriweather',serif; margin: 0 0 .4rem;">New Application</h2>
        <p style="color:var(--muted-foreground); margin: 0 0 2rem; font-size:.9rem;">Complete all sections to submit your internship/attachment application</p>
        <ApplicationForm @cancel="showForm = false" @submitted="onSubmitted" />
      </div>
    </template>

    <!-- Dashboard content -->
    <template v-else>
      <div class="container dash-content">
        <div class="dash-top">
          <div>
            <h1 class="dash-title">Welcome back, {{ studentName }} 👋</h1>
            <p class="dash-subtitle">Track your applications and manage your profile</p>
          </div>
          <button class="btn btn-primary" @click="showForm = true">
            <Plus :size="16" /> New Application
          </button>
        </div>

        <!-- Stat cards -->
        <div class="dash-stats">
          <div class="dash-stat-card card" v-for="s in statCards" :key="s.label">
            <div class="dash-stat-inner">
              <div class="dash-stat-icon" :style="{ background: s.bg }">
                <component :is="s.icon" :size="20" :color="s.color" />
              </div>
              <div>
                <div class="dash-stat-value">{{ s.value }}</div>
                <div class="dash-stat-label">{{ s.label }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Application card -->
        <div v-if="application" class="app-card card">
          <div class="app-card-header">
            <div>
              <div class="app-card-title">Application {{ application.id }}</div>
              <div class="app-card-dept">{{ application.department }} · {{ application.county }}</div>
            </div>
            <span :class="['badge', statusBadgeClass]">
              <component :is="statusIcon" :size="12" style="margin-right:.25rem;" />
              {{ statusLabel }}
            </span>
          </div>
          <div class="app-card-body">
            <div class="progress-section">
              <div class="progress-meta">
                <span class="progress-label">Review Progress</span>
                <span class="progress-pct">{{ application.progress }}%</span>
              </div>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: application.progress + '%' }"></div>
              </div>
            </div>
            <div class="app-meta-grid">
              <div>
                <div class="meta-label">Applied</div>
                <div class="meta-value">{{ application.appliedDate }}</div>
              </div>
              <div>
                <div class="meta-label">Expected Response</div>
                <div class="meta-value">Within 2 weeks</div>
              </div>
            </div>
            <div class="app-note">
              <strong>Note:</strong> Your application is currently being reviewed by the {{ application.department }} department.
              You'll receive an email notification once a decision is made.
            </div>
          </div>
        </div>

        <div v-else class="empty-state card">
          <FileText :size="40" class="empty-icon" />
          <p>No applications yet. Click "New Application" to get started.</p>
          <button class="btn btn-primary" @click="showForm = true">Apply Now</button>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { Bell, User, LogOut, Plus, FileText, Clock, CheckCircle2, XCircle, TrendingUp } from 'lucide-vue-next'
import ApplicationForm from '../components/ApplicationForm.vue'

import logoUrl from '../assets/krcs-logo.png'
const logo = logoUrl
const showForm = ref(false)
const studentName = ref('James')

const application = ref({
  id: 'APP-009', department: 'ICT & Innovation', county: 'Nairobi',
  status: 'under_review', appliedDate: '2026-03-10', progress: 65,
})

const statusMap = {
  pending: { label: 'Pending', badgeClass: 'badge-yellow', icon: Clock },
  under_review: { label: 'Under Review', badgeClass: 'badge-blue', icon: FileText },
  accepted: { label: 'Accepted', badgeClass: 'badge-green', icon: CheckCircle2 },
  rejected: { label: 'Rejected', badgeClass: 'badge-red', icon: XCircle },
}

const statusLabel = computed(() => statusMap[application.value?.status]?.label || '')
const statusBadgeClass = computed(() => statusMap[application.value?.status]?.badgeClass || '')
const statusIcon = computed(() => statusMap[application.value?.status]?.icon || FileText)

const statCards = [
  { icon: FileText, label: 'Total Applications', value: 1, bg: 'var(--accent)', color: 'var(--accent-foreground)' },
  { icon: Clock, label: 'Under Review', value: 1, bg: '#eff6ff', color: '#2563eb' },
  { icon: CheckCircle2, label: 'Accepted', value: 0, bg: '#f0fdf4', color: '#16a34a' },
]

function onSubmitted() {
  showForm.value = false
}
</script>

<style scoped>
.dashboard-page { min-height: 100vh; background: var(--background); }

/* Header */
.dash-header { background: var(--card); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 50; }
.dash-header-inner { height: 3.75rem; display: flex; align-items: center; justify-content: space-between; }
.dash-brand { display: flex; align-items: center; gap: .75rem; }
.dash-logo { height: 2rem; width: 2rem; object-fit: contain; }
.dash-brand-name { font-weight: 700; font-family: 'Merriweather', serif; font-size: .875rem; color: var(--foreground); }
.dash-header-right { display: flex; align-items: center; gap: .75rem; }
.notif-btn { position: relative; }
.notif-dot { position: absolute; top: .4rem; right: .4rem; width: .5rem; height: .5rem; border-radius: 50%; background: var(--primary); }
.user-avatar { width: 2rem; height: 2rem; border-radius: 50%; background: var(--primary); color: var(--primary-foreground); display: flex; align-items: center; justify-content: center; }

/* Content */
.dash-content { padding: 2.5rem 1.25rem; }
.dash-top { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 2rem; }
@media (min-width: 640px) { .dash-top { flex-direction: row; align-items: center; justify-content: space-between; } }
.dash-title { font-size: 1.5rem; font-family: 'Merriweather', serif; color: var(--foreground); margin: 0; }
.dash-subtitle { color: var(--muted-foreground); font-size: .875rem; margin: .25rem 0 0; }

/* Stat cards */
.dash-stats { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
.dash-stat-card { padding: 1.5rem; }
.dash-stat-inner { display: flex; align-items: center; gap: .75rem; }
.dash-stat-icon { width: 2.5rem; height: 2.5rem; border-radius: .75rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.dash-stat-value { font-size: 1.5rem; font-weight: 700; color: var(--foreground); font-family: 'Merriweather', serif; }
.dash-stat-label { font-size: .75rem; color: var(--muted-foreground); }

/* Application card */
.app-card { padding: 1.5rem 2rem; }
.app-card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.25rem; flex-wrap: wrap; gap: .75rem; }
.app-card-title { font-size: 1.05rem; font-weight: 700; font-family: 'Merriweather', serif; color: var(--foreground); }
.app-card-dept { font-size: .875rem; color: var(--muted-foreground); margin-top: .2rem; }
.app-card-body { display: flex; flex-direction: column; gap: 1rem; }

/* Badge colors */
.badge-yellow { background: #fef9c3; color: #854d0e; border-color: #fde68a; }
.badge-blue { background: #dbeafe; color: #1e40af; border-color: #bfdbfe; }
.badge-green { background: #dcfce7; color: #166534; border-color: #bbf7d0; }
.badge-red { background: #fee2e2; color: #991b1b; border-color: #fecaca; }

/* Progress */
.progress-section { }
.progress-meta { display: flex; justify-content: space-between; font-size: .875rem; margin-bottom: .5rem; }
.progress-label { color: var(--muted-foreground); }
.progress-pct { font-weight: 600; color: var(--foreground); }

/* App meta */
.app-meta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.meta-label { font-size: .8rem; color: var(--muted-foreground); margin-bottom: .2rem; }
.meta-value { font-size: .875rem; font-weight: 600; color: var(--foreground); }
.app-note { background: var(--accent); border-radius: .5rem; padding: 1rem; font-size: .875rem; color: var(--accent-foreground); }

/* Empty state */
.empty-state { padding: 3rem; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 1rem; }
.empty-icon { color: var(--muted-foreground); }
</style>