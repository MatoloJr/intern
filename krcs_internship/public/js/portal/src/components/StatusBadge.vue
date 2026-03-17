<template>
  <span :class="['status-badge', statusClass]">{{ status }}</span>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ status: String })
const statusClass = computed(() => {
  const map = {
    'Pending': 'status-pending',
    'Under Review': 'status-review',
    'Shortlisted': 'status-shortlisted',
    'Accepted': 'status-accepted',
    'Rejected': 'status-rejected',
    'Published': 'status-published',
    'Draft': 'status-draft',
    'Closed': 'status-closed'
  }
  return map[props.status] || 'status-default'
})
</script>

<style scoped>
.status-badge {
  display: inline-block;
  font-size: .72rem;
  font-weight: 600;
  padding: .25rem .7rem;
  border-radius: 20px;
}
.status-pending    { background: #fef3c7; color: #92400e; }
.status-review     { background: #dbeafe; color: #1e40af; }
.status-shortlisted{ background: #d1fae5; color: #065f46; }
.status-accepted   { background: #d1fae5; color: #065f46; }
.status-rejected   { background: #fee2e2; color: #991b1b; }
.status-published  { background: #d1fae5; color: #065f46; }
.status-draft      { background: #f3f4f6; color: #6b7280; }
.status-closed     { background: #fee2e2; color: #991b1b; }
.status-default    { background: #f3f4f6; color: #374151; }
</style>