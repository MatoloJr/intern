<!-- krcs_internship/public/js/portal/src/components/AppNavbar.vue -->
<template>
  <nav class="navbar">
    <div class="navbar-inner">
      <RouterLink to="/" class="navbar-brand">
        <img :src="logo" alt="KRCS" class="brand-logo" />
        <div class="brand-text">
          <div class="brand-name">Kenya Red Cross Society</div>
          <div class="brand-sub">Internship & Attachment Portal</div>
        </div>
      </RouterLink>

      <button class="mobile-toggle" @click="mobileOpen = !mobileOpen" aria-label="Toggle menu">
        <span class="toggle-bar"></span>
        <span class="toggle-bar"></span>
        <span class="toggle-bar"></span>
      </button>

      <div :class="['nav-links', mobileOpen ? 'open' : '']">
        <RouterLink to="/internships" @click="mobileOpen = false">Browse Internships</RouterLink>
        <RouterLink to="/track" @click="mobileOpen = false">Track Application</RouterLink>
        <RouterLink to="/about" @click="mobileOpen = false">About</RouterLink>
        <RouterLink to="/login" class="nav-login" @click="mobileOpen = false">Log In</RouterLink>
        <RouterLink to="/login?role=student" class="btn btn-primary btn-sm" @click="mobileOpen = false">Apply Now</RouterLink>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
const logo = '/assets/krcs_internship/images/krcs-logo.png'
const mobileOpen = ref(false)
</script>

<style scoped>
.navbar {
  position: sticky; top: 0; z-index: 100;
  background: rgba(255,255,255,.92); backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  box-shadow: 0 1px 3px rgba(0,0,0,.06);
}
.navbar-inner {
  max-width: 1200px; margin: 0 auto; padding: 0 1.25rem;
  height: 4rem; display: flex; align-items: center; justify-content: space-between;
}
.navbar-brand { display: flex; align-items: center; gap: .65rem; text-decoration: none; }
.brand-logo { height: 2.5rem; width: 2.5rem; object-fit: contain; }
.brand-text { display: none; }
@media (min-width: 480px) { .brand-text { display: block; } }
.brand-name { font-size: .875rem; font-weight: 700; color: var(--foreground); font-family: 'Merriweather', serif; line-height: 1.2; }
.brand-sub { font-size: .65rem; color: var(--muted-foreground); }

.nav-links {
  display: none; flex-direction: column; gap: .5rem;
  position: absolute; top: 4rem; left: 0; right: 0;
  background: var(--card); padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border);
}
.nav-links.open { display: flex; }
@media (min-width: 768px) {
  .nav-links {
    display: flex; flex-direction: row; position: static;
    padding: 0; border: none; align-items: center; gap: 1.75rem;
  }
}
.nav-links a {
  text-decoration: none; color: var(--muted-foreground);
  font-size: .875rem; font-weight: 500;
  transition: color .15s;
}
.nav-links a:hover, .nav-links a.router-link-active { color: var(--foreground); }
.nav-login { }
.mobile-toggle {
  display: flex; flex-direction: column; gap: 5px;
  background: none; border: none; cursor: pointer; padding: .25rem;
}
@media (min-width: 768px) { .mobile-toggle { display: none; } }
.toggle-bar { display: block; width: 22px; height: 2px; background: var(--foreground); border-radius: 2px; }
</style>