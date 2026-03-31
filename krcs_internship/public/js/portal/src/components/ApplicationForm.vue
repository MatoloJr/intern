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
      <p>A confirmation has been sent to <strong>{{ form.email }}</strong></p>
      <div style="display:flex; gap:1rem; justify-content:center; flex-wrap:wrap; margin-top:1rem;">
        <RouterLink to="/track" class="btn btn-primary">Track My Application</RouterLink>
        <button class="btn btn-outline" @click="reset">Submit Another</button>
      </div>
    </div>

    <template v-else>
      <!-- Step indicator -->
      <div class="step-indicator-row">
        <template v-for="(s, i) in steps" :key="s">
          <div class="step-item">
            <div :class="['step-indicator', i < currentStep ? 'step-complete' : i === currentStep ? 'step-active' : 'step-inactive']">
              <svg v-if="i < currentStep" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              <span v-else>{{ i + 1 }}</span>
            </div>
            <span class="step-label">{{ s }}</span>
          </div>
          <div v-if="i < steps.length - 1" class="step-connector">
            <div class="step-connector-fill" :style="{ width: i < currentStep ? '100%' : '0%' }"></div>
          </div>
        </template>
      </div>

      <!-- Form card -->
      <div class="card form-card">

        <!-- Step 1: Personal Info -->
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
              <input v-model="form.fullName" class="form-input" placeholder="John Kamau Mwangi" required />
              <p v-if="fieldErrors.fullName" class="field-error">{{ fieldErrors.fullName }}</p>
            </div>
            <div class="form-group">
              <label class="form-label">Phone *</label>
              <input v-model="form.phone" class="form-input" placeholder="+254 7XX XXX XXX" />
              <p v-if="fieldErrors.phone" class="field-error">{{ fieldErrors.phone }}</p>
            </div>
            <div class="form-group">
              <label class="form-label">Email *</label>
              <input v-model="form.email" class="form-input" type="email" placeholder="john@example.com" />
              <p v-if="fieldErrors.email" class="field-error">{{ fieldErrors.email }}</p>
            </div>
          </div>
        </div>

        <!-- Step 2: Academic Info -->
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
              <p class="step-desc">Your university or college details</p>
            </div>
          </div>
          <div class="form-grid">
            <div class="form-group span-2">
              <label class="form-label">University / College Name *</label>
              <input v-model="form.university" class="form-input" placeholder="University of Nairobi" />
              <p v-if="fieldErrors.university" class="field-error">{{ fieldErrors.university }}</p>
            </div>
            <div class="form-group span-2">
              <label class="form-label">Course / Programme *</label>
              <input v-model="form.course" class="form-input" placeholder="Bachelor of Science in Computer Science" />
              <p v-if="fieldErrors.course" class="field-error">{{ fieldErrors.course }}</p>
            </div>
            <div class="form-group">
              <label class="form-label">Year of Study *</label>
              <select v-model="form.yearOfStudy" class="form-select">
                <option value="">Select year</option>
                <option value="First">First</option>
                <option value="Second">Second</option>
                <option value="Third">Third</option>
                <option value="Fourth">Fourth</option>
                <option value="Graduate">Graduate</option>
              </select>
              <p v-if="fieldErrors.yearOfStudy" class="field-error">{{ fieldErrors.yearOfStudy }}</p>
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
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
              </svg>
            </div>
            <div>
              <h3 class="step-title">Cover Letter</h3>
              <p class="step-desc">Tell us why you want to intern at KRCS</p>
            </div>
          </div>
          <div class="form-grid">
            <div class="form-group span-2">
              <label class="form-label">Cover Letter</label>
              <textarea
                v-model="form.coverLetter"
                class="form-textarea"
                rows="8"
                placeholder="Describe your motivation, relevant skills and what you hope to gain from this internship..."
              ></textarea>
            </div>
            <div class="form-group span-2">
              <label class="form-label">Skills &amp; Areas of Interest</label>
              <textarea
                v-model="form.skills"
                class="form-textarea"
                rows="4"
                placeholder="e.g. Python, data analysis, public health, community outreach..."
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Navigation buttons -->
        <div class="form-nav">
          <button
            class="btn btn-outline"
            type="button"
            @click="prevStep"
            :disabled="currentStep === 0"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="19" y1="12" x2="5" y2="12"/>
              <polyline points="12 19 5 12 12 5"/>
            </svg>
            Back
          </button>
          <div style="display:flex; gap:.75rem; align-items:center;">
            <p v-if="submitError" class="form-error">{{ submitError }}</p>
            <button
              v-if="currentStep < steps.length - 1"
              class="btn btn-primary"
              type="button"
              @click="nextStep"
            >
              Next
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="5" y1="12" x2="19" y2="12"/>
                <polyline points="12 5 19 12 12 19"/>
              </svg>
            </button>
            <button
              v-else
              class="btn btn-primary"
              type="button"
              @click="handleSubmit"
              :disabled="submitting"
            >
              {{ submitting ? "Submitting…" : "Submit Application" }}
              <svg v-if="!submitting" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="22" y1="2" x2="11" y2="13"/>
                <polygon points="22 2 15 22 11 13 2 9 22 2"/>
              </svg>
            </button>
          </div>
        </div>

      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue"
