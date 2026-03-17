/**
 * Calls a Frappe whitelisted method.
 * Works whether Frappe's JS is loaded (desk/portal) or via plain fetch (SPA).
 */
export async function frappeCall(method, args = {}) {
  // If Frappe desk JS is available, use it (handles CSRF automatically)
  if (window.frappe?.call) {
    return new Promise((resolve, reject) => {
      window.frappe.call({
        method,
        args,
        callback: resolve,
        error: reject
      })
    })
  }

  // Fallback: plain fetch for guest usage
  const params = new URLSearchParams({ cmd: method, ...args })
  const res = await fetch('/api/method/' + method, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-Frappe-CSRF-Token': getCsrfToken()
    },
    body: params
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

function getCsrfToken() {
  return window.frappe?.csrf_token ||
    document.cookie.split('; ')
      .find(r => r.startsWith('csrf_token='))
      ?.split('=')[1] || ''
}

export async function uploadFile(file, doctype, docname, fieldname) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('doctype', doctype)
  formData.append('docname', docname)
  formData.append('fieldname', fieldname)
  formData.append('is_private', '0')

  const res = await fetch('/api/method/upload_file', {
    method: 'POST',
    headers: { 'X-Frappe-CSRF-Token': getCsrfToken() },
    body: formData
  })
  return res.json()
}