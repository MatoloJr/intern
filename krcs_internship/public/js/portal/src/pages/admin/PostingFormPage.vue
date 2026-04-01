<template>
  <div>
    <h1 class="page-title">{{ isEdit ? "Edit Posting" : "New Posting" }}</h1>

    <div v-if="loadingForm" class="loading-msg">Loading…</div>
    <form v-else @submit.prevent="handleSubmit" class="form-card">

      <div class="form-group">
        <label>Title *</label>
        <input v-model="form.title" required placeholder="e.g. IT Systems Support Intern" />
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Department *</label>
          <select v-model="form.department" required>
            <option value="">— Select Department —</option>
            <option v-for="d in departmentOptions" :key="d" :value="d">{{ d }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>Location</label>
          <select v-model="form.location">
            <option v-for="l in LOCATIONS" :key="l" :value="l">{{ l }}</option>
          </select>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Duration</label>
          <select v-model="form.duration">
            <option>1 month</option>
            <option>3 months</option>
            <option>6 months</option>
            <option>1 year</option>
          </select>
        </div>
        <div class="form-group">
          <label>Positions</label>
          <input v-model.number="form.positions" type="number" min="1" />
        </div>
        <div class="form-group">
          <label>Deadline *</label>
          <input v-model="form.deadline" type="date" required />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Stipend Type</label>
          <select v-model="form.stipend_type">
            <option>Unpaid</option>
            <option>Paid</option>
          </select>
        </div>
        <div v-if="form.stipend_type === 'Paid'" class="form-group">
          <label>Monthly Amount (KES)</label>
          <input v-model.number="form.stipend_amount" type="number" min="0" placeholder="0" />
        </div>
        <div class="form-group">
          <label>Status</label>
          <select v-model="form.status">
            <option>Draft</option>
            <option>Published</option>
            <option>Closed</option>
          </select>
        </div>
      </div>

      <div class="form-group">
        <label>Description</label>
        <textarea v-model="form.description" rows="5" placeholder="Describe the internship role…"></textarea>
      </div>

      <!-- Responsibilities -->
      <div class="form-group">
        <label>Responsibilities <span class="hint">(one per line)</span></label>
        <div v-for="(_, i) in responsibilityLines" :key="i" class="line-input">
          <input v-model="responsibilityLines[i]" :placeholder="'Responsibility ' + (i + 1)" />
          <button type="button" @click="responsibilityLines.splice(i, 1)" v-if="responsibilityLines.length > 1">✕</button>
        </div>
        <button type="button" class="btn-add-line" @click="responsibilityLines.push('')">+ Add Responsibility</button>
      </div>

      <!-- Requirements -->
      <div class="form-group">
        <label>Requirements <span class="hint">(one per line)</span></label>
        <div v-for="(_, i) in requirementLines" :key="i" class="line-input">
          <input v-model="requirementLines[i]" :placeholder="'Requirement ' + (i + 1)" />
          <button type="button" @click="requirementLines.splice(i, 1)" v-if="requirementLines.length > 1">✕</button>
        </div>
        <button type="button" class="btn-add-line" @click="requirementLines.push('')">+ Add Requirement</button>
      </div>

      <!-- Skills -->
      <div class="form-group">
        <label>Skills / Keywords</label>
        <div class="skills-input-row">
          <input v-model="skillInput" placeholder="Add a skill…" @keydown.enter.prevent="addSkill" />
          <button type="button" @click="addSkill">Add</button>
        </div>
        <div class="skills-tags">
          <span v-for="s in skillTags" :key="s" class="skill-tag">
            {{ s }}
            <button type="button" @click="skillTags = skillTags.filter(x => x !== s)">✕</button>
          </span>
        </div>
      </div>

      <div class="form-group checkbox-row">
        <input type="checkbox" id="featured" v-model="form.featured" />
        <label for="featured" style="font-weight:400;cursor:pointer">Feature on homepage</label>
      </div>

      <div v-if="error" class="error-banner">{{ error }}</div>

      <div class="form-actions">
        <RouterLink to="/admin/postings" class="btn-cancel">Cancel</RouterLink>
        <button type="submit" class="btn-submit" :disabled="saving">
          {{ saving ? "Saving…" : (isEdit ? "Save Changes" : "Create Posting") }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useRoute, useRouter, RouterLink } from "vue-router"
import { useAdminStore } from "../../stores/admin"
import { usePostingsStore } from "../../stores/postings"

const route = useRoute()
const router = useRouter()
const admin = useAdminStore()
const store = usePostingsStore()

const isEdit = computed(() => !!route.params.id)
const saving = ref(false)
const loadingForm = ref(false)
const error = ref("")
const departmentOptions = ref([])

const LOCATIONS = ["Nairobi", "Mombasa", "Kisumu", "Eldoret", "Nakuru", "Remote"]

// Department options from the Internship Posting Select field
const DEPT_SELECT_OPTIONS = [
  "PROGRAM", "HR", "AUDIT & RISK", "PROCUREMENT", "FINANCE",
  "GLOBAL FUND", "ICHA", "NSD", "IT", "PR",
  "LEGAL", "TRAINING SCHOOL", "SECURITY", "COMPLIANCE"
]

const form = ref({
  title: "", department: "", location: "Nairobi",
  duration: "3 months", positions: 1, deadline: "",
  stipend_type: "Unpaid", stipend_amount: 0,
  description: "", status: "Draft", featured: false
})

const responsibilityLines = ref([""])
const requirementLines = ref([""])
const skillTags = ref([])
const skillInput = ref("")

function addSkill() {
  const s = skillInput.value.trim()
  if (s && !skillTags.value.includes(s)) skillTags.value.push(s)
  skillInput.value = ""
}

async function handleSubmit() {
  saving.value = true
  error.value = ""
  try {
    const payload = {
      ...form.value,
      featured: form.value.featured ? 1 : 0,
      responsibilities: responsibilityLines.value.filter(Boolean).join("\n"),
      requirements: requirementLines.value.filter(Boolean).join("\n"),
      skills: skillTags.value.join("\n"),
    }
    if (isEdit.value) {
      await admin.updatePosting(route.params.id, payload)
    } else {
      await admin.createPosting(payload)
    }
    router.push("/admin/postings")
  } catch (e) {
    error.value = e.message || "Save failed. Please check all required fields."
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  loadingForm.value = true
  try {
    // Try to get live departments from DB; fall back to the Select options
    const depts = await store.fetchDepartments()
    if (depts && depts.length > 0) {
      departmentOptions.value = depts.map((d) => d.department || d.name)
    } else {
      departmentOptions.value = DEPT_SELECT_OPTIONS
    }
  } catch (_) {
    departmentOptions.value = DEPT_SELECT_OPTIONS
  }

  if (isEdit.value) {
    try {
      const posting = await store.fetchPosting(route.params.id)
      if (posting) {
        Object.assign(form.value, {
          title: posting.title || "",
          department: posting.department || "",
          location: posting.location || "Nairobi",
          duration: posting.duration || "3 months",
          positions: posting.positions || 1,
          deadline: posting.deadline || "",
          stipend_type: posting.stipend_type || "Unpaid",
          stipend_amount: posting.stipend_amount || 0,
          description: posting.description || "",
          status: posting.status || "Draft",
          featured: !!posting.featured,
        })
        responsibilityLines.value = posting.responsibilities_list?.length
          ? posting.responsibilities_list : [""]
        requirementLines.value = posting.requirements_list?.length
          ? posting.requirements_list : [""]
        skillTags.value = posting.skills_list || []
      }
    } catch (e) {
      error.value = "Could not load posting data: " + e.message
    }
  }
  loadingForm.value = false
})
</script>

<style scoped>
.page-title { font-size: 1.5rem; font-weight: 700; color: #111; margin: 0 0 1.5rem; }
.loading-msg { text-align: center; color: #6b7280; padding: 2rem; }
.form-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 2rem; max-width: 820px; box-shadow: 0 1px 4px rgba(0,0,0,.05); }
.form-group { margin-bottom: 1.1rem; }
.form-group label { display: block; font-size: .8rem; font-weight: 600; color: #374151; margin-bottom: .35rem; }
.hint { font-weight: 400; color: #9ca3af; font-size: .75rem; }
.form-group input, .form-group select, .form-group textarea {
  width: 100%; padding: .55rem .75rem;
  border: 1px solid #d1d5db; border-radius: 7px;
  font-size: .875rem; outline: none; font-family: inherit;
  box-sizing: border-box; resize: vertical;
}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { border-color: #cc0000; }
.form-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; }
.line-input { display: flex; gap: .4rem; margin-bottom: .4rem; }
.line-input input { flex: 1; }
.line-input button { background: none; border: 1px solid #d1d5db; border-radius: 5px; padding: 0 .55rem; cursor: pointer; color: #9ca3af; font-size: .9rem; }
.line-input button:hover { color: #ef4444; border-color: #ef4444; }
.btn-add-line { background: none; border: 1px dashed #d1d5db; border-radius: 6px; padding: .35rem .75rem; font-size: .8rem; color: #6b7280; cursor: pointer; margin-top: .2rem; }
.btn-add-line:hover { border-color: #cc0000; color: #cc0000; }
.skills-input-row { display: flex; gap: .5rem; margin-bottom: .5rem; }
.skills-input-row input { flex: 1; }
.skills-input-row button { background: #cc0000; color: #fff; border: none; border-radius: 7px; padding: .5rem .9rem; font-size: .82rem; cursor: pointer; }
.skills-tags { display: flex; flex-wrap: wrap; gap: .4rem; }
.skill-tag { background: #f3f4f6; border-radius: 20px; padding: .25rem .65rem; font-size: .78rem; font-weight: 600; color: #374151; display: flex; align-items: center; gap: .3rem; }
.skill-tag button { background: none; border: none; cursor: pointer; color: #9ca3af; padding: 0; }
.skill-tag button:hover { color: #ef4444; }
.checkbox-row { display: flex; align-items: center; gap: .5rem; flex-direction: row; }
.checkbox-row input { width: auto; }
.error-banner { background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 8px; padding: .75rem 1rem; font-size: .875rem; margin-bottom: 1rem; }
.form-actions { display: flex; gap: .75rem; margin-top: 1.5rem; }
.btn-cancel { padding: .65rem 1.25rem; border: 1px solid #d1d5db; border-radius: 8px; text-decoration: none; color: #374151; font-size: .875rem; }
.btn-submit { background: #cc0000; color: #fff; border: none; border-radius: 8px; padding: .65rem 1.5rem; font-weight: 700; font-size: .875rem; cursor: pointer; }
.btn-submit:disabled { opacity: .6; cursor: default; }
</style>