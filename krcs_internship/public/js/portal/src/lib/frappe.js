/**
 * Calls a Frappe whitelisted method.
 * Works whether Frappe's JS is loaded (desk/portal) or via plain fetch (SPA).
 */
export async function frappeCall(method, args = {}) {
  // Use Frappe desk JS when available (handles CSRF automatically)
  if (window.frappe?.call) {
    return new Promise((resolve, reject) => {
      window.frappe.call({
        method,
        args,
        callback: (r) => resolve(r),
        error: (r) => {
          const msg =
            r?.message ||
            r?.exc ||
            (typeof r === "string" ? r : "Frappe call failed")
          reject(new Error(msg))
        }
      })
    })
  }

  // Fallback: plain fetch for SPA / guest usage
  const body = new URLSearchParams()
  body.append("cmd", method)
  for (const [k, v] of Object.entries(args)) {
    if (v === null || v === undefined) continue
    body.append(k, typeof v === "object" ? JSON.stringify(v) : String(v))
  }

  const res = await fetch(`/api/method/${method}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-Frappe-CSRF-Token": _getCsrfToken()
    },
    body: body.toString()
  })

  // Parse response JSON even on error status (Frappe sends error detail in JSON)
  let data
  try {
    data = await res.json()
  } catch (_) {
    throw new Error(`HTTP ${res.status}: non-JSON response from server`)
  }

  if (!res.ok) {
    // Frappe puts the human-readable error in _server_messages or exc
    const serverMsg = _extractFrappeError(data)
    throw new Error(serverMsg || `HTTP ${res.status}`)
  }

  // Frappe encodes Python exceptions in data.exc / data.exc_type
  if (data.exc) {
    const serverMsg = _extractFrappeError(data)
    throw new Error(serverMsg || "Server error")
  }

  return data
}

function _getCsrfToken() {
  // Priority: window.__FRAPPE_SESSION__ (injected by portal.html) >
  //           window.frappe.csrf_token > cookie
  return (
    window.__FRAPPE_SESSION__?.csrf_token ||
    window.frappe?.csrf_token ||
    document.cookie
      .split("; ")
      .find((r) => r.startsWith("csrf_token="))
      ?.split("=")[1] ||
    ""
  )
}

function _extractFrappeError(data) {
  // _server_messages is a JSON-encoded list of message dicts
  if (data._server_messages) {
    try {
      const msgs = JSON.parse(data._server_messages)
      const first = msgs[0]
      if (typeof first === "string") {
        // May itself be JSON-encoded
        try {
          const inner = JSON.parse(first)
          return inner.message || first
        } catch (_) {
          return first
        }
      }
      return first?.message || String(first)
    } catch (_) {}
  }
  if (data.exception) return data.exception
  if (data.exc_type) return `${data.exc_type}: ${data.exc || ""}`
  if (data.message) return data.message
  return null
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
    headers: { "X-Frappe-CSRF-Token": _getCsrfToken() },
    body: formData
  })
  if (!res.ok) throw new Error(`Upload failed: HTTP ${res.status}`)
  return res.json()
}