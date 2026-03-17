<template>
  <div class="page-wrap">
    <AppNavbar />
    <div class="hero-band">
      <h1>Contact Us</h1>
      <p>Have questions about the internship programme? We'd love to hear from you.</p>
    </div>

    <div class="content">
      <div class="two-col">
        <!-- Contact info -->
        <div>
          <h2>Get In Touch</h2>
          <div class="divider"></div>
          <div class="contact-items">
            <div v-for="item in contactItems" :key="item.label" class="contact-item">
              <span class="contact-icon">{{ item.icon }}</span>
              <div>
                <strong>{{ item.label }}</strong>
                <p v-for="line in item.lines" :key="line">{{ line }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Form -->
        <div class="form-card">
          <h2>Send a Message</h2>
          <div class="divider"></div>
          <form @submit.prevent="handleSubmit">
            <div class="form-row">
              <div class="form-group">
                <label>Name *</label>
                <input v-model="form.name" required />
              </div>
              <div class="form-group">
                <label>Email *</label>
                <input v-model="form.email" type="email" required />
              </div>
            </div>
            <div class="form-group">
              <label>Subject</label>
              <input v-model="form.subject" />
            </div>
            <div class="form-group">
              <label>Message *</label>
              <textarea v-model="form.message" rows="5" required></textarea>
            </div>
            <button type="submit" class="btn-submit" :disabled="sent">
              {{ sent ? '✓ Message Sent!' : 'Send Message' }}
            </button>
          </form>
        </div>
      </div>
    </div>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppNavbar from '../components/AppNavbar.vue'
import AppFooter from '../components/AppFooter.vue'

const sent = ref(false)
const form = ref({ name: '', email: '', subject: '', message: '' })

const contactItems = [
  { icon: '📍', label: 'Address', lines: ['KRCS Headquarters, South C', 'Bellevue, off Mombasa Road', 'P.O. Box 40712-00100, Nairobi'] },
  { icon: '📞', label: 'Phone', lines: ['+254 20 3950000', '+254 703 037000'] },
  { icon: '✉️', label: 'Email', lines: ['internships@redcross.or.ke'] },
  { icon: '🕐', label: 'Working Hours', lines: ['Mon–Fri: 8:00 AM – 5:00 PM', 'Saturday: 9:00 AM – 1:00 PM'] },
]

function handleSubmit() {
  sent.value = true
  form.value = { name: '', email: '', subject: '', message: '' }
  setTimeout(() => { sent.value = false }, 4000)
}
</script>

<style scoped>
.page-wrap { display: flex; flex-direction: column; min-height: 100vh; }
.hero-band { background: #cc0000; color: #fff; padding: 4rem 1.25rem; text-align: center; }
.hero-band h1 { font-size: clamp(1.5rem, 3vw, 2.25rem); font-weight: 800; margin: 0 0 .75rem; }
.hero-band p { font-size: .95rem; opacity: .9; }
.content { max-width: 1100px; margin: 0 auto; padding: 3rem 1.25rem; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; }
@media (max-width: 768px) { .two-col { grid-template-columns: 1fr; } }
h2 { font-size: 1.35rem; font-weight: 700; color: #111; margin: 0; }
.divider { width: 40px; height: 3px; background: #cc0000; border-radius: 2px; margin: .5rem 0 1.5rem; }
.contact-items { display: flex; flex-direction: column; gap: 1rem; }
.contact-item { display: flex; gap: 1rem; background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 1rem; }
.contact-icon { font-size: 1.25rem; flex-shrink: 0; }
.contact-item strong { display: block; font-size: .85rem; font-weight: 700; color: #111; margin-bottom: .3rem; }
.contact-item p { font-size: .82rem; color: #6b7280; margin: .1rem 0; }
.form-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 2rem; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
@media (max-width: 480px) { .form-row { grid-template-columns: 1fr; } }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; font-size: .8rem; font-weight: 600; color: #374151; margin-bottom: .35rem; }
.form-group input, .form-group textarea {
  width: 100%;
  padding: .55rem .75rem;
  border: 1px solid #d1d5db;
  border-radius: 7px;
  font-size: .875rem;
  outline: none;
  font-family: inherit;
  resize: vertical;
  box-sizing: border-box;
}
.form-group input:focus, .form-group textarea:focus { border-color: #cc0000; }
.btn-submit {
  width: 100%;
  background: #cc0000;
  color: #fff;
  border: none;
  padding: .75rem;
  border-radius: 8px;
  font-weight: 700;
  font-size: .9rem;
  cursor: pointer;
  transition: background .15s;
}
.btn-submit:hover:not(:disabled) { background: #a30000; }
.btn-submit:disabled { opacity: .7; cursor: default; }
</style>