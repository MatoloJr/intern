<template>
  <div class="page-wrap">
    <AppNavbar />

    <div class="hero-band">
      <h1>Track My Application</h1>
      <p>Enter your email address to see the status of your internship applications.</p>
    </div>

    <div class="content">
      <form class="lookup-card card" @submit.prevent="lookUp">
        <div class="form-group">
          <label class="form-label">Email Address *</label>
          <input
            v-model="email"
            type="email"
            class="form-input"
            placeholder="you@university.ac.ke"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary btn-full" :disabled="loading">
          <span v-if="loading">Searching…</span>
          <span v-else>Track Applications</span>
        </button>
        <p v-if="error" class="error-msg">{{ error }}</p>
      </form>

      <!-- Results -->
      <div v-if="searched && !loading">
        <div v-if="applications.length === 0" class="empty-state card">
          <div class="empty-icon">📭</div>
          <h3>No Applications Found</h3>
          <p>No applications were found for <strong>{{ email }}</strong>.</p>
          <p>Double-check your email or <RouterLink to="/internships">browse open internships</RouterLink>.</p>
        </div>

        <div v-else>
          <h2 class="results-heading">
            {{ applications.length }} application{{ applications.length !== 1 ? "s" : "" }} found
          </h2>

          <div v-for="app in applications" :key="app.name" class="app-card card">
            <div class="app-card-header">
              <div>
                <h3 class="app-title">{{ app.title || "Walk-in Application" }}</h3>
                <p class="app-meta">
                  <span v-if="app.department">{{ app.department }}</span>
                  <span v-if="app.location"> · {{ app.location }}</span>
                  <span> · Applied {{ formatDate(app.date_applied) }}</span>
                </p>
              </div>
              <StatusBadge :status="app.status" />
            </div>

            <!-- Progress bar -->
            <div class="progress-section">
              <div class="progress-bar">
                <div
                  class="progress-fill"
                  :style="{ width: progressPct(app.status) + '%' }"
                  :class="'progress-' + app.status?.toLowerCase().replace(' ', '-')"
                ></div>
              </div>
              <div class="progress-steps">
                <span
                  v-for="step in steps"
                  :key="step.key"
                  :class="['step-dot', isStepActive(app.status, step.key) ? 'step-dot-active' : '']"
                >{{ step.label }}</span>
              </div>
            </div>

            <!-- Timeline -->
            <div v-if="app.timeline?.length" class="timeline">
              <h4>Activity Timeline</h4>
              <div v-for="(entry, i) in app.timeline" :key="i" class="timeline-entry">
                <div class="tl-dot-wrap">
                  <span class="tl-dot"></span>
                  <span v-if="i < app.timeline.length - 1" class="tl-line"></span>
                </div>
                <div class="tl-content">
                  <p class="tl-action">{{ entry.actions }}</p>
                  <p class="tl-date">{{ formatDate(entry.date) }}</p>
                </div>
              </div>
            </div>

            <!-- Status messages -->
            <div v-if="app.status === 'Accepted'" class="status-msg status-msg-success">
              🎉 Congratulations! Your application has been accepted. Watch your email for next steps.
            </div>
            <div v-else-if="app.status === 'Rejected'" class="status-msg status-msg-error">
              Thank you for applying. Unfortunately your application was not successful this time.
            </div>
            <div v-else-if="app.status === 'Shortlisted'" class="status-msg status-msg-info">
              You have been shortlisted! KRCS will be in touch to schedule the next stage.
            </div>
          </div>
        </div>
      </div>
    </div>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref } from "vue"
import { RouterLink } from "vue-router"
import AppNavbar from "../components/AppNavbar.vue"
import AppFooter from "../components/AppFooter.vue"
import StatusBadge from "../components/StatusBadge.vue"
import { frappeCall } from "../lib/frappe"

const email = ref("")
const applications = ref([])
const searched = ref(false)
const loading = ref(false)
const error = ref("")

const steps = [
  { key: "pending", label: "Submitted" },
  { key: "under-review", label: "Under Review" },
  { key: "shortlisted", label: "Shortlisted" },
  { key: "accepted", label: "Accepted" },
]

const statusOrder = {
  Pending: 1,
  "Under Review": 2,
  Shortlisted: 3,
  Accepted: 4,
  Rejected: 0,
}

function progressPct(status) {
  const map = {
    Pending: 20,
    "Under Review": 45,
    Shortlisted: 70,
    Accepted: 100,
    Rejected: 100,
  }
  return map[status] ?? 10
}

