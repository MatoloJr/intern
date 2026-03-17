<template>
  <div class="page-wrap">
    <AppNavbar />

    <div v-if="loading" class="loading-state">Loading…</div>
    <div v-else-if="!posting" class="loading-state">Posting not found.</div>

    <template v-else>
      <!-- Header band -->
      <div class="detail-header">
        <div class="detail-header-inner">
          <span class="badge-dept">{{ posting.department }}</span>
          <h1>{{ posting.title }}</h1>
          <div class="meta-row">
            <span>📍 {{ posting.location }}</span>
            <span>⏱ {{ posting.duration }}</span>
            <span>👥 {{ posting.positions }} position{{ posting.positions > 1 ? 's' : '' }}</span>
            <span>📅 Deadline: {{ formatDate(posting.deadline) }}</span>
            <span v-if="posting.stipend_type === 'Paid'">
              💰 KES {{ Number(posting.stipend_amount).toLocaleString() }}/mo
            </span>
          </div>
        </div>
      </div>

      <div class="detail-body">
        <!-- Main content -->
        <div class="detail-main">
          <section>
            <h2>Overview</h2>
            <div class="divider"></div>
            <div class="prose" v-html="posting.description"></div>
          </section>

          <section v-if="posting.responsibilities_list?.length">
            <h2>Responsibilities</h2>
            <div class="divider"></div>
            <ul class="check-list">
              <li v-for="r in posting.responsibilities_list" :key="r">{{ r }}</li>
            </ul>
          </section>

          <section v-if="posting.requirements_list?.length">
            <h2>Requirements</h2>
            <div class="divider"></div>
            <ul class="check-list">
              <li v-for="r in posting.requirements_list" :key="r">{{ r }}</li>
            </ul>
          </section>

          <section v-if="posting.skills_list?.length">
            <h2>Skills Required</h2>
            <div class="divider"></div>
            <div class="skills-row">
              <span v-for="s in posting.skills_list" :key="s" class="skill-tag">{{ s }}</span>
            </div>
          </section>
        </div>

        <!-- Sidebar -->
        <aside class="detail-sidebar">
          <div class="sidebar-card">
            <div class="deadline-display" :class="urgent ? 'urgent' : ''">
              {{ daysLeft > 0 ? daysLeft + ' days left' : 'Closed' }}
            </div>
            <RouterLink
              :to="'/internships/' + posting.name + '/apply'"
              class="btn-apply"
              :class="daysLeft <= 0 ? 'disabled' : ''"
            >Apply Now</RouterLink>
            <button class="btn-share" @click="copyLink">🔗 Share</button>
            <div class="sidebar-stats">
              <div class="stat-row">
                <span>Applications</span>
                <span>{{ posting.applications_count || 0 }}</span>
              </div>
              <div class="stat-row">
                <span>Positions</span>
                <span>{{ posting.positions }}</span>
              </div>
              <div class="stat-row">
                <span>Stipend</span>
                <StatusBadge :status="posting.stipend_type" />
              </div>
            </div>
          </div>
        </aside>
      </div>

      <!-- Similar postings -->
      <div v-if="posting.similar?.length" class="similar-section">
        <div class="similar-inner">
          <h2>Similar Internships</h2>
          <div class="cards-grid">
            <InternshipCard v-for="p in posting.similar" :key="p.name" :posting="p" />
          </div>
        </div>
      </div>
    </template>

    <!-- Mobile sticky apply bar -->
    <div v-if="posting" class="mobile-apply-bar">
      <RouterLink
        :to="'/internships/' + posting.name + '/apply'"
        class="btn-apply"
      >Apply Now</RouterLink>
    </div>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import AppNavbar from '../components/AppNavbar.vue'
import AppFooter from '../components/AppFooter.vue'
import InternshipCard from '../components/InternshipCard.vue'
import StatusBadge from '../components/StatusBadge.vue'
import { usePostingsStore } from '../stores/postings'

const route = useRoute()
const store = usePostingsStore()
const posting = ref(null)
const loading = ref(true)

const daysLeft = computed(() => {
  if (!posting.value?.deadline) return 0
  return Math.ceil((new Date(posting.value.deadline) - new Date()) / 86400000)
})
const urgent = computed(() => daysLeft.value > 0 && daysLeft.value <= 7)

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('en-KE', { day: 'numeric', month: 'long', year: 'numeric' }) : ''
}

