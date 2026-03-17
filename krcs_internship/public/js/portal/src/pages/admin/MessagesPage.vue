<template>
  <div class="messages-layout">
    <!-- Inbox list -->
    <div class="inbox">
      <div class="inbox-header">
        <h2>Inbox</h2>
        <button class="btn-compose" @click="composeOpen = true">+ Compose</button>
      </div>
      <div class="loading-msg" v-if="loading">Loading…</div>
      <div v-else class="message-list">
        <div
          v-for="m in store.messages"
          :key="m.name"
          :class="['msg-row', selected?.name === m.name ? 'msg-row-active' : '', !m.read ? 'msg-unread' : '']"
          @click="openMessage(m)"
        >
          <div class="msg-subject">{{ m.subject }}</div>
          <div class="msg-to">To: {{ m.to_email }}</div>
          <div class="msg-date">{{ formatDate(m.sent_date) }}</div>
        </div>
        <div v-if="!store.messages.length" class="empty-msg">No messages yet.</div>
      </div>
    </div>

    <!-- Message detail -->
    <div class="msg-detail">
      <div v-if="!selected" class="no-selection">Select a message to view it</div>
      <template v-else>
        <h2>{{ selected.subject }}</h2>
        <div class="msg-meta">
          <span>To: {{ selected.to_email }}</span>
          <span>{{ formatDate(selected.sent_date) }}</span>
        </div>
        <div class="msg-body" v-html="selected.body"></div>
      </template>
    </div>

    <!-- Compose modal -->
    <div v-if="composeOpen" class="modal-overlay" @click.self="composeOpen = false">
      <div class="modal">
        <h3>Compose Message</h3>
        <div class="form-group">
          <label>To (email)</label>
          <input v-model="compose.to_email" type="email" />
        </div>
        <div class="form-group">
          <label>Subject</label>
          <input v-model="compose.subject" />
        </div>
        <div class="form-group">
          <label>Message</label>
          <textarea v-model="compose.body" rows="6"></textarea>
        </div>
        <div class="modal-actions">
          <button @click="composeOpen = false" class="btn-cancel">Cancel</button>
          <button @click="sendCompose" class="btn-send" :disabled="sending">
            {{ sending ? 'Sending…' : 'Send' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMessagesStore } from '../../stores/messages'

const store = useMessagesStore()
const selected = ref(null)
const loading = ref(true)
const composeOpen = ref(false)
const sending = ref(false)
const compose = ref({ to_email: '', subject: '', body: '' })

function formatDate(d) {
  return d ? new Date(d).toLocaleString('en-KE', { dateStyle: 'medium', timeStyle: 'short' }) : ''
}

async function openMessage(m) {
  selected.value = m
  if (!m.read) await store.markRead(m.name)
}

async function sendCompose() {
  sending.value = true
  await store.adminSend(compose.value.to_email, compose.value.subject, compose.value.body)
  composeOpen.value = false
  sending.value = false
  compose.value = { to_email: '', subject: '', body: '' }
  await store.fetchMessages('')
}

onMounted(async () => {
  // Admin sees all messages — pass empty string as sentinel
  await store.fetchMessages('')
  loading.value = false
})
</script>

<style scoped>
.messages-layout { display: grid; grid-template-columns: 320px 1fr; gap: 1.25rem; height: calc(100vh - 140px); }
@media (max-width: 768px) { .messages-layout { grid-template-columns: 1fr; height: auto; } }
.inbox { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; overflow: hidden; display: flex; flex-direction: column; }
.inbox-header { display: flex; justify-content: space-between; align-items: center; padding: .85rem 1rem; border-bottom: 1px solid #e5e7eb; }
.inbox-header h2 { font-size: .95rem; font-weight: 700; margin: 0; color: #111; }
.btn-compose { background: #cc0000; color: #fff; border: none; border-radius: 6px; padding: .35rem .75rem; font-size: .8rem; cursor: pointer; font-weight: 600; }
.message-list { overflow-y: auto; flex: 1; }
.msg-row { padding: .75rem 1rem; border-bottom: 1px solid #f3f4f6; cursor: pointer; transition: background .1s; }
.msg-row:hover { background: #fef2f2; }
.msg-row-active { background: #fef2f2; border-left: 3px solid #cc0000; }
.msg-unread .msg-subject { font-weight: 700; color: #111; }
.msg-subject { font-size: .85rem; color: #374151; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.msg-to { font-size: .75rem; color: #9ca3af; margin-top: .15rem; }
.msg-date { font-size: .72rem; color: #9ca3af; }
.empty-msg { text-align: center; color: #9ca3af; padding: 2rem; font-size: .85rem; }
.loading-msg { text-align: center; color: #6b7280; padding: 1.5rem; font-size: .85rem; }
.msg-detail { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 1.5rem; overflow-y: auto; }
.no-selection { display: flex; align-items: center; justify-content: center; height: 200px; color: #9ca3af; font-size: .875rem; }
.msg-detail h2 { font-size: 1.1rem; font-weight: 700; color: #111; margin: 0 0 .5rem; }
.msg-meta { display: flex; gap: 1.5rem; font-size: .78rem; color: #9ca3af; margin-bottom: 1.25rem; padding-bottom: .75rem; border-bottom: 1px solid #e5e7eb; }
.msg-body { font-size: .875rem; color: #374151; line-height: 1.7; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.4); z-index: 200; display: flex; align-items: center; justify-content: center; }
.modal { background: #fff; border-radius: 12px; padding: 2rem; max-width: 500px; width: 90%; }
.modal h3 { margin: 0 0 1rem; font-size: 1.05rem; }
.form-group { margin-bottom: .85rem; }
.form-group label { display: block; font-size: .8rem; font-weight: 600; color: #374151; margin-bottom: .3rem; }
.form-group input, .form-group textarea { width: 100%; padding: .5rem .7rem; border: 1px solid #d1d5db; border-radius: 7px; font-size: .875rem; outline: none; font-family: inherit; box-sizing: border-box; resize: vertical; }
.modal-actions { display: flex; gap: .6rem; justify-content: flex-end; margin-top: 1rem; }
.btn-cancel { padding: .55rem 1rem; border: 1px solid #d1d5db; border-radius: 7px; background: #fff; cursor: pointer; font-size: .85rem; }
.btn-send { padding: .55rem 1.1rem; background: #cc0000; color: #fff; border: none; border-radius: 7px; cursor: pointer; font-weight: 600; font-size: .85rem; }
.btn-send:disabled { opacity: .6; cursor: default; }
</style>