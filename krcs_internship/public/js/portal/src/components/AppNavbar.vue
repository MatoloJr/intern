<template>
  <nav class="navbar">
    <div class="navbar-inner">
      <RouterLink to="/" class="navbar-brand">
        <img :src="logo" alt="KRCS" class="brand-logo" />        <span class="brand-name">KRCS Internship Portal</span>
      </RouterLink>

      <button class="mobile-toggle" @click="mobileOpen = !mobileOpen">
        <span class="toggle-bar"></span>
        <span class="toggle-bar"></span>
        <span class="toggle-bar"></span>
      </button>

      <div :class="['nav-links', mobileOpen ? 'open' : '']">
        <RouterLink to="/internships" @click="mobileOpen = false">Browse Internships</RouterLink>
        <RouterLink to="/track" @click="mobileOpen = false">Track Application</RouterLink>
        <RouterLink to="/about" @click="mobileOpen = false">About</RouterLink>
        <RouterLink to="/admin" class="btn-admin" @click="mobileOpen = false">Admin</RouterLink>
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
  position: sticky;
  top: 0;
  z-index: 100;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0,0,0,.06);
}
.navbar-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.25rem;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.navbar-brand {
  display: flex;
  align-items: center;
  gap: .6rem;
  text-decoration: none;
  color: #111;
  font-weight: 700;
  font-size: 1rem;
}
.brand-logo { height: 36px; width: 36px; object-fit: contain; }
.brand-name { display: none; }
@media (min-width: 480px) { .brand-name { display: inline; } }
.nav-links {
  display: none;
  flex-direction: column;
  gap: .5rem;
  position: absolute;
  top: 64px;
  left: 0; right: 0;
  background: #fff;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #e5e7eb;
}
.nav-links.open { display: flex; }
@media (min-width: 768px) {
  .nav-links {
    display: flex;
    flex-direction: row;
    position: static;
    padding: 0;
    border: none;
    align-items: center;
    gap: 1.5rem;
  }
}
.nav-links a {
  text-decoration: none;
  color: #374151;
  font-size: .9rem;
  font-weight: 500;
  transition: color .15s;
}
.nav-links a:hover, .nav-links a.router-link-active { color: #cc0000; }
.btn-admin {
  background: #cc0000;
  color: #fff !important;
  padding: .45rem 1rem;
  border-radius: 8px;
}
.btn-admin:hover { background: #a30000; }
.mobile-toggle {
  display: flex;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: .25rem;
}
@media (min-width: 768px) { .mobile-toggle { display: none; } }
.toggle-bar {
  display: block;
  width: 22px; height: 2px;
  background: #374151;
  border-radius: 2px;
}
</style>