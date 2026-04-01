<template>
  <div class="app-form-wrap">
    <!-- Success screen -->
    <div v-if="submitted" class="success-screen card">
      <div class="success-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="hsl(145,63%,42%)" stroke-width="2">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
          <polyline points="22 4 12 14.01 9 11.01"/>
        </svg>
      </div>
      <h2>Application Submitted!</h2>
      <p>Reference: <strong>{{ refNumber }}</strong></p>
      <p>We'll update you at <strong>{{ form.email }}</strong></p>
      <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;margin-top:1.5rem">
        <RouterLink to="/track" class="btn btn-primary">Track My Application</RouterLink>
        <button class="btn btn-outline" @click="reset">Submit Another</button>
      </div>
    </div>

    <template v-else>
      <!-- Step indicator -->
      <div class="step-row">
        <template v-for="(s, i) in steps" :key="s">
          <div class="step-item">
            <div :class="['step-circle',
              i < currentStep ? 'step-done' :
              i === currentStep ? 'step-active' : 'step-idle']">
              <svg v-if="i < currentStep" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              <span v-else>{{ i + 1 }}</span>
            </div>
            <span class="step-label">{{ s }}</span>
          </div>
          <div v-if="i < steps.length - 1" class="step-line">
            <div class="step-line-fill" :style="{ width: i < currentStep ? '100%' : '0' }"></div>
          </div>
        </template>
      </div>

      <div class="card form-card">

        <!-- Step 1: Personal -->
        <div v-if="currentStep === 0" class="form-step">
          <div class="step-head">
            <div class="step-icon-box">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </div>
            <div>
              <h3 class="step-title">Personal Information</h3>
              <p class="step-desc">Tell us about yourself</p>
            </div>
          </div>
          <div class="form-grid">
            <div class="form-group span-2">
              <label class="form-label">Full Name *</label>
              <input v-model="form.fullName" class="form-input" placeholder="John Kamau Mwangi" />
              <p v-if="errors.fullName" class="field-error">{{ errors.fullName }}</p>
            </div>
            <div class="form-group">
              <label class="form-label">Phone Number *</label>
              <input v-model="form.phone" class="form-input" placeholder="+254 7XX XXX XXX" />
              <p v-if="errors.phone" class="field-error">{{ errors.phone }}</p>
            </div>
            <div class="form-group">
              <label class="form-label">Email Address *</label>
              <input v-model="form.email" class="form-input" type="email" placeholder="you@university.ac.ke" />
              <p v-if="errors.email" class="field-error">{{ errors.email }}</p>
            </div>
          </div>
        </div>

        <!-- Step 2: Academic -->
        <div v-if="currentStep === 1" class="form-step">
          <div class="step-head">
            <div class="step-icon-box">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
                <path d="M6 12v5c3 3 9 3 12 0v-5"/>
              </svg>
            </div>
            <div>
              <h3 class="step-title">Academic Information</h3>
              <p class="step-desc">Your institution and programme details</p>
            </div>
          </div>
          <div class="form-grid">
            <div class="form-group span-2">
              <label class="form-label">University / College *</label>
              <input
                v-model="form.university"
                class="form-input"
                placeholder="e.g. University of Nairobi"
                list="uni-list"
              />
              <datalist id="uni-list">
                <option v-for="u in universities" :key="u.name" :value="u.university_name || u.name">
                  {{ u.university_name || u.name }}
                </option>
              </datalist>
              <p v-if="errors.university" class="field-error">{{ errors.university }}</p>
            </div>
            <div class="form-group span-2">
              <label class="form-label">Course / Programme *</label>
              <input
                v-model="form.course"
                class="form-input"
                placeholder="e.g. Bachelor of Science in Computer Science"
                list="course-list"
              />
              <datalist id="course-list">
                <option v-for="c in courses" :key="c.name" :value="c.name_of_course || c.name">
                  {{ c.name_of_course || c.name }}
                </option>
              </datalist>
              <p v-if="errors.course" class="field-error">{{ errors.course }}</p>
            </div>
            <div class="form-group">
              <label class="form-label">Year of Study *</label>
              <select v-model="form.yearOfStudy" class="form-select">
                <option value="">— Select year —</option>
                <option value="First">First Year</option>
                <option value="Second">Second Year</option>
                <option value="Third">Third Year</option>
                <option value="Fourth">Fourth Year</option>
                <option value="Graduate">Graduate</option>
              </select>
              <p v-if="errors.yearOfStudy" class="field-error">{{ errors.yearOfStudy }}</p>
            </div>
          </div>
        </div>

        <!-- Step 3: Cover Letter -->
        <div v-if="currentStep === 2" class="form-step">
          <div class="step-head">
            <div class="step-icon-box">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
              </svg>
            </div>
            <div>
              <h3 class="step-title">Cover Letter</h3>
              <p class="step-desc">Why do you want to intern at KRCS?</p>
            </div>
          </div>
          <div class="form-grid">
            <div class="form-group span-2">
              <label class="form-label">Cover Letter <span style="font-weight:400;color:var(--muted-foreground)">(optional)</span></label>
              <textarea
                v-model="form.coverLetter"
                class="form-textarea"
                rows="7"
                placeholder="Describe your motivation, relevant experience, and what you hope to contribute and gain from this internship…"
              ></textarea>
            </div>
            <div class="form-group span-2">
              <label class="form-label">Skills &amp; Interests <span style="font-weight:400;color:var(--muted-foreground)">(optional)</span></label>
              <textarea
                v-model="form.skills"
                class="form-textarea"
                rows="3"
                placeholder="e.g. Python, data analysis, public health, community outreach…"
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Navigation -->
        <div class="form-nav">
          <button class="btn btn-outline" type="button" @click="prevStep" :disabled="currentStep === 0">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>
            </svg>
            Back
          </button>
          <div style="display:flex;gap:.75rem;align-items:center;flex-wrap:wrap">
            <p v-if="submitError" class="form-error">{{ submitError }}</p>
            <button
              v-if="currentStep < steps.length - 1"
              class="btn btn-primary"
              type="button"
              @click="nextStep"
            >
              Next
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
              </svg>
            </button>
            <button
              v-else
              class="btn btn-primary"
              type="button"
              @click="handleSubmit"
              :disabled="submitting"
            >
              <svg v-if="submitting" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation:spin 1s linear infinite">
                <circle cx="12" cy="12" r="10" stroke-dasharray="30" stroke-dashoffset="10"/>
              </svg>
              {{ submitting ? "Submitting…" : "Submit Application" }}
            </button>
          </div>
        </div>

      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue"
