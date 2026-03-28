// krcs_internship/public/js/portal/src/router/index.js
import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { path: '/',
    component: () => import('../pages/HomePage.vue') },
  { path: '/login',
    component: () => import('../pages/LoginPage.vue') },
  { path: '/student-dashboard',
    component: () => import('../pages/StudentDashboardPage.vue') },
  { path: '/internships',
    component: () => import('../pages/InternshipsPage.vue') },
  { path: '/internships/:id',
    component: () => import('../pages/InternshipDetailPage.vue') },
  { path: '/internships/:id/apply',
    component: () => import('../pages/ApplyPage.vue') },
  { path: '/track',
    component: () => import('../pages/TrackApplicationPage.vue') },
  { path: '/about',
    component: () => import('../pages/AboutPage.vue') },
  { path: '/contact',
    component: () => import('../pages/ContactPage.vue') },
  { path: '/privacy',
    component: () => import('../pages/PrivacyPage.vue') },
  { path: '/terms',
    component: () => import('../pages/TermsPage.vue') },
  {
    path: '/admin',
    component: () => import('../layouts/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/admin/dashboard' },
      { path: 'dashboard', component: () => import('../pages/admin/DashboardPage.vue') },
      { path: 'postings', component: () => import('../pages/admin/PostingsPage.vue') },
      { path: 'postings/new', component: () => import('../pages/admin/PostingFormPage.vue') },
      { path: 'postings/:id/edit', component: () => import('../pages/admin/PostingFormPage.vue') },
      { path: 'applications', component: () => import('../pages/admin/ApplicationsPage.vue') },
      { path: 'reports', component: () => import('../pages/admin/ReportsPage.vue') },
      { path: 'messages', component: () => import('../pages/admin/MessagesPage.vue') },
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const user = window.frappe?.session?.user
    if (!user || user === 'Guest') {
      return { path: '/login' }
    }
  }
})

export default router