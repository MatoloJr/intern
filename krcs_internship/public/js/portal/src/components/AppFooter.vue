<template>
  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-col">
        <div class="footer-brand">
          <img :src="logo" alt="KRCS" />
          <span>KRCS Internship Portal</span>
        </div>
        <p>Empowering the next generation of humanitarian leaders.</p>
      </div>
      <div class="footer-col">
        <h4>Quick Links</h4>
        <RouterLink to="/internships">Browse Internships</RouterLink>
        <RouterLink to="/track">Track Application</RouterLink>
      </div>
      <div class="footer-col">
        <h4>About</h4>
        <RouterLink to="/about">About KRCS</RouterLink>
        <RouterLink to="/contact">Contact</RouterLink>
        <RouterLink to="/privacy">Privacy Policy</RouterLink>
        <RouterLink to="/terms">Terms of Service</RouterLink>
      </div>
      <div class="footer-col">
        <h4>Contact</h4>
        <p>internships@redcross.or.ke</p>
        <p>+254 20 3950000</p>
        <p>Mon–Fri 8:00 AM – 5:00 PM</p>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© {{ year }} Kenya Red Cross Society. All rights reserved.</p>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from 'vue-router'

import logoUrl from '../assets/krcs-logo.png'
const logo = logoUrl
const year = new Date().getFullYear()
</script>

<style scoped>
.footer {
  background: #7a0000;
  color: #fde8e8;
  margin-top: auto;
}
.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 1.25rem 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 2rem;
}
.footer-brand {
  display: flex;
  align-items: center;
  gap: .6rem;
  font-weight: 700;
  font-size: 1rem;
  margin-bottom: .75rem;
}
.footer-brand img { height: 32px; width: 32px; object-fit: contain; }
.footer-col p { font-size: .85rem; opacity: .8; line-height: 1.6; margin: .2rem 0; }
.footer-col h4 { font-size: .9rem; font-weight: 600; margin-bottom: .75rem; color: #fff; }
.footer-col a {
  display: block;
  color: #fde8e8;
  text-decoration: none;
  font-size: .85rem;
  opacity: .8;
  margin-bottom: .35rem;
  transition: opacity .15s;
}
.footer-col a:hover { opacity: 1; }
.footer-bottom {
  border-top: 1px solid rgba(255,255,255,.15);
  text-align: center;
  padding: 1rem;
  font-size: .8rem;
  opacity: .6;
}
</style>