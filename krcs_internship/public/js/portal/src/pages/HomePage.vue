<!-- krcs_internship/public/js/portal/src/pages/HomePage.vue -->
<template>
  <div class="home-page">
    <AppNavbar />

    <!-- Hero -->
    <section class="hero">
      <div class="hero-bg">
        <img :src="heroImage" alt="KRCS Volunteers" class="hero-img" />
        <div class="hero-overlay"></div>
        <div class="hero-gradient"></div>
      </div>
      <div class="hero-content container">
        <div class="hero-badge">
          <span class="badge-dot"></span>
          <span>{{ new Date().getFullYear() }} Applications Open</span>
        </div>
        <h1 class="hero-title">
          Shape the Future of<br />
          <em>Humanitarian Work</em>
        </h1>
        <p class="hero-subtitle">
          Join Kenya's largest humanitarian organization. Gain real-world experience in health,
          disaster response, technology, and community development across all 47 counties.
        </p>
        <form class="search-bar" @submit.prevent="doSearch">
          <input v-model="query" class="search-input" placeholder="Search by keyword, location or department…" />
          <button type="submit" class="btn btn-primary search-btn">Search</button>
        </form>
        <div class="hero-actions">
          <RouterLink to="/internships" class="btn btn-lg btn-white">
            Browse Internships <ArrowRight :size="18" />
          </RouterLink>
          <RouterLink to="/track" class="btn btn-lg btn-outline-white">
            Track My Application
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Stats -->
    <section class="stats-section">
      <div class="container stats-grid">
        <div v-for="s in stats" :key="s.label" class="stat-item">
          <component :is="s.icon" :size="24" class="stat-icon" />
          <span class="stat-value">{{ s.value }}</span>
          <span class="stat-label">{{ s.label }}</span>
        </div>
      </div>
    </section>

    <!-- Featured Internships -->
    <section class="section">
      <div class="container">
        <div class="section-header">
          <span class="badge badge-secondary section-badge">Current Openings</span>
          <h2>Featured Internships</h2>
          <p class="section-desc">Explore internship and attachment positions across our departments.</p>
        </div>
        <div v-if="store.loading" class="loading-grid">
          <div v-for="i in 6" :key="i" class="skeleton" style="height: 240px; border-radius: 16px;"></div>
        </div>
        <div v-else class="cards-grid">
          <InternshipCard v-for="p in featured" :key="p.name" :posting="p" />
        </div>
        <div class="section-cta">
          <RouterLink to="/internships" class="btn btn-primary btn-lg" style="border-radius: 9999px;">
            View All Internships <ChevronRight :size="18" />
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Why KRCS -->
    <section class="section section-muted">
      <div class="container">
        <div class="section-header">
          <span class="badge badge-secondary section-badge">Why Join Us</span>
          <h2>More Than an Internship</h2>
          <p class="section-desc">At KRCS, interns don't just observe — they contribute to life-saving work.</p>
        </div>
        <div class="why-grid">
          <div v-for="item in whyItems" :key="item.title" class="why-card">
            <div class="why-icon-wrap">
              <component :is="item.icon" :size="28" class="why-icon" />
            </div>
            <h3>{{ item.title }}</h3>
            <p>{{ item.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="section">
      <div class="container">
        <div class="section-header">
          <span class="badge badge-secondary section-badge">Process</span>
          <h2>How It Works</h2>
        </div>
        <div class="steps-grid">
          <div v-for="(step, i) in steps" :key="i" class="step-card">
            <div class="step-icon-wrap">{{ step.icon }}</div>
            <div class="step-num">Step {{ i + 1 }}</div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Departments -->
    <section class="section section-muted">
      <div class="container">
        <div class="section-header">
          <h2>Departments We Offer</h2>
        </div>
        <div class="dept-grid">
          <div
            v-for="d in departments"
            :key="d.name"
            class="dept-card"
            @click="$router.push('/internships?department=' + d.name)"
          >
            <span class="dept-icon">{{ d.icon }}</span>
            <span>{{ d.name }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials -->
    <section class="section">
      <div class="container">
        <div class="section-header">
          <span class="badge badge-secondary section-badge">Alumni Stories</span>
          <h2>Hear From Our Alumni</h2>
        </div>
        <div class="testimonials-grid">
          <div v-for="t in testimonials" :key="t.name" class="testimonial-card card">
            <div class="testimonial-top">
              <div class="testimonial-avatar">{{ t.avatar }}</div>
              <div>
                <div class="testimonial-name">{{ t.name }}</div>
                <div class="testimonial-role">{{ t.role }} · {{ t.university }}</div>
              </div>
            </div>
            <p class="testimonial-quote">"{{ t.quote }}"</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Banner -->
    <section class="cta-section">
      <div class="hero-bg">
        <img :src="heroImage" alt="" class="hero-img" style="opacity:.2;" />
        <div class="hero-overlay"></div>
      </div>
      <div class="cta-content container">
        <h2>Ready to Make a Difference?</h2>
        <p>Applications for the {{ new Date().getFullYear() }} cohort are now open.</p>
        <div class="hero-actions">
          <RouterLink to="/internships" class="btn btn-lg btn-white">
            Apply as Student <ArrowRight :size="18" />
          </RouterLink>
          <RouterLink to="/admin" class="btn btn-lg btn-outline-white">
            Admin Portal <ArrowRight :size="18" />
          </RouterLink>
        </div>
      </div>
    </section>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import AppNavbar from '../components/AppNavbar.vue'
import AppFooter from '../components/AppFooter.vue'
import InternshipCard from '../components/InternshipCard.vue'
import { usePostingsStore } from '../stores/postings'

// Lucide-style SVG icons as inline components
import { ArrowRight, ChevronRight, Globe, Briefcase, Heart, TrendingUp, Shield, Star } from 'lucide-vue-next'

const router = useRouter()
const store = usePostingsStore()
const query = ref('')
const heroImage = '/assets/krcs_internship/images/krcs-hero.jpg'

const featured = computed(() => store.postings.filter(p => p.featured).slice(0, 6))

const stats = [
  { icon: Globe, value: '47+', label: 'Counties Covered' },
  { icon: Briefcase, value: '200+', label: 'Interns Annually' },
  { icon: Heart, value: '10+', label: 'Departments' },
  { icon: TrendingUp, value: '85%', label: 'Employment Rate' },
]

const whyItems = [
  { icon: Shield, title: 'Real Impact', desc: 'Work on programs that directly affect communities — from drought response to blood drives to first aid training.' },
  { icon: Star, title: 'Mentorship', desc: 'Every intern is paired with a senior professional who guides their development throughout the program.' },
  { icon: Briefcase, title: 'Career Launchpad', desc: '85% of our former interns secure employment within 6 months. Many join KRCS full-time.' },
]

const steps = [
  { icon: '👤', title: 'Browse Openings', desc: 'Explore internships across all KRCS departments and filter by location, duration or stipend.' },
  { icon: '📝', title: 'Submit Application', desc: 'Fill in the multi-step form, upload your CV and cover letter, and submit in minutes.' },
  { icon: '✅', title: 'Track Your Status', desc: 'Use your email address to track every stage of your application in real time.' },
]

const departments = [
  { name: 'Health', icon: '❤️' },
  { name: 'Disaster Response', icon: '🛡️' },
  { name: 'Logistics', icon: '🚛' },
  { name: 'Communication', icon: '📡' },
  { name: 'Finance', icon: '💰' },
  { name: 'Information Technology', icon: '💻' },
  { name: 'Human Resources', icon: '👥' },
  { name: 'Water & Sanitation', icon: '💧' },
]

const testimonials = [
  { avatar: 'GM', name: 'Grace Mwende', role: 'Former Health Intern', university: 'University of Nairobi', quote: 'My internship at KRCS was transformative. I gained hands-on experience in community health that my classroom could not provide.' },
  { avatar: 'DK', name: 'David Kipchoge', role: 'Former IT Intern', university: 'JKUAT', quote: 'Working with the KRCS IT team opened doors I never imagined. I developed real systems that serve thousands of people across Kenya.' },
  { avatar: 'AH', name: 'Amina Hassan', role: 'Former Disaster Response Intern', university: 'Maseno University', quote: 'The disaster response internship taught me resilience and leadership. I was part of real emergency operations that saved lives.' },
]

onMounted(() => store.fetchPostings())

function doSearch() {
  if (query.value.trim()) router.push('/internships?search=' + encodeURIComponent(query.value.trim()))
  else router.push('/internships')
}
</script>

<style scoped>
.home-page { display: flex; flex-direction: column; min-height: 100vh; }

/* Hero */
.hero {
  position: relative;
  min-height: 85vh;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
}
.hero-bg { position: absolute; inset: 0; }
.hero-img { width: 100%; height: 100%; object-fit: cover; }
.hero-overlay { position: absolute; inset: 0; background: var(--hero-overlay); }
.hero-gradient { position: absolute; inset: 0; background: linear-gradient(to top, var(--background), transparent 50%); }
.hero-content {
  position: relative; z-index: 10;
  text-align: center; padding: 2rem 1.25rem;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: .5rem;
  background: rgba(255,255,255,.12); backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,.2);
  border-radius: 9999px; padding: .5rem 1.25rem;
  color: #fff; font-size: .875rem; font-weight: 600;
  letter-spacing: .05em; text-transform: uppercase;
  margin-bottom: 2rem;
}
.badge-dot { width: .5rem; height: .5rem; border-radius: 50%; background: #fff; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: .5; } }
.hero-title {
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  font-weight: 700; color: #fff;
  line-height: 1.15; margin: 0 0 1.25rem;
}
.hero-title em { font-style: italic; }
.hero-subtitle { font-size: 1.1rem; color: rgba(255,255,255,.85); max-width: 600px; margin: 0 auto 2rem; line-height: 1.7; }
.search-bar {
  display: flex; gap: .5rem; max-width: 560px;
  margin: 0 auto 2rem;
  background: #fff; border-radius: .75rem;
  padding: .35rem .35rem .35rem .85rem;
}
.search-input { flex: 1; border: none; outline: none; font-size: .9rem; color: var(--foreground); background: transparent; font-family: inherit; }
.search-btn { border-radius: .5rem; flex-shrink: 0; }
.hero-actions { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }
.btn-white { background: #fff; color: var(--primary); }
.btn-white:hover { background: #f9f9f9; }
.btn-outline-white { border: 2px solid rgba(255,255,255,.4); color: #fff; background: transparent; }
.btn-outline-white:hover { background: rgba(255,255,255,.1); }

/* Stats */
.stats-section { background: var(--krcs-red-dark); padding: 1.5rem 0; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 1rem; text-align: center; }
.stat-item { display: flex; flex-direction: column; align-items: center; gap: .4rem; }
.stat-icon { color: rgba(255,255,255,.8); }
.stat-value { font-size: 1.75rem; font-weight: 800; color: #fff; font-family: 'Merriweather', serif; }
.stat-label { font-size: .8rem; color: rgba(255,255,255,.7); }

/* Section common */
.section { padding: 5rem 0; }
.section-muted { background: hsl(0,0%,97%); }
.section-header { text-align: center; margin-bottom: 3rem; }
.section-badge { letter-spacing: .08em; text-transform: uppercase; font-size: .7rem; margin-bottom: 1rem; }
.section-header h2 { font-size: clamp(1.6rem, 3vw, 2.25rem); color: var(--foreground); margin: .5rem 0; }
.section-desc { color: var(--muted-foreground); max-width: 520px; margin: .5rem auto 0; font-size: .95rem; }
.section-cta { text-align: center; margin-top: 2.5rem; }

/* Cards grid */
.cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.25rem; }
.loading-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.25rem; }

/* Why KRCS */
.why-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 2rem; }
.why-card { text-align: center; padding: 1.5rem; }
.why-icon-wrap {
  width: 3.5rem; height: 3.5rem;
  border-radius: 1rem; background: var(--accent);
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 1rem;
}
.why-icon { color: var(--accent-foreground); }
.why-card h3 { font-size: 1.1rem; font-weight: 700; margin: 0 0 .5rem; }
.why-card p { font-size: .875rem; color: var(--muted-foreground); line-height: 1.7; margin: 0; }

/* Steps */
.steps-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; }
.step-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: calc(var(--radius) * 2); padding: 2rem 1.5rem;
  text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,.05);
}
.step-icon-wrap { font-size: 2rem; margin-bottom: .5rem; }
.step-num { font-size: .75rem; font-weight: 600; color: var(--primary); text-transform: uppercase; letter-spacing: .05em; margin-bottom: .4rem; }
.step-card h3 { font-size: 1rem; font-weight: 700; margin: 0 0 .5rem; }
.step-card p { font-size: .85rem; color: var(--muted-foreground); line-height: 1.6; margin: 0; }

/* Departments */
.dept-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 1rem; }
.dept-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: .75rem; padding: 1.25rem .75rem;
  text-align: center; cursor: pointer;
  transition: box-shadow .15s, border-color .15s;
  font-size: .82rem; font-weight: 600; color: var(--foreground);
  display: flex; flex-direction: column; align-items: center; gap: .5rem;
}
.dept-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,.08); border-color: var(--primary); }
.dept-icon { font-size: 1.75rem; }

/* Testimonials */
.testimonials-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; }
.testimonial-card { padding: 2rem; }
.testimonial-top { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
.testimonial-avatar {
  width: 3rem; height: 3rem; border-radius: 50%;
  background: var(--primary); color: var(--primary-foreground);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: .9rem; flex-shrink: 0;
}
.testimonial-name { font-weight: 700; font-size: .9rem; }
.testimonial-role { font-size: .78rem; color: var(--muted-foreground); }
.testimonial-quote { font-size: .875rem; color: var(--muted-foreground); font-style: italic; line-height: 1.7; margin: 0; }

/* CTA section */
.cta-section { position: relative; padding: 6rem 0; overflow: hidden; }
.cta-content { position: relative; z-index: 10; text-align: center; }
.cta-content h2 { font-size: clamp(1.75rem, 3vw, 2.5rem); color: #fff; margin: 0 0 1rem; }
.cta-content p { font-size: 1.1rem; color: rgba(255,255,255,.8); margin: 0 0 2rem; }
</style>