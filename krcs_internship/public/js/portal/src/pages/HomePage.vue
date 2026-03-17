<template>
  <div class="home">
    <AppNavbar />

    <!-- Hero -->
    <section class="hero">
      <div class="hero-inner">
        <h1>Shape Your Future with<br/>Kenya Red Cross Society</h1>
        <p>Explore internship opportunities across health, disaster response, IT, logistics and more.</p>
        <form class="search-bar" @submit.prevent="doSearch">
          <input v-model="query" placeholder="Search by keyword, location or department…" />
          <button type="submit">Search</button>
        </form>
        <div class="hero-actions">
          <RouterLink to="/internships" class="btn-primary">Browse Internships</RouterLink>
          <RouterLink to="/track" class="btn-outline">Track My Application</RouterLink>
        </div>
      </div>
    </section>

    <!-- Stats -->
    <section class="stats">
      <div class="stats-inner">
        <div v-for="s in stats" :key="s.label" class="stat-item">
          <span class="stat-value">{{ s.value }}</span>
          <span class="stat-label">{{ s.label }}</span>
        </div>
      </div>
    </section>

    <!-- Featured internships -->
    <section class="section">
      <div class="section-inner">
        <h2>Featured Internships</h2>
        <div class="divider"></div>
        <div v-if="store.loading" class="loading-msg">Loading…</div>
        <div v-else class="cards-grid">
          <InternshipCard
            v-for="p in featured"
            :key="p.name"
            :posting="p"
          />
        </div>
        <div class="section-cta">
          <RouterLink to="/internships" class="btn-primary">View All Internships</RouterLink>
        </div>
      </div>
    </section>

    <!-- How it works -->
    <section class="section section-muted">
      <div class="section-inner">
        <h2>How It Works</h2>
        <div class="divider"></div>
        <div class="steps-grid">
          <div v-for="(step, i) in steps" :key="i" class="step-card">
            <div class="step-icon">{{ step.icon }}</div>
            <div class="step-num">Step {{ i + 1 }}</div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Departments -->
    <section class="section">
      <div class="section-inner">
        <h2>Departments We Offer</h2>
        <div class="divider"></div>
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
    <section class="section section-muted">
      <div class="section-inner">
        <h2>What Our Interns Say</h2>
        <div class="divider"></div>
        <div class="testimonial-wrap">
          <div class="testimonial-card">
            <div class="testimonial-avatar">{{ testimonials[activeTestimonial].avatar }}</div>
            <p class="testimonial-quote">"{{ testimonials[activeTestimonial].quote }}"</p>
            <div class="testimonial-name">{{ testimonials[activeTestimonial].name }}</div>
            <div class="testimonial-role">{{ testimonials[activeTestimonial].role }} · {{ testimonials[activeTestimonial].university }}</div>
          </div>
          <div class="testimonial-dots">
            <button
              v-for="(_, i) in testimonials"
              :key="i"
              :class="['dot', i === activeTestimonial ? 'active' : '']"
              @click="activeTestimonial = i"
            />
          </div>
        </div>
      </div>
    </section>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import AppNavbar from '../components/AppNavbar.vue'
import AppFooter from '../components/AppFooter.vue'
import InternshipCard from '../components/InternshipCard.vue'
import { usePostingsStore } from '../stores/postings'

const router = useRouter()
const store = usePostingsStore()
const query = ref('')
const activeTestimonial = ref(0)

const featured = computed(() =>
  store.postings.filter(p => p.featured).slice(0, 6)
)

