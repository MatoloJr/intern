<template>
  <div class="admin-wrap">
    <!-- Top bar -->
    <header class="admin-topbar">
      <div class="topbar-left">
        <button class="sidebar-toggle" @click="sidebarOpen = !sidebarOpen">☰</button>
        <RouterLink to="/" class="topbar-brand">
          <img :src="logo" alt="KRCS" />
          <span>KRCS Admin</span>
        </RouterLink>
      </div>
      <div class="topbar-right">
        <span class="admin-user">{{ user }}</span>
        <a href="/logout" class="btn-logout">Log out</a>
      </div>
    </header>

    <div class="admin-body">
      <!-- Sidebar -->
      <aside :class="['admin-sidebar', sidebarOpen ? 'open' : '']">
        <nav>
          <RouterLink
            v-for="item in navItems"
            :key="item.to"
            :to="item.to"
            class="nav-item"
            active-class="nav-item-active"
            @click="sidebarOpen = false"
          >
            <span class="nav-icon">{{ item.icon }}</span>
            <span>{{ item.label }}</span>
          </RouterLink>
        </nav>
      </aside>

      <!-- Overlay for mobile -->
      <div
        v-if="sidebarOpen"
        class="sidebar-overlay"
        @click="sidebarOpen = false"
      ></div>

      <!-- Main content -->
      <main class="admin-main">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

const logo = '/assets/krcs_internship/images/krcs-logo.png'

const sidebarOpen = ref(false)
const user = window.frappe?.session?.user || 'Admin'

const navItems = [
  { to: '/admin/dashboard',    icon: '📊', label: 'Dashboard' },
  { to: '/admin/postings',     icon: '📋', label: 'Manage Postings' },
  { to: '/admin/postings/new', icon: '➕', label: 'New Posting' },
  { to: '/admin/applications', icon: '📁', label: 'Applications' },
  { to: '/admin/messages',     icon: '✉️', label: 'Messages' },
  { to: '/admin/reports',      icon: '📈', label: 'Reports' },
]
</script>

<style scoped>
.admin-wrap { display: flex; flex-direction: column; min-height: 100vh; }
.admin-topbar {
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.25rem;
  position: sticky;
  top: 0;
  z-index: 100;
}
.topbar-left { display: flex; align-items: center; gap: .75rem; }
.sidebar-toggle {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #374151;
  padding: .2rem;
}
@media (min-width: 1024px) { .sidebar-toggle { display: none; } }
.topbar-brand { display: flex; align-items: center; gap: .5rem; text-decoration: none; font-weight: 700; color: #111; font-size: .95rem; }
.topbar-brand img { height: 32px; width: 32px; object-fit: contain; }
.topbar-right { display: flex; align-items: center; gap: 1rem; }
.admin-user { font-size: .82rem; color: #6b7280; }
.btn-logout { font-size: .82rem; color: #cc0000; text-decoration: none; font-weight: 600; }
.admin-body { display: flex; flex: 1; overflow: hidden; }
.admin-sidebar {
  width: 220px;
  background: #7a0000;
  padding: 1.25rem 0;
  flex-shrink: 0;
  position: fixed;
  top: 60px;
  bottom: 0;
  left: 0;
  z-index: 90;
  transform: translateX(-100%);
  transition: transform .25s;
}
.admin-sidebar {
  width: 220px;
  background: #7a0000;
  padding: 1.25rem 0;
  flex-shrink: 0;
  position: fixed;
  top: 60px;
  bottom: 0;
  left: 0;
  z-index: 90;
  transform: translateX(-100%);
  transition: transform .25s;
}
.admin-sidebar.open {
  transform: translateX(0);
}
@media (min-width: 1024px) {
  .admin-sidebar {
    position: sticky;
    transform: translateX(0);
  }
}
@media (min-width: 1024px) {
  .admin-sidebar { position: sticky; transform: translateX(0); }
}
.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.3);
  z-index: 89;
}
@media (min-width: 1024px) { .sidebar-overlay { display: none; } }
.nav-item {
  display: flex;
  align-items: center;
  gap: .7rem;
  padding: .7rem 1.25rem;
  text-decoration: none;
  color: rgba(255,255,255,.75);
  font-size: .875rem;
  font-weight: 500;
  transition: background .15s, color .15s;
}
.nav-item:hover { background: rgba(255,255,255,.1); color: #fff; }
.nav-item-active { background: rgba(255,255,255,.15); color: #fff; }
.nav-icon { font-size: 1rem; }
.admin-main {
  flex: 1;
  padding: 2rem 1.5rem;
  overflow-y: auto;
  margin-left: 0;
}
@media (min-width: 1024px) { .admin-main { margin-left: 220px; } }
</style>