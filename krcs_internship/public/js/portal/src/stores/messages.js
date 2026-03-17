import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { frappeCall } from '../lib/frappe'

export const useMessagesStore = defineStore('messages', () => {
  const messages = ref([])

  const unreadCount = computed(
    () => messages.value.filter(m => !m.read).length
  )

  async function fetchMessages(email) {
    const res = await frappeCall(
      'krcs_internship.krcs_internship.api.get_messages',
      { email }
    )
    messages.value = res.message || []
  }

  async function markRead(name) {
    await frappeCall(
      'krcs_internship.krcs_internship.api.mark_message_read',
      { name }
    )
    const msg = messages.value.find(m => m.name === name)
    if (msg) msg.read = 1
  }

  async function adminSend(to_email, subject, body, application = null) {
    return frappeCall(
      'krcs_internship.krcs_internship.api.admin_send_message',
      { to_email, subject, body, application }
    )
  }

  return { messages, unreadCount, fetchMessages, markRead, adminSend }
})