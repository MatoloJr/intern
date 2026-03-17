<template>
  <div class="card" @click="$router.push('/internships/' + posting.name)">
    <div class="card-top-bar"></div>
    <div class="card-body">
      <div class="card-header">
        <span class="badge badge-dept">{{ posting.department || '—' }}</span>
        <span :class="['badge', posting.stipend_type === 'Paid' ? 'badge-paid' : 'badge-unpaid']">
          {{ posting.stipend_type === 'Paid'
              ? 'KES ' + Number(posting.stipend_amount).toLocaleString()
              : 'Unpaid' }}
        </span>
      </div>
      <h3 class="card-title">{{ posting.title }}</h3>
      <p class="card-desc">{{ truncate(posting.description) }}</p>
      <div class="card-meta">
        <span>📍 {{ posting.location }}</span>
        <span>⏱ {{ posting.duration }}</span>
        <span>👥 {{ posting.positions }} position{{ posting.positions > 1 ? 's' : '' }}</span>
      </div>
      <div class="card-footer">
        <span :class="['deadline', urgent ? 'urgent' : '']">
          📅 {{ daysLeft > 0 ? daysLeft + ' days left' : 'Closed' }}
        </span>
        <button class="btn-view">View Details</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({ posting: Object })
const router = useRouter()

const daysLeft = computed(() => {
  if (!props.posting.deadline) return 0
  const diff = new Date(props.posting.deadline) - new Date()
  return Math.ceil(diff / 86400000)
})
const urgent = computed(() => daysLeft.value > 0 && daysLeft.value <= 7)

function truncate(text, len = 110) {
  if (!text) return ''
  const plain = text.replace(/<[^>]+>/g, '')
  return plain.length > len ? plain.slice(0, len) + '…' : plain
}
</script>

<style scoped>
.card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow .2s, border-color .2s;
}
.card:hover { box-shadow: 0 4px 16px rgba(0,0,0,.1); border-color: rgba(204,0,0,.3); }
.card-top-bar { height: 4px; background: #cc0000; }
.card-body { padding: 1.1rem; }
.card-header { display: flex; justify-content: space-between; margin-bottom: .75rem; flex-wrap: wrap; gap: .4rem; }
.badge {
  font-size: .72rem;
  font-weight: 600;
  padding: .25rem .65rem;
  border-radius: 20px;
}
.badge-dept { background: #f3f4f6; color: #374151; }
.badge-paid { background: #fef3c7; color: #92400e; }
.badge-unpaid { background: #f3f4f6; color: #6b7280; }
.card-title { font-size: 1.05rem; font-weight: 700; color: #111; margin: 0 0 .5rem; }
.card-desc { font-size: .82rem; color: #6b7280; line-height: 1.5; margin: 0 0 .85rem; }
.card-meta { display: flex; flex-wrap: wrap; gap: .75rem; font-size: .78rem; color: #6b7280; margin-bottom: .85rem; }
.card-footer { display: flex; justify-content: space-between; align-items: center; }
.deadline { font-size: .78rem; color: #6b7280; }
.deadline.urgent { color: #cc0000; font-weight: 600; }
.btn-view {
  background: #cc0000;
  color: #fff;
  border: none;
  padding: .4rem .9rem;
  border-radius: 8px;
  font-size: .82rem;
  font-weight: 600;
  cursor: pointer;
  transition: background .15s;
}
.btn-view:hover { background: #a30000; }
</style>