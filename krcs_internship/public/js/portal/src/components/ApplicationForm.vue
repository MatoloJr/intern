<!-- src/components/ApplicationForm.vue -->
<template>
  <div class="app-form-wrap">
    <!-- Success screen -->
    <div v-if="submitted" class="success-screen card">
      <div class="success-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="hsl(145,63%,42%)" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
      </div>
      <h2>Application Submitted!</h2>
      <p>Reference: <strong>{{ refNumber }}</strong></p>
      <p>A confirmation has been sent to {{ form.email }}</p>
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
              <svg v-if="i < currentStep" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
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
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
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
            </div>
            <div class="form-group">
              <label class="form-label">Date of Birth *</label>
              <input v-model="form.dateOfBirth" class="form-input" type="date" required />
            </div>
            <div class="form-group">
              <label class="form-label">Gender *</label>
              <select v-model="form.gender" class="form-select">
                <option value="">Select gender</option>
                <option>Male</option>
                <option>Female</option>
                <option>Prefer not to say</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">National ID *</label>
              <input v-model="form.nationalId" class="form-input" placeholder="12345678" />
            </div>
            <div class="form-group">
              <label class="form-label">Phone *</label>
              <input v-model="form.phone" class="form-input" placeholder="+254 7XX XXX XXX" />
            </div>
            <div class="form-group">
              <label class="form-label">Email *</label>
              <input v-model="form.email" class="form-input" type="email" placeholder="john@example.com" />
            </div>
            <div class="form-group">
              <label class="form-label">County of Residence *</label>
              <select v-model="form.county" class="form-select">
                <option value="">Select county</option>
                <option v-for="c in counties" :key="c">{{ c }}</option>
              </select>
            </div>
            <div class="form-group span-2">
              <label class="form-label">Physical Address *</label>
              <input v-model="form.physicalAddress" class="form-input" placeholder="P.O. Box 123, Nairobi" />
            </div>
          </div>
        </div>

        <!-- Step 2: Academic Info -->
        <div v-if="currentStep === 1" class="form-step">
          <div class="step-head">
            <div class="step-icon-box">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
            </div>
            <div>
              <h3 class="step-title">Academic Information</h3>
              <p class="step-desc">Your university or college details</p>
            </div>
          </div>
          <div class="form-grid">
            <div class="form-group span-2">
              <label class="form-label">University/College Name *</label>
              <input v-model="form.institution" class="form-input" placeholder="University of Nairobi" />
            </div>
            <div class="form-group">
              <label class="form-label">Registration Number *</label>
              <input v-model="form.regNumber" class="form-input" placeholder="E35/1234/2022" />
            </div>
            <div class="form-group">
              <label class="form-label">Year of Study *</label>
              <select v-model="form.yearOfStudy" class="form-select">
                <option value="">Select year</option>
                <option v-for="y in yearOptions" :key="y">{{ y }}</option>
              </select>
            </div>
            <div class="form-group span-2">
              <label class="form-label">Course/Programme *</label>
              <input v-model="form.course" class="form-input" placeholder="Bachelor of Science in Computer Science" />
            </div>
            <div class="form-group span-2">
              <label class="form-label">Faculty/Department *</label>
              <input v-model="form.faculty" class="form-input" placeholder="School of Computing & Informatics" />
            </div>
            <div class="form-group">
              <label class="form-label">Expected Graduation *</label>
              <select v-model="form.expectedGraduation" class="form-select">
                <option value="">Select year</option>
                <option v-for="y in graduationYears" :key="y">{{ y }}</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Step 3: Attachment Details -->
        <div v-if="currentStep === 2" class="form-step">
          <div class="step-head">
            <div class="step-icon-box">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/></svg>
            </div>
            <div>
              <h3 class="step-title">Attachment Details</h3>
              <p class="step-desc">Where and when you'd like to be placed</p>
            </div>
          </div>
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">Preferred Department *</label>
              <select v-model="form.preferredDepartment" class="form-select">
                <option value="">Select department</option>
                <option v-for="d in departments" :key="d">{{ d }}</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Preferred Branch/County *</label>
              <select v-model="form.preferredBranch" class="form-select">
                <option value="">Select branch</option>
                <option v-for="c in counties" :key="c">{{ c }}</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Start Date *</label>
              <input v-model="form.startDate" class="form-input" type="date" />
            </div>
            <div class="form-group">
              <label class="form-label">End Date *</label>
              <input v-model="form.endDate" class="form-input" type="date" />
            </div>
            <div class="form-group">
              <label class="form-label">Duration (weeks) *</label>
              <input v-model="form.duration" class="form-input" type="number" placeholder="8" min="4" max="52" />
            </div>
          </div>
        </div>

        <!-- Step 4: Emergency Contact -->
        <div v-if="currentStep === 3" class="form-step">
          <div class="step-head">
            <div class="step-icon-box">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            </div>
            <div>
              <h3 class="step-title">Next of Kin / Emergency Contact</h3>
              <p class="step-desc">In case of emergency during your attachment</p>
            </div>
          </div>
          <div class="form-grid">
            <div class="form-group span-2">
              <label class="form-label">Full Name *</label>
              <input v-model="form.kinName" class="form-input" placeholder="Jane Wanjiku Mwangi" />
            </div>
            <div class="form-group">
              <label class="form-label">Relationship *</label>
              <input v-model="form.kinRelationship" class="form-input" placeholder="Mother / Father / Sibling" />
            </div>
            <div class="form-group">
              <label class="form-label">Phone Number *</label>
              <input v-model="form.kinPhone" class="form-input" placeholder="+254 7XX XXX XXX" />
            </div>
          </div>
        </div>

        <!-- Step 5: Documents -->
        <div v-if="currentStep === 4" class="form-step">
          <div class="step-head">
            <div class="step-icon-box">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
            </div>
            <div>
              <h3 class="step-title">Required Documents</h3>
              <p class="step-desc">Upload the following documents to complete your application</p>
            </div>
          </div>
          <div class="docs-alert">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <span>The university introduction letter is mandatory. KRCS requires formal acknowledgment from your institution.</span>
          </div>
          <div class="docs-list">
            <div v-for="doc in requiredDocs" :key="doc.key" class="doc-item">
              <label class="form-label">
                {{ doc.label }}
                <span v-if="doc.required" class="required-star">*</span>
              </label>
              <p v-if="doc.hint" class="doc-hint">{{ doc.hint }}</p>
              <div v-if="files[doc.key]" class="file-uploaded">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                <span>{{ files[doc.key].name }}</span>
                <button class="remove-file" type="button" @click="removeFile(doc.key)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </button>
              </div>
              <div v-else class="upload-zone" @click="triggerUpload(doc.key, doc.accept)">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--muted-foreground)" stroke-width="2" style="margin-bottom:.5rem;"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>
                <p style="font-size:.875rem; color:var(--muted-foreground); margin:0;">Click to upload</p>
                <p style="font-size:.75rem; color:var(--muted-foreground); margin:.25rem 0 0;">{{ doc.accept }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 6: Optional Info -->
        <div v-if="currentStep === 5" class="form-step">
          <div class="step-head">
            <div class="step-icon-box">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            </div>
            <div>
              <h3 class="step-title">Additional Information</h3>
              <p class="step-desc">Optional details to strengthen your application</p>
            </div>
          </div>
          <div class="form-grid">
            <div class="form-group span-2">
              <label class="form-label">LinkedIn Profile URL</label>
              <input v-model="form.linkedIn" class="form-input" placeholder="https://linkedin.com/in/yourprofile" />
            </div>
            <div class="form-group span-2">
              <label class="form-label">Relevant Skills & Areas of Interest</label>
              <textarea v-model="form.skills" class="form-textarea" rows="4" placeholder="e.g. I can code in Python, I speak Swahili and English..."></textarea>
            </div>
            <div class="form-group span-2">
              <label class="form-label">How did you hear about KRCS internships?</label>
              <select v-model="form.referralSource" class="form-select">
                <option value="">Select option</option>
                <option v-for="s in referralSources" :key="s">{{ s }}</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Navigation buttons -->
        <div class="form-nav">
          <button class="btn btn-outline" type="button" @click="prevStep" :disabled="currentStep === 0">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
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
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            </button>
            <button
              v-else
              class="btn btn-primary"
              type="button"
              @click="handleSubmit"
              :disabled="submitting"
            >
              {{ submitting ? 'Submitting…' : 'Submit Application' }}
              <svg v-if="!submitting" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
            </button>
          </div>
        </div>

      </div>
    </template>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { frappeCall } from '../lib/frappe'

const emit = defineEmits(['cancel', 'submitted'])

const steps = ['Personal', 'Academic', 'Attachment', 'Emergency', 'Documents', 'Additional']
const currentStep = ref(0)
const submitted = ref(false)
const submitting = ref(false)
const submitError = ref('')
const refNumber = ref('')
const files = ref({})

const form = ref({
  fullName: '', dateOfBirth: '', gender: '', nationalId: '',
  phone: '', email: '', county: '', physicalAddress: '',
  institution: '', regNumber: '', course: '', yearOfStudy: '',
  expectedGraduation: '', faculty: '',
  preferredDepartment: '', preferredBranch: '',
  startDate: '', endDate: '', duration: '',
  kinName: '', kinRelationship: '', kinPhone: '',
  linkedIn: '', skills: '', referralSource: '',
})

const counties = [
  'Baringo','Bomet','Bungoma','Busia','Elgeyo-Marakwet','Embu','Garissa',
  'Homa Bay','Isiolo','Kajiado','Kakamega','Kericho','Kiambu','Kilifi',
  'Kirinyaga','Kisii','Kisumu','Kitui','Kwale','Laikipia','Lamu',
  'Machakos','Makueni','Mandera','Marsabit','Meru','Migori','Mombasa',
  "Murang'a",'Nairobi','Nakuru','Nandi','Narok','Nyamira','Nyandarua',
  'Nyeri','Samburu','Siaya','Taita-Taveta','Tana River','Tharaka-Nithi',
  'Trans-Nzoia','Turkana','Uasin Gishu','Vihiga','Wajir','West Pokot',
]

const departments = [
  'Health & Social Services','Disaster Management','ICT & Innovation',
  'Finance & Administration','Human Resource','Supply Chain & Logistics',
  'Communication & Resource Mobilization','Youth & Volunteering',
  'Legal & Compliance','Monitoring, Evaluation & Learning',
]

const yearOptions = ['1st Year','2nd Year','3rd Year','4th Year','5th Year','6th Year','Postgraduate']
const graduationYears = Array.from({ length: 8 }, (_, i) => String(new Date().getFullYear() + i))
const referralSources = [
  'University career office','KRCS website','Social media',
  'Friend or family member','Previous KRCS intern/volunteer','Job board','Other',
]

const requiredDocs = [
  { label: 'University Introduction Letter', key: 'introLetter', required: true, accept: '.pdf,.doc,.docx', hint: 'Must be on official university letterhead' },
  { label: 'National ID or Student ID', key: 'nationalIdDoc', required: true, accept: '.pdf,.jpg,.jpeg,.png' },
  { label: 'Academic Transcript / Result Slip', key: 'transcript', required: true, accept: '.pdf,.jpg,.jpeg,.png', hint: 'Most recent copy' },
  { label: 'Insurance Cover', key: 'insurance', required: true, accept: '.pdf,.jpg,.jpeg,.png', hint: 'NHIF or student insurance cover' },
  { label: 'Passport Photo', key: 'passportPhoto', required: true, accept: '.jpg,.jpeg,.png', hint: 'Recent passport-size photo' },
  { label: 'CV / Resume (optional)', key: 'cv', required: false, accept: '.pdf,.doc,.docx' },
]

function triggerUpload(key, accept) {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = accept
  input.onchange = (e) => {
    const file = e.target.files?.[0]
    if (file) files.value = { ...files.value, [key]: { name: file.name, file } }
  }
  input.click()
}

function removeFile(key) {
  const updated = { ...files.value }
  delete updated[key]
  files.value = updated
}

function nextStep() {
  submitError.value = ''
  if (currentStep.value === 4) {
    const required = ['introLetter', 'nationalIdDoc', 'transcript', 'insurance', 'passportPhoto']
    const missing = required.filter(k => !files.value[k])
    if (missing.length > 0) {
      submitError.value = 'Please upload all required documents before proceeding.'
      return
    }
  }
  if (currentStep.value < steps.length - 1) currentStep.value++
}

function prevStep() {
  submitError.value = ''
  if (currentStep.value > 0) currentStep.value--
}

async function handleSubmit() {
  submitting.value = true
  submitError.value = ''
  try {
    const res = await frappeCall('krcs_internship.api.submit_application', {
      posting: 'WALK-IN',
      applicant_name: form.value.fullName,
      email: form.value.email,
      phone: form.value.phone,
      university: form.value.institution,
      course: form.value.course,
      year_of_study: form.value.yearOfStudy,
      cover_letter: form.value.skills,
    })
    refNumber.value = res.message?.name || 'REF-' + Date.now()
    submitted.value = true
    emit('submitted')
  } catch (e) {
    submitError.value = e.message || 'Submission failed. Please try again.'
  } finally {
    submitting.value = false
  }
}

function reset() {
  submitted.value = false
  currentStep.value = 0
  submitError.value = ''
  files.value = {}
  Object.keys(form.value).forEach(k => { form.value[k] = '' })
}
</script>

<style scoped>
.app-form-wrap { max-width: 800px; margin: 0 auto; }

/* Step indicator row */
.step-indicator-row {
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 2rem; gap: 0; overflow-x: auto; padding-bottom: .5rem;
}
.step-item { display: flex; flex-direction: column; align-items: center; gap: .4rem; flex-shrink: 0; }
.step-label { font-size: .7rem; color: var(--muted-foreground); font-weight: 500; white-space: nowrap; }
.step-connector {
  flex: 1; height: 2px; background: var(--border);
  position: relative; min-width: 1rem; max-width: 4rem;
  margin: 0 .2rem; margin-bottom: 1.6rem;
}
.step-connector-fill { position: absolute; inset-y: 0; left: 0; background: var(--primary); transition: width .4s; }

/* Form card */
.form-card { padding: 2rem; }
.form-step { min-height: 380px; }
.step-head { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.75rem; }
.step-icon-box {
  width: 2.5rem; height: 2.5rem; border-radius: .625rem;
  background: var(--accent); display: flex; align-items: center; justify-content: center;
  color: var(--accent-foreground); flex-shrink: 0;
}
.step-title { font-size: 1.1rem; font-weight: 700; font-family: 'Merriweather', serif; margin: 0; color: var(--foreground); }
.step-desc { font-size: .8rem; color: var(--muted-foreground); margin: .2rem 0 0; }

/* Form grid */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-group { display: flex; flex-direction: column; }
.span-2 { grid-column: 1 / -1; }
@media (max-width: 560px) {
  .form-grid { grid-template-columns: 1fr; }
  .span-2 { grid-column: 1; }
}

/* Documents */
.docs-alert {
  display: flex; align-items: flex-start; gap: .65rem;
  background: var(--accent); border: 1px solid rgba(0,0,0,.06);
  border-radius: .5rem; padding: .85rem 1rem;
  font-size: .825rem; color: var(--accent-foreground);
  margin-bottom: 1.5rem;
}
.docs-list { display: flex; flex-direction: column; gap: 1.25rem; }
.doc-hint { font-size: .75rem; color: var(--muted-foreground); margin: .15rem 0 .4rem; }
.required-star { color: var(--destructive); margin-left: .15rem; }
.file-uploaded {
  display: flex; align-items: center; gap: .75rem;
  background: var(--accent); border: 1px solid var(--border);
  border-radius: .5rem; padding: .65rem .85rem;
}
.file-uploaded span { flex: 1; font-size: .875rem; color: var(--foreground); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.remove-file { background: none; border: none; cursor: pointer; color: var(--muted-foreground); padding: 0; display: flex; align-items: center; }
.remove-file:hover { color: var(--destructive); }

/* Nav */
.form-nav {
  display: flex; justify-content: space-between; align-items: center;
  margin-top: 2rem; padding-top: 1.5rem;
  border-top: 1px solid var(--border); flex-wrap: wrap; gap: .75rem;
}
.form-error { color: var(--destructive); font-size: .8rem; margin: 0; }

/* Success */
.success-screen { padding: 3rem; text-align: center; max-width: 480px; margin: 2rem auto; }
.success-icon { margin-bottom: 1rem; display: flex; justify-content: center; }
.success-screen h2 { font-family: 'Merriweather', serif; font-size: 1.5rem; margin: 0 0 .75rem; }
.success-screen p { color: var(--muted-foreground); font-size: .9rem; margin: .25rem 0; }
</style>