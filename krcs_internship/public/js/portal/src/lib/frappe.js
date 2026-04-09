/**
 * Calls a Frappe whitelisted method via JSON POST.
 *
 * Works in two modes:
 *   1. Inside Frappe desk/portal (window.frappe.call exists) — uses it directly
 *   2. Standalone SPA / Vite dev server — uses fetch with CSRF token
 */
export async function frappeCall(method, args = {}) {
	// ── Mode 1: Full Frappe desk JS available ──────────────────────────────
	if (window.frappe?.call && typeof window.frappe.call === 'function') {
		return new Promise((resolve, reject) => {
			window.frappe.call({
				method,
				args,
				callback: (r) => resolve(r),
				error: (r) => {
					const msg =
						r?.message ||
						r?.exc ||
						(typeof r === 'string' ? r : 'Frappe call failed')
					reject(new Error(msg))
				}
			})
		})
	}

	// ── Mode 2: SPA / Vite dev mode — plain fetch ──────────────────────────
	// Build the URL: in production the base is the Frappe site,
	// in Vite dev the proxy rewrites /api → intern.localhost:8006
	const url = '/api/method/' + method

	const csrfToken = _getCsrfToken()

	let response
	try {
		response = await fetch(url, {
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'X-Frappe-CSRF-Token': csrfToken,
				'X-Requested-With': 'XMLHttpRequest'
			},
			credentials: 'include',   // send session cookie so Frappe sees the session
			body: JSON.stringify(args)
		})
	} catch (networkErr) {
		throw new Error('Network error: ' + networkErr.message)
	}

	let data
	try {
		data = await response.json()
	} catch (_) {
		throw new Error(`HTTP ${response.status}: server returned non-JSON response`)
	}

	// Frappe signals errors via exc string or _server_messages
	if (!response.ok || (data.exc && data.exc.trim())) {
		const serverMsg = _extractFrappeError(data)
		throw new Error(serverMsg || `HTTP ${response.status}`)
	}

	return data
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function _getCsrfToken() {
	// Priority: shim injected by portal.html > frappe global > cookie
	return (
		window.__FRAPPE_SESSION__?.csrf_token ||
		window.frappe?.csrf_token ||
		_cookieValue('csrf_token') ||
		'Guest'
	)
}

function _cookieValue(name) {
	const match = document.cookie
		.split('; ')
		.find((c) => c.startsWith(name + '='))
	return match ? decodeURIComponent(match.split('=')[1]) : ''
}

function _extractFrappeError(data) {
	if (data._server_messages) {
		try {
			const msgs = JSON.parse(data._server_messages)
			const first = Array.isArray(msgs) ? msgs[0] : msgs
			if (typeof first === 'string') {
				try {
					return JSON.parse(first).message || first
				} catch (_) {
					return first
				}
			}
			return first?.message || String(first)
		} catch (_) {}
	}
	if (data.exception) return data.exception
	if (data.exc_type) return `${data.exc_type}: ${data.exc || ''}`
	if (data.message && typeof data.message === 'string') return data.message
	return null
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
		headers: {
			'X-Frappe-CSRF-Token': _getCsrfToken(),
			'X-Requested-With': 'XMLHttpRequest'
		},
		credentials: 'include',
		body: formData
	})
	if (!res.ok) throw new Error(`Upload failed: HTTP ${res.status}`)
	return res.json()
}