function isStepActive(status, stepKey) {
  const normalised = (status || "").toLowerCase().replace(" ", "-")
  const order = ["pending", "under-review", "shortlisted", "accepted"]
  const current = order.indexOf(normalised)
  const target = order.indexOf(stepKey)
  return current >= 0 && target <= current
}

function formatDate(d) {
  if (!d) return ""
  return new Date(d).toLocaleDateString("en-KE", {
    day: "numeric",
    month: "long",
    year: "numeric",
  })
}

async function lookUp() {
  if (!email.value.trim()) return
  loading.value = true
  error.value = ""
  searched.value = false
  try {
    const res = await frappeCall("krcs_internship.api.get_application_status", {
      email: email.value.trim(),
    })
    applications.value = res.message || []
    searched.value = true
  } catch (e) {
    error.value = e.message || "Could not fetch applications. Please try again."
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page-wrap { display: flex; flex-direction: column; min-height: 100vh; }
.hero-band {
  background: #cc0000; color: #fff;
  padding: 3.5rem 1.25rem; text-align: center;
}
.hero-band h1 { font-size: clamp(1.5rem, 3vw, 2rem); font-weight: 800; margin: 0 0 .5rem; }
.hero-band p { font-size: .95rem; opacity: .9; margin: 0; }
.content { max-width: 720px; margin: 0 auto; padding: 2.5rem 1.25rem; flex: 1; width: 100%; }

/* Lookup card */
.lookup-card { padding: 2rem; margin-bottom: 2rem; }
.form-group { margin-bottom: 1.25rem; }
.btn-full { width: 100%; justify-content: center; }
.error-msg { color: #cc0000; font-size: .82rem; margin: .75rem 0 0; }

/* Empty state */
.empty-state { padding: 3rem; text-align: center; }
.empty-icon { font-size: 2.5rem; margin-bottom: .75rem; }
.empty-state h3 { font-size: 1.1rem; font-weight: 700; margin: 0 0 .5rem; }
.empty-state p { font-size: .875rem; color: #6b7280; margin: .25rem 0; }
.empty-state a { color: #cc0000; text-decoration: underline; }

/* Results */
.results-heading { font-size: 1rem; font-weight: 600; color: #374151; margin-bottom: 1rem; }

/* App card */
.app-card { padding: 1.5rem; margin-bottom: 1.25rem; }
.app-card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.25rem; gap: .75rem; flex-wrap: wrap; }
.app-title { font-size: 1.05rem; font-weight: 700; color: #111; margin: 0 0 .25rem; }
.app-meta { font-size: .8rem; color: #6b7280; margin: 0; }

/* Progress */
.progress-section { margin-bottom: 1.25rem; }
.progress-bar { height: 6px; background: #f3f4f6; border-radius: 9999px; overflow: hidden; margin-bottom: .6rem; }
.progress-fill { height: 100%; border-radius: 9999px; transition: width .4s; background: #cc0000; }
.progress-fill.progress-accepted { background: #10b981; }
.progress-fill.progress-rejected { background: #ef4444; }
.progress-steps { display: flex; justify-content: space-between; }
.step-dot { font-size: .72rem; color: #9ca3af; font-weight: 500; }
.step-dot-active { color: #cc0000; font-weight: 700; }

/* Timeline */
.timeline { border-top: 1px solid #e5e7eb; padding-top: 1rem; }
.timeline h4 { font-size: .82rem; font-weight: 700; color: #374151; margin: 0 0 .75rem; text-transform: uppercase; letter-spacing: .05em; }
.timeline-entry { display: flex; gap: .75rem; margin-bottom: .75rem; }
.tl-dot-wrap { display: flex; flex-direction: column; align-items: center; flex-shrink: 0; width: 12px; }
.tl-dot { width: 10px; height: 10px; border-radius: 50%; background: #cc0000; flex-shrink: 0; margin-top: 3px; }
.tl-line { flex: 1; width: 2px; background: #f3f4f6; margin-top: 3px; }
.tl-content { padding-bottom: .5rem; }
.tl-action { font-size: .875rem; color: #374151; margin: 0 0 .15rem; }
.tl-date { font-size: .75rem; color: #9ca3af; margin: 0; }

/* Status messages */
.status-msg { border-radius: 8px; padding: .85rem 1rem; font-size: .85rem; margin-top: 1rem; }
.status-msg-success { background: #d1fae5; color: #065f46; }
.status-msg-error { background: #fee2e2; color: #991b1b; }
.status-msg-info { background: #dbeafe; color: #1e40af; }
</style>