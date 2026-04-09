import { createRouter, createWebHashHistory } from 'vue-router'

// ALL imports must be static/eager when building as IIFE.
// Dynamic imports (() => import('...')) create separate ES module chunks
// that contain bare "export" statements, which cause:
// "Uncaught SyntaxError: Unexpected token 'export'"
// when portal.js is loaded as a plain <script> (not type="module")
import HomePage from '../pages/HomePage.vue'
import LoginPage from '../pages/LoginPage.vue'
import StudentDashboardPage from '../pages/StudentDashboardPage.vue'
import InternshipsPage from '../pages/InternshipsPage.vue'
import InternshipDetailPage from '../pages/InternshipDetailPage.vue'
import ApplyPage from '../pages/ApplyPage.vue'
import TrackApplicationPage from '../pages/TrackApplicationPage.vue'
import AboutPage from '../pages/AboutPage.vue'
import ContactPage from '../pages/ContactPage.vue'
import PrivacyPage from '../pages/PrivacyPage.vue'
import TermsPage from '../pages/TermsPage.vue'
import AdminLayout from '../layouts/AdminLayout.vue'
import DashboardPage from '../pages/admin/DashboardPage.vue'
import PostingsPage from '../pages/admin/PostingsPage.vue'
import PostingFormPage from '../pages/admin/PostingFormPage.vue'
import ApplicationsPage from '../pages/admin/ApplicationsPage.vue'
import ReportsPage from '../pages/admin/ReportsPage.vue'
import MessagesPage from '../pages/admin/MessagesPage.vue'

const routes = [
	{ path: '/',                       component: HomePage },
	{ path: '/login',                  component: LoginPage },
	{ path: '/student-dashboard',      component: StudentDashboardPage },
	{ path: '/internships',            component: InternshipsPage },
	{ path: '/internships/:id',        component: InternshipDetailPage },
	{ path: '/internships/:id/apply',  component: ApplyPage },
	{ path: '/track',                  component: TrackApplicationPage },
	{ path: '/about',                  component: AboutPage },
	{ path: '/contact',                component: ContactPage },
	{ path: '/privacy',                component: PrivacyPage },
	{ path: '/terms',                  component: TermsPage },
	{
		path: '/admin',
		component: AdminLayout,
		meta: { requiresAuth: true },
		children: [
			{ path: '',                redirect: '/admin/dashboard' },
			{ path: 'dashboard',       component: DashboardPage },
			{ path: 'postings',        component: PostingsPage },
			{ path: 'postings/new',    component: PostingFormPage },
			{ path: 'postings/:id/edit', component: PostingFormPage },
			{ path: 'applications',    component: ApplicationsPage },
			{ path: 'reports',         component: ReportsPage },
			{ path: 'messages',        component: MessagesPage },
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