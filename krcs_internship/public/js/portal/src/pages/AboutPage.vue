<template>
  <div class="page-wrap">
    <AppNavbar />
    <div class="hero-band">
      <h1>About Kenya Red Cross Society</h1>
      <p>Empowering communities, building resilience and nurturing the next generation of humanitarian leaders.</p>
    </div>

    <div class="content">
      <!-- Mission / Vision -->
      <div class="two-col">
        <div class="info-card">
          <div class="card-icon">🎯</div>
          <h3>Our Mission</h3>
          <p>To prevent and alleviate human suffering through mobilisation of the power of humanity by providing quality humanitarian services to the most vulnerable communities.</p>
        </div>
        <div class="info-card">
          <div class="card-icon">🌍</div>
          <h3>Our Vision</h3>
          <p>To be the leading humanitarian organisation in Kenya, providing timely and effective assistance to people affected by disasters and other emergencies.</p>
        </div>
      </div>

      <!-- Values -->
      <section class="section">
        <h2>Our Core Values</h2>
        <div class="divider"></div>
        <div class="values-grid">
          <div v-for="v in values" :key="v.title" class="value-card">
            <div class="value-icon">{{ v.icon }}</div>
            <h4>{{ v.title }}</h4>
            <p>{{ v.desc }}</p>
          </div>
        </div>
      </section>

      <!-- Programme stats -->
      <section class="section stats-section">
        <h2>Our Internship Programme</h2>
        <div class="divider"></div>
        <p class="programme-desc">
          The KRCS Internship Programme provides university students and recent graduates
          with hands-on experience in humanitarian work across Health, Disaster Response,
          IT, Logistics, Finance and Communications.
        </p>
        <div class="stat-boxes">
          <div class="stat-box"><span class="stat-num">500+</span><span>Interns Placed</span></div>
          <div class="stat-box"><span class="stat-num">8</span><span>Departments</span></div>
          <div class="stat-box"><span class="stat-num">47</span><span>Counties Reached</span></div>
        </div>
      </section>
    </div>

    <AppFooter />
  </div>
</template>

<script setup>
import AppNavbar from '../components/AppNavbar.vue'
import AppFooter from '../components/AppFooter.vue'

const values = [
  { icon: '❤️', title: 'Humanity', desc: 'We serve people in need without discrimination.' },
  { icon: '🛡️', title: 'Integrity', desc: 'We act with honesty, transparency and accountability.' },
  { icon: '👥', title: 'Volunteerism', desc: 'We harness the power of volunteers in service delivery.' },
  { icon: '🌐', title: 'Neutrality', desc: 'We remain impartial in all our humanitarian operations.' },
  { icon: '🏅', title: 'Excellence', desc: 'We strive for the highest standards in all we do.' },
  { icon: '💡', title: 'Innovation', desc: 'We embrace creative solutions to humanitarian challenges.' },
]
</script>

<style scoped>
.page-wrap { display: flex; flex-direction: column; min-height: 100vh; }
.hero-band { background: #cc0000; color: #fff; padding: 4rem 1.25rem; text-align: center; }
.hero-band h1 { font-size: clamp(1.5rem, 3vw, 2.25rem); font-weight: 800; margin: 0 0 .75rem; }
.hero-band p { font-size: .95rem; opacity: .9; max-width: 560px; margin: 0 auto; }
.content { max-width: 1100px; margin: 0 auto; padding: 3rem 1.25rem; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 3rem; }
@media (max-width: 600px) { .two-col { grid-template-columns: 1fr; } }
.info-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 2rem; box-shadow: 0 1px 4px rgba(0,0,0,.05); }
.card-icon { font-size: 2rem; margin-bottom: .75rem; }
.info-card h3 { font-size: 1.05rem; font-weight: 700; color: #111; margin: 0 0 .6rem; }
.info-card p { font-size: .87rem; color: #374151; line-height: 1.6; margin: 0; }
.section { margin-bottom: 3rem; }
.section h2 { font-size: 1.5rem; font-weight: 700; color: #111; text-align: center; margin: 0; }
.divider { width: 48px; height: 3px; background: #cc0000; border-radius: 2px; margin: .6rem auto 2rem; }
.values-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 1.25rem; }
.value-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 1.5rem; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,.04); }
.value-icon { font-size: 1.75rem; margin-bottom: .5rem; }
.value-card h4 { font-size: .9rem; font-weight: 700; color: #111; margin: 0 0 .4rem; }
.value-card p { font-size: .8rem; color: #6b7280; line-height: 1.5; margin: 0; }
.stats-section { text-align: center; }
.programme-desc { max-width: 640px; margin: 0 auto 2rem; font-size: .9rem; color: #374151; line-height: 1.7; }
.stat-boxes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; max-width: 440px; margin: 0 auto; }
.stat-box { background: #fef2f2; border-radius: 10px; padding: 1.25rem; }
.stat-num { display: block; font-size: 1.75rem; font-weight: 800; color: #cc0000; }
.stat-box span:last-child { font-size: .78rem; color: #6b7280; }
</style>