const stats = [
  { value: '24+', label: 'Active Internships' },
  { value: '1,250+', label: 'Applications Received' },
  { value: '8', label: 'Departments' },
  { value: '340+', label: 'Students Placed' },
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

let timer
onMounted(() => {
  store.fetchPostings()
  timer = setInterval(() => {
    activeTestimonial.value = (activeTestimonial.value + 1) % testimonials.length
  }, 5000)
})
onUnmounted(() => clearInterval(timer))

function doSearch() {
  if (query.value.trim()) {
    router.push('/internships?search=' + encodeURIComponent(query.value.trim()))
  } else {
    router.push('/internships')
  }
}
</script>

<style scoped>
.home { display: flex; flex-direction: column; min-height: 100vh; }

/* Hero */
.hero {
  background: linear-gradient(135deg, #cc0000 0%, #7a0000 100%);
  padding: 5rem 1.25rem;
  text-align: center;
  color: #fff;
}
.hero-inner { max-width: 720px; margin: 0 auto; }
.hero h1 { font-size: clamp(1.75rem, 4vw, 2.75rem); font-weight: 800; line-height: 1.2; margin-bottom: 1rem; }
.hero p { font-size: 1.05rem; opacity: .9; margin-bottom: 2rem; }
.search-bar {
  display: flex;
  gap: .5rem;
  max-width: 540px;
  margin: 0 auto 1.75rem;
  background: #fff;
  border-radius: 10px;
  padding: .35rem .35rem .35rem .75rem;
}
.search-bar input {
  flex: 1;
  border: none;
  outline: none;
  font-size: .9rem;
  color: #111;
  background: transparent;
}
.search-bar button {
  background: #cc0000;
  color: #fff;
  border: none;
  padding: .55rem 1.2rem;
  border-radius: 7px;
  font-weight: 600;
  cursor: pointer;
}
.hero-actions { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }
.btn-primary {
  background: #fff;
  color: #cc0000;
  padding: .7rem 1.5rem;
  border-radius: 8px;
  font-weight: 700;
  text-decoration: none;
  font-size: .9rem;
  transition: background .15s;
}
.btn-primary:hover { background: #f9f9f9; }
.btn-outline {
  border: 2px solid #fff;
  color: #fff;
  padding: .7rem 1.5rem;
  border-radius: 8px;
  font-weight: 700;
  text-decoration: none;
  font-size: .9rem;
  transition: background .15s;
}
.btn-outline:hover { background: rgba(255,255,255,.1); }

/* Stats */
.stats { background: #7a0000; padding: 1.5rem 1.25rem; }
.stats-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  text-align: center;
}
.stat-value { display: block; font-size: 1.75rem; font-weight: 800; color: #fff; }
.stat-label { font-size: .8rem; color: rgba(255,255,255,.75); }

/* Generic section */
.section { padding: 4rem 1.25rem; }
.section-muted { background: #f9fafb; }
.section-inner { max-width: 1200px; margin: 0 auto; }
.section-inner h2 { font-size: 1.6rem; font-weight: 700; text-align: center; color: #111; margin: 0; }
.divider { width: 60px; height: 3px; background: #cc0000; margin: .75rem auto 2.5rem; border-radius: 2px; }
.section-cta { text-align: center; margin-top: 2rem; }
.section-cta .btn-primary { background: #cc0000; color: #fff; }
.section-cta .btn-primary:hover { background: #a30000; }

/* Cards grid */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
}

/* Steps */
.steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}
.step-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.75rem 1.5rem;
  text-align: center;
  box-shadow: 0 1px 4px rgba(0,0,0,.05);
}
.step-icon { font-size: 2rem; margin-bottom: .5rem; }
.step-num { font-size: .75rem; font-weight: 600; color: #cc0000; text-transform: uppercase; letter-spacing: .05em; margin-bottom: .4rem; }
.step-card h3 { font-size: 1rem; font-weight: 700; margin: 0 0 .5rem; color: #111; }
.step-card p { font-size: .85rem; color: #6b7280; line-height: 1.6; margin: 0; }

/* Departments */
.dept-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 1rem;
}
.dept-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 1.25rem .75rem;
  text-align: center;
  cursor: pointer;
  transition: box-shadow .15s, border-color .15s;
  font-size: .82rem;
  font-weight: 600;
  color: #374151;
}
.dept-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,.08); border-color: #cc0000; }
.dept-icon { display: block; font-size: 1.75rem; margin-bottom: .5rem; }

/* Testimonials */
.testimonial-wrap { max-width: 600px; margin: 0 auto; text-align: center; }
.testimonial-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 1px 4px rgba(0,0,0,.05);
  margin-bottom: 1.25rem;
}
.testimonial-avatar {
  width: 52px; height: 52px;
  background: #cc0000;
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0 auto .75rem;
}
.testimonial-quote { font-size: .9rem; color: #374151; font-style: italic; line-height: 1.7; margin: 0 0 .75rem; }
.testimonial-name { font-weight: 700; color: #111; font-size: .9rem; }
.testimonial-role { font-size: .8rem; color: #6b7280; margin-top: .2rem; }
.testimonial-dots { display: flex; justify-content: center; gap: .5rem; }
.dot { width: 8px; height: 8px; border-radius: 50%; background: #d1d5db; border: none; cursor: pointer; padding: 0; }
.dot.active { background: #cc0000; }
.loading-msg { text-align: center; color: #6b7280; padding: 2rem; }
</style>