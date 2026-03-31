<!-- krcs_internship/public/js/portal/src/pages/LoginPage.vue -->
<template>
  <div class="login-page">
    <!-- Left branding panel -->
    <div class="login-left">
      <div class="login-left-bg">
        <div class="hero-overlay"></div>
      </div>
      <div class="login-left-content">
        <img :src="logo" alt="KRCS" class="brand-logo-lg" />
        <h1>Welcome to the<br />KRCS Portal</h1>
        <p>Access your internship applications, track your progress, and connect with Kenya's largest humanitarian network.</p>
        <div class="login-stats">
          <div class="login-stat" v-for="s in statItems" :key="s.label">
            <span class="login-stat-value">{{ s.value }}</span>
            <span class="login-stat-label">{{ s.label }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Right form panel -->
    <div class="login-right">
      <RouterLink to="/" class="back-link">
        <ArrowLeft :size="16" /> Back to home
      </RouterLink>

      <div class="login-mobile-brand">
        <img :src="logo" alt="KRCS" class="brand-logo-sm" />
        <div>
          <div class="brand-name-sm">Kenya Red Cross Society</div>
          <div class="brand-sub">Internship & Attachment Portal</div>
        </div>
      </div>

      <!-- Tab switcher -->
      <div class="tabs-list">
        <button
          :class="['tab-trigger', activeTab === 'student' ? 'active' : '']"
          @click="activeTab = 'student'"
        >
          <GraduationCap :size="16" /> Student
        </button>
        <button
          :class="['tab-trigger', activeTab === 'admin' ? 'active' : '']"
          @click="activeTab = 'admin'"
        >
          <ShieldCheck :size="16" /> Admin
        </button>
      </div>

      <!-- Student form -->
      <div v-if="activeTab === 'student'" class="login-card card">
        <div class="login-card-header">
          <h2>{{ isSignUp ? 'Create Account' : 'Student Login' }}</h2>
          <p>{{ isSignUp ? 'Sign up to start your internship application' : 'Access your internship application dashboard' }}</p>
        </div>
        <form @submit.prevent="handleStudentLogin" class="login-form">
          <div v-if="isSignUp" class="form-group">
            <label class="form-label">Full Name</label>
            <input v-model="studentForm.name" class="form-input" placeholder="Enter your full name" required />
          </div>
          <div class="form-group">
            <label class="form-label">Email</label>
            <input v-model="studentForm.email" class="form-input" type="email" placeholder="student@university.ac.ke" required />
          </div>
          <div class="form-group">
            <label class="form-label">Password</label>
            <div class="password-wrap">
              <input
                v-model="studentForm.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                placeholder="••••••••"
                required
              />
              <button type="button" class="password-toggle" @click="showPassword = !showPassword">
                <EyeOff v-if="showPassword" :size="16" />
                <Eye v-else :size="16" />
              </button>
            </div>
          </div>
          <button type="submit" class="btn btn-primary" style="width:100%">
            {{ isSignUp ? 'Create Account' : 'Sign In' }}
          </button>
          <p class="toggle-mode">
            {{ isSignUp ? 'Already have an account?' : "Don't have an account?" }}
            <button type="button" class="toggle-link" @click="isSignUp = !isSignUp">
              {{ isSignUp ? 'Sign In' : 'Sign Up' }}
            </button>
          </p>
        </form>
      </div>

      <!-- Admin form -->
      <div v-if="activeTab === 'admin'" class="login-card card">
        <div class="login-card-header">
          <h2>Admin Login</h2>
          <p>Access the administration panel to manage applications</p>
        </div>
        <form @submit.prevent="handleAdminLogin" class="login-form">
          <div class="form-group">
            <label class="form-label">Admin Email</label>
            <input v-model="adminForm.email" class="form-input" type="email" placeholder="admin@redcross.or.ke" required />
          </div>
          <div class="form-group">
            <label class="form-label">Password</label>
            <div class="password-wrap">
              <input
                v-model="adminForm.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                placeholder="••••••••"
                required
              />
              <button type="button" class="password-toggle" @click="showPassword = !showPassword">
                <EyeOff v-if="showPassword" :size="16" />
                <Eye v-else :size="16" />
              </button>
            </div>
          </div>
          <button type="submit" class="btn btn-primary" style="width:100%">Access Admin Panel</button>
          <p class="admin-note">Contact IT support if you need admin access credentials.</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { ArrowLeft, GraduationCap, ShieldCheck, Eye, EyeOff } from 'lucide-vue-next'

const router = useRouter()
import logoUrl from '../assets/krcs-logo.png'
const logo = logoUrl
const heroImage = '/assets/krcs_internship/images/krcs-hero.jpg'

const activeTab = ref('student')
const isSignUp = ref(false)
const showPassword = ref(false)

const studentForm = ref({ name: '', email: '', password: '' })
const adminForm = ref({ email: '', password: '' })

const statItems = [
  { value: '200+', label: 'Annual Interns' },
  { value: '47', label: 'Counties' },
  { value: '10+', label: 'Departments' },
]

function handleStudentLogin() {
  router.push('/student-dashboard')
}
function handleAdminLogin() {
  router.push('/admin/dashboard')
}
</script>

<style scoped>
.login-page { display: flex; min-height: 100vh; }

/* Left panel */
.login-left {
  display: none;
  position: relative; flex: 1;
  align-items: center; justify-content: center;
}
@media (min-width: 1024px) { .login-left { display: flex; } }
.login-left-bg { position: absolute; inset: 0; }
.hero-img { width: 100%; height: 100%; object-fit: cover; }
.hero-overlay { position: absolute; inset: 0; background: var(--hero-overlay); }
.login-left-content {
  position: relative; z-index: 10;
  text-align: center; padding: 3rem;
  max-width: 480px;
}
.brand-logo-lg { height: 5rem; width: 5rem; object-fit: contain; margin-bottom: 2rem; filter: drop-shadow(0 4px 12px rgba(0,0,0,.3)); }
.login-left-content h1 { font-size: 2.25rem; color: #fff; margin: 0 0 1rem; line-height: 1.2; }
.login-left-content p { color: rgba(255,255,255,.8); font-size: 1rem; line-height: 1.7; }
.login-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 2.5rem; }
.login-stat { text-align: center; }
.login-stat-value { display: block; font-size: 1.75rem; font-weight: 800; color: #fff; font-family: 'Merriweather', serif; }
.login-stat-label { font-size: .75rem; color: rgba(255,255,255,.6); }

/* Right panel */
.login-right {
  flex: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 2rem 1.5rem;
  background: var(--background);
  max-width: 520px;
}
@media (min-width: 1024px) { .login-right { max-width: 50%; } }
.login-right > * { width: 100%; max-width: 420px; }
.back-link {
  display: inline-flex; align-items: center; gap: .4rem;
  font-size: .875rem; color: var(--muted-foreground);
  text-decoration: none; margin-bottom: 2rem;
  transition: color .15s;
}
.back-link:hover { color: var(--foreground); }

.login-mobile-brand {
  display: flex; align-items: center; gap: .75rem;
  margin-bottom: 2rem;
}
@media (min-width: 1024px) { .login-mobile-brand { display: none; } }
.brand-logo-sm { height: 2.5rem; width: 2.5rem; object-fit: contain; }
.brand-name-sm { font-size: .875rem; font-weight: 700; color: var(--foreground); font-family: 'Merriweather', serif; }
.brand-sub { font-size: .75rem; color: var(--muted-foreground); }

.login-card { padding: 2rem; margin-top: 1.5rem; }
.login-card-header { margin-bottom: 1.5rem; }
.login-card-header h2 { font-size: 1.25rem; margin: 0 0 .4rem; font-family: 'Merriweather', serif; }
.login-card-header p { font-size: .875rem; color: var(--muted-foreground); margin: 0; }

.login-form { display: flex; flex-direction: column; gap: 1rem; }
.form-group { display: flex; flex-direction: column; gap: .35rem; }
.password-wrap { position: relative; }
.password-wrap .form-input { padding-right: 2.5rem; }
.password-toggle {
  position: absolute; right: .75rem; top: 50%; transform: translateY(-50%);
  background: none; border: none; cursor: pointer; color: var(--muted-foreground);
  padding: 0;
}
.password-toggle:hover { color: var(--foreground); }

.toggle-mode { text-align: center; font-size: .875rem; color: var(--muted-foreground); margin: 0; }
.toggle-link { background: none; border: none; color: var(--primary); font-weight: 600; cursor: pointer; font-family: inherit; font-size: inherit; padding: 0; }
.toggle-link:hover { text-decoration: underline; }
.admin-note { text-align: center; font-size: .75rem; color: var(--muted-foreground); margin: 0; }
</style>