function copyLink() {
  navigator.clipboard.writeText(window.location.href)
  alert('Link copied!')
}

onMounted(async () => {
  try {
    posting.value = await store.fetchPosting(route.params.id)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page-wrap { display: flex; flex-direction: column; min-height: 100vh; }
.loading-state { text-align: center; padding: 4rem; color: #6b7280; flex: 1; }
.detail-header { background: #cc0000; padding: 2.5rem 1.25rem; color: #fff; }
.detail-header-inner { max-width: 1200px; margin: 0 auto; }
.badge-dept { background: rgba(255,255,255,.2); color: #fff; font-size: .75rem; font-weight: 600; padding: .25rem .7rem; border-radius: 20px; display: inline-block; margin-bottom: .75rem; }
.detail-header h1 { font-size: clamp(1.4rem, 3vw, 2rem); font-weight: 800; margin: 0 0 1rem; }
.meta-row { display: flex; flex-wrap: wrap; gap: 1rem; font-size: .85rem; opacity: .9; }
.detail-body { max-width: 1200px; margin: 0 auto; padding: 2rem 1.25rem; display: flex; gap: 2rem; align-items: flex-start; }
.detail-main { flex: 1; min-width: 0; }
.detail-main section { margin-bottom: 2.25rem; }
.detail-main h2 { font-size: 1.15rem; font-weight: 700; color: #111; margin: 0; }
.divider { width: 36px; height: 2px; background: #cc0000; margin: .5rem 0 1rem; border-radius: 2px; }
.prose { font-size: .9rem; color: #374151; line-height: 1.7; }
.check-list { list-style: none; padding: 0; margin: 0; }
.check-list li { display: flex; gap: .6rem; font-size: .88rem; color: #374151; margin-bottom: .6rem; }
.check-list li::before { content: '✓'; color: #cc0000; font-weight: 700; flex-shrink: 0; }
.skills-row { display: flex; flex-wrap: wrap; gap: .5rem; }
.skill-tag { background: #f3f4f6; color: #374151; font-size: .78rem; font-weight: 600; padding: .3rem .75rem; border-radius: 20px; }
.detail-sidebar { width: 260px; flex-shrink: 0; position: sticky; top: 80px; }
.sidebar-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.deadline-display { text-align: center; font-size: 1.1rem; font-weight: 700; color: #374151; margin-bottom: 1rem; }
.deadline-display.urgent { color: #cc0000; }
.btn-apply {
  display: block;
  width: 100%;
  background: #cc0000;
  color: #fff;
  text-align: center;
  padding: .75rem;
  border-radius: 8px;
  font-weight: 700;
  text-decoration: none;
  margin-bottom: .6rem;
  font-size: .9rem;
  transition: background .15s;
}
.btn-apply:hover { background: #a30000; }
.btn-apply.disabled { opacity: .5; pointer-events: none; }
.btn-share {
  display: block;
  width: 100%;
  background: none;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: .6rem;
  font-size: .85rem;
  cursor: pointer;
  color: #374151;
  transition: border-color .15s;
}
.btn-share:hover { border-color: #cc0000; }
.sidebar-stats { margin-top: 1.25rem; border-top: 1px solid #e5e7eb; padding-top: 1rem; }
.stat-row { display: flex; justify-content: space-between; font-size: .82rem; color: #6b7280; margin-bottom: .5rem; align-items: center; }
.similar-section { background: #f9fafb; padding: 2.5rem 1.25rem; }
.similar-inner { max-width: 1200px; margin: 0 auto; }
.similar-inner h2 { font-size: 1.25rem; font-weight: 700; color: #111; margin-bottom: 1.25rem; }
.cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.25rem; }
.mobile-apply-bar {
  display: none;
  position: fixed;
  bottom: 0; left: 0; right: 0;
  background: #fff;
  border-top: 1px solid #e5e7eb;
  padding: .75rem 1.25rem;
  z-index: 50;
}
@media (max-width: 768px) {
  .detail-body { flex-direction: column; }
  .detail-sidebar { display: none; }
  .mobile-apply-bar { display: block; }
}
</style>