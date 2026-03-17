<template>
  <div class="page-wrap">
    <AppNavbar />
    <div class="hero-band">
      <h1>Privacy Policy</h1>
      <p>Last updated: March 1, 2026</p>
    </div>
    <div class="content">
      <p class="intro">
        Kenya Red Cross Society ("KRCS") is committed to protecting your personal information.
        This policy explains how we collect, use and safeguard data through the KRCS Internship Portal.
      </p>
      <div v-for="(section, i) in sections" :key="i" class="policy-section">
        <h2>{{ i + 1 }}. {{ section.title }}</h2>
        <div class="divider"></div>
        <p>{{ section.content }}</p>
      </div>
      <div class="contact-note">
        Questions? Email us at
        <a href="mailto:privacy@redcross.or.ke">privacy@redcross.or.ke</a>
      </div>
    </div>
    <AppFooter />
  </div>
</template>

<script setup>
import AppNavbar from '../components/AppNavbar.vue'
import AppFooter from '../components/AppFooter.vue'

const sections = [
  { title: 'Information We Collect', content: 'We collect personal information you provide when registering, including your full name, email, phone number, university details, course of study and uploaded documents such as CVs and cover letters. We also collect usage data like IP addresses and pages visited.' },
  { title: 'How We Use Your Information', content: 'Your information is used to process internship applications, match you with suitable opportunities, communicate application status updates, improve our platform and comply with legal obligations. We do not sell your personal data to third parties.' },
  { title: 'Data Security', content: 'We implement industry-standard security measures including encryption, secure servers and access controls. However, no method of electronic transmission is 100% secure.' },
  { title: 'Data Retention', content: 'We retain your personal information for as long as necessary to fulfil the purposes outlined in this policy, typically for the duration of the internship cycle plus one year. You may request deletion at any time.' },
  { title: 'Your Rights', content: 'You have the right to access, correct or delete your personal data, object to processing, and receive a portable copy of your data. Contact us at privacy@redcross.or.ke to exercise these rights.' },
  { title: 'Cookies', content: 'Our platform uses cookies to enhance your experience and analyse site traffic. You can control cookie preferences through your browser settings.' },
  { title: 'Changes to This Policy', content: 'We may update this policy from time to time. We will notify you of significant changes via email or a prominent notice on our platform.' },
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