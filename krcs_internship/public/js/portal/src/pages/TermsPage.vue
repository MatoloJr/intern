<template>
  <div class="page-wrap">
    <AppNavbar />
    <div class="hero-band">
      <h1>Terms of Service</h1>
      <p>Last updated: March 1, 2026</p>
    </div>
    <div class="content">
      <p class="intro">
        Welcome to the KRCS Internship Portal. These Terms of Service govern your use
        of the platform operated by the Kenya Red Cross Society.
      </p>
      <div v-for="(section, i) in sections" :key="i" class="policy-section">
        <h2>{{ i + 1 }}. {{ section.title }}</h2>
        <div class="divider"></div>
        <p>{{ section.content }}</p>
      </div>
      <div class="contact-note">
        Questions? Email <a href="mailto:legal@redcross.or.ke">legal@redcross.or.ke</a>
      </div>
    </div>
    <AppFooter />
  </div>
</template>

<script setup>
import AppNavbar from '../components/AppNavbar.vue'
import AppFooter from '../components/AppFooter.vue'

const sections = [
  { title: 'Acceptance of Terms', content: 'By accessing or using the KRCS Internship Portal, you agree to be bound by these Terms of Service. If you do not agree, you may not use the platform.' },
  { title: 'Eligibility', content: 'The platform is available to students currently enrolled in accredited universities and colleges in Kenya, or recent graduates within 2 years of graduation. You must be at least 18 years old to create an account.' },
  { title: 'User Accounts', content: 'You are responsible for maintaining the confidentiality of your account credentials and must provide accurate information during registration. KRCS reserves the right to suspend accounts that violate these terms.' },
  { title: 'Application Process', content: 'Submitting an application does not guarantee placement. KRCS reserves the right to accept or reject applications at its sole discretion. All application materials may be retained for future consideration.' },
  { title: 'Intellectual Property', content: 'All content on the platform, including logos, text and graphics, is the property of KRCS or its licensors. You may not reproduce or distribute content without prior written consent.' },
  { title: 'User Conduct', content: 'You agree not to submit fraudulent information, attempt to access other users\' accounts, use the platform for any illegal purpose, or upload malicious files.' },
  { title: 'Limitation of Liability', content: 'KRCS shall not be liable for any indirect, incidental or consequential damages arising from your use of the platform. The platform is provided "as is" without warranties of any kind.' },
  { title: 'Governing Law', content: 'These terms shall be governed by the laws of the Republic of Kenya. Any disputes shall be resolved through arbitration in Nairobi, Kenya.' },
]
</script>

<style scoped>
.page-wrap { display: flex; flex-direction: column; min-height: 100vh; }
.hero-band { background: #cc0000; color: #fff; padding: 3.5rem 1.25rem; text-align: center; }
.hero-band h1 { font-size: clamp(1.5rem, 3vw, 2rem); font-weight: 800; margin: 0 0 .5rem; }
.hero-band p { font-size: .9rem; opacity: .8; }
.content { max-width: 780px; margin: 0 auto; padding: 3rem 1.25rem; }
.intro { font-size: .9rem; color: #374151; line-height: 1.7; margin-bottom: 2.5rem; }
.policy-section { margin-bottom: 2rem; }
.policy-section h2 { font-size: 1.05rem; font-weight: 700; color: #111; margin: 0; }
.divider { width: 32px; height: 2px; background: #cc0000; border-radius: 2px; margin: .4rem 0 .75rem; }
.policy-section p { font-size: .87rem; color: #374151; line-height: 1.7; margin: 0; }
.contact-note { background: #f9fafb; border-radius: 8px; padding: 1.25rem; text-align: center; font-size: .85rem; color: #6b7280; margin-top: 2rem; }
.contact-note a { color: #cc0000; text-decoration: none; font-weight: 600; }
</style>