import { RouterLink } from "vue-router"
import { frappeCall } from "../lib/frappe"
import { usePostingsStore } from "../stores/postings"

const props = defineProps({
  postingId: { type: String, default: "WALK-IN" }
})
const emit = defineEmits(["cancel", "submitted"])

const store = usePostingsStore()
const steps = ["Personal", "Academic", "Cover Letter"]
const currentStep = ref(0)
const submitted = ref(false)
const submitting = ref(false)
const submitError = ref("")
const refNumber = ref("")
const universities = ref([])
const courses = ref([])

const form = ref({
  fullName: "", phone: "", email: "",
  university: "", course: "", yearOfStudy: "",
  coverLetter: "", skills: "",
})

const errors = reactive({})

function clearErrors() {
  Object.keys(errors).forEach((k) => delete errors[k])
}

function validateStep(step) {
  clearErrors()
  if (step === 0) {
    if (!form.value.fullName.trim()) errors.fullName = "Full name is required"
    if (!form.value.email.trim()) errors.email = "Email is required"
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email.trim()))
      errors.email = "Please enter a valid email address"
    if (!form.value.phone.trim()) errors.phone = "Phone number is required"
  } else if (step === 1) {
    if (!form.value.university.trim()) errors.university = "University / college name is required"
    if (!form.value.course.trim()) errors.course = "Course name is required"
    if (!form.value.yearOfStudy) errors.yearOfStudy = "Please select your year of study"
  }
  return Object.keys(errors).length === 0
}

function nextStep() {
  submitError.value = ""
  if (!validateStep(currentStep.value)) return
  if (currentStep.value < steps.length - 1) currentStep.value++
}
function prevStep() {
  submitError.value = ""
  if (currentStep.value > 0) currentStep.value--
}

