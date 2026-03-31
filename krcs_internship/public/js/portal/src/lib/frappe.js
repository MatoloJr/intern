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
        error: (err) => reject(new Error(err?.message || "Frappe call failed"))
      })
    })
  }

  // Fallback: plain fetch for guest/SPA usage
  // Frappe expects cmd + flat key-value pairs via form-encoded body
  const body = new URLSearchParams()
  body.append("cmd", method)
  for (const [k, v] of Object.entries(args)) {
    if (v === null || v === undefined) continue
    // Frappe accepts JSON strings for complex values
    body.append(k, typeof v === "object" ? JSON.stringify(v) : String(v))
  }

  const res = await fetch(`/api/method/${method}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-Frappe-CSRF-Token": getCsrfToken()
    },
    body: body.toString()
  })

  if (!res.ok) {
    let msg = `HTTP ${res.status}`
    try {
      const data = await res.json()
      msg = data?.exc_type || data?.message || msg
    } catch (_) {}
    throw new Error(msg)
  }

  const data = await res.json()

  // Frappe returns exceptions as { exc: "...", exc_type: "..." }
  if (data.exc_type) {
    throw new Error(data.exception || data.exc_type || "Server error")
  }

  return data
}

function getCsrfToken() {
  return (
    window.frappe?.csrf_token ||
    document.cookie
      .split("; ")
      .find((r) => r.startsWith("csrf_token="))
      ?.split("=")[1] ||
    ""
  )
}

export async function uploadFile(file, doctype, docname, fieldname) {
  const formData = new FormData()
  formData.append("file", file)
  formData.append("doctype", doctype)
  formData.append("docname", docname)
  formData.append("fieldname", fieldname)
  formData.append("is_private", "0")

  const res = await fetch("/api/method/upload_file", {
    method: "POST",
    headers: { "X-Frappe-CSRF-Token": getCsrfToken() },
    body: formData
  })
  if (!res.ok) throw new Error(`Upload failed: HTTP ${res.status}`)
  return res.json()
}