import { RouterLink } from "vue-router"
import { frappeCall } from "../lib/frappe"

const props = defineProps({
  postingId: { type: String, default: "WALK-IN" }
})

const emit = defineEmits(["cancel", "submitted"])

const steps = ["Personal", "Academic", "Cover Letter"]
const currentStep = ref(0)
const submitted = ref(false)
const submitting = ref(false)
const submitError = ref("")
const refNumber = ref("")

const form = ref({
  fullName: "",
  phone: "",
  email: "",
  university: "",
  course: "",
  yearOfStudy: "",
  coverLetter: "",
  skills: "",
})

const fieldErrors = reactive({})

function validateStep(step) {
  // Clear errors for this step
  Object.keys(fieldErrors).forEach((k) => delete fieldErrors[k])

  if (step === 0) {
    if (!form.value.fullName.trim()) fieldErrors.fullName = "Full name is required"
    if (!form.value.email.trim()) fieldErrors.email = "Email is required"
    if (!form.value.phone.trim()) fieldErrors.phone = "Phone number is required"
  } else if (step === 1) {
    if (!form.value.university.trim()) fieldErrors.university = "University name is required"
    if (!form.value.course.trim()) fieldErrors.course = "Course name is required"
    if (!form.value.yearOfStudy) fieldErrors.yearOfStudy = "Please select your year of study"
  }

  return Object.keys(fieldErrors).length === 0
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
    const res = await frappeCall("krcs_internship.api.submit_application", {
      posting: props.postingId || "WALK-IN",
      applicant_name: form.value.fullName,
      email: form.value.email,
      phone: form.value.phone,
      university: form.value.university,
      course: form.value.course,
      year_of_study: form.value.yearOfStudy,
      cover_letter: form.value.coverLetter + (form.value.skills ? `\n\nSkills: ${form.value.skills}` : ""),
      school_letter: "",
    })
    refNumber.value = res.message?.name || "REF-" + Date.now()
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
  Object.keys(fieldErrors).forEach((k) => delete fieldErrors[k])
  form.value = {
    fullName: "", phone: "", email: "",
    university: "", course: "", yearOfStudy: "",
    coverLetter: "", skills: "",
  }
}
</script>

<style scoped>
.app-form-wrap { max-width: 720px; margin: 0 auto; }

.step-indicator-row {
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 2rem; overflow-x: auto; padding-bottom: .5rem;
}
.step-item { display: flex; flex-direction: column; align-items: center; gap: .4rem; flex-shrink: 0; }
.step-label { font-size: .7rem; color: var(--muted-foreground); font-weight: 500; white-space: nowrap; }
.step-connector {
  flex: 1; height: 2px; background: var(--border);
  position: relative; min-width: 1.5rem; max-width: 5rem;
  margin: 0 .3rem; margin-bottom: 1.6rem;
}
.step-connector-fill { position: absolute; inset-y: 0; left: 0; background: var(--primary); transition: width .4s; }

.form-card { padding: 2rem; }
.form-step { min-height: 320px; }
.step-head { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.75rem; }
.step-icon-box {
  width: 2.5rem; height: 2.5rem; border-radius: .625rem;
  background: var(--accent); display: flex; align-items: center; justify-content: center;
  color: var(--accent-foreground); flex-shrink: 0;
}
.step-title { font-size: 1.1rem; font-weight: 700; font-family: "Merriweather", serif; margin: 0; color: var(--foreground); }
.step-desc { font-size: .8rem; color: var(--muted-foreground); margin: .2rem 0 0; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-group { display: flex; flex-direction: column; }
.span-2 { grid-column: 1 / -1; }
@media (max-width: 560px) {
  .form-grid { grid-template-columns: 1fr; }
  .span-2 { grid-column: 1; }
}

.field-error { font-size: .75rem; color: var(--destructive); margin: .25rem 0 0; }

.form-nav {
  display: flex; justify-content: space-between; align-items: center;
  margin-top: 2rem; padding-top: 1.5rem;
  border-top: 1px solid var(--border); flex-wrap: wrap; gap: .75rem;
}
.form-error { color: var(--destructive); font-size: .8rem; margin: 0; }

.success-screen { padding: 3rem; text-align: center; max-width: 480px; margin: 2rem auto; }
.success-icon { margin-bottom: 1rem; display: flex; justify-content: center; }
.success-screen h2 { font-family: "Merriweather", serif; font-size: 1.5rem; margin: 0 0 .75rem; }
.success-screen p { color: var(--muted-foreground); font-size: .9rem; margin: .25rem 0; }
</style>