async function handleSubmit() {
  if (!validateStep(currentStep.value)) return
  submitting.value = true
  submitError.value = ""
  try {
    const coverText = [
      form.value.coverLetter,
      form.value.skills ? `Skills & Interests:\n${form.value.skills}` : ""
    ].filter(Boolean).join("\n\n")

    const res = await frappeCall("krcs_internship.api.submit_application", {
      posting: props.postingId || "WALK-IN",
      applicant_name: form.value.fullName.trim(),
      email: form.value.email.trim(),
      phone: form.value.phone.trim(),
      university: form.value.university.trim(),
      course: form.value.course.trim(),
      year_of_study: form.value.yearOfStudy,
      cover_letter: coverText,
      school_letter: "",
    })

    refNumber.value = res.message?.name || res.message?.reference || "REF-" + Date.now()
    submitted.value = true
    emit("submitted", refNumber.value)
  } catch (e) {
    submitError.value = e.message || "Submission failed. Please try again."
  } finally {
    submitting.value = false
  }
}

function reset() {
  submitted.value = false
  currentStep.value = 0
  submitError.value = ""
  clearErrors()
  form.value = {
    fullName: "", phone: "", email: "",
    university: "", course: "", yearOfStudy: "",
    coverLetter: "", skills: "",
  }
}

onMounted(async () => {
  // Load autocomplete lists in background — failures are silent
  try {
    [universities.value, courses.value] = await Promise.all([
      store.fetchUniversities(),
      store.fetchCourses(),
    ])
  } catch (_) {}
})
</script>

<style scoped>
.app-form-wrap { max-width: 720px; margin: 0 auto; }

/* Step row */
.step-row {
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 2rem; overflow-x: auto; padding-bottom: .5rem; gap: 0;
}
.step-item { display: flex; flex-direction: column; align-items: center; gap: .35rem; flex-shrink: 0; }
.step-label { font-size: .7rem; color: var(--muted-foreground); font-weight: 500; white-space: nowrap; }
.step-circle {
  width: 2.25rem; height: 2.25rem; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: .85rem; font-weight: 600; transition: all .25s;
}
.step-active { background: var(--primary); color: #fff; box-shadow: 0 0 0 4px var(--krcs-red-light); }
.step-done { background: hsl(145, 63%, 42%); color: #fff; }
.step-idle { background: hsl(0, 0%, 78%); color: #fff; }
.step-line {
  flex: 1; height: 2px; background: var(--border);
  position: relative; min-width: 2rem; max-width: 6rem;
  margin: 0 .25rem; margin-bottom: 1.5rem;
}
.step-line-fill { position: absolute; inset-y: 0; left: 0; background: var(--primary); transition: width .4s; }

/* Form card */
.form-card { padding: 2rem; }
.form-step { min-height: 300px; }
.step-head { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.75rem; }
.step-icon-box {
  width: 2.5rem; height: 2.5rem; border-radius: .625rem;
  background: var(--accent); display: flex; align-items: center; justify-content: center;
  color: var(--accent-foreground); flex-shrink: 0;
}
.step-title { font-size: 1.1rem; font-weight: 700; font-family: "Merriweather", serif; margin: 0; }
.step-desc { font-size: .8rem; color: var(--muted-foreground); margin: .2rem 0 0; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-group { display: flex; flex-direction: column; }
.span-2 { grid-column: 1 / -1; }
@media (max-width: 540px) { .form-grid { grid-template-columns: 1fr; } .span-2 { grid-column: 1; } }

.field-error { font-size: .75rem; color: var(--destructive); margin: .2rem 0 0; }

.form-nav {
  display: flex; justify-content: space-between; align-items: center;
  margin-top: 2rem; padding-top: 1.5rem;
  border-top: 1px solid var(--border); flex-wrap: wrap; gap: .75rem;
}
.form-error { color: var(--destructive); font-size: .82rem; margin: 0; max-width: 320px; }

/* Success */
.success-screen { padding: 3rem; text-align: center; max-width: 460px; margin: 2rem auto; }
.success-icon { display: flex; justify-content: center; margin-bottom: 1rem; }
.success-screen h2 { font-family: "Merriweather", serif; font-size: 1.4rem; margin: 0 0 .75rem; }
.success-screen p { color: var(--muted-foreground); font-size: .9rem; margin: .25rem 0; }

@keyframes spin { to { transform: rotate(360deg); } }
</style>