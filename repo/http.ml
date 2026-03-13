# =============================================================================
# MyLang HTTP Package v1.0.0
# =============================================================================
# HTTP client utilities for MyLang
# Requires: requests (pip install requests)
# Author: MyLang Team
# Repository: https://github.com/Botan-linux/mylang
# =============================================================================

# Get requests module
let _requests = __py_import__("requests")

# -----------------------------------------------------------------------------
# Response Class
# -----------------------------------------------------------------------------

class HttpResponse {
    fn new(status_code, headers, body, url) {
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.url = url
        return self
    }
    
    fn ok() {
        return self.status_code >= 200 and self.status_code < 300
    }
    
    fn is_redirect() {
        return self.status_code >= 300 and self.status_code < 400
    }
    
    fn is_client_error() {
        return self.status_code >= 400 and self.status_code < 500
    }
    
    fn is_server_error() {
        return self.status_code >= 500
    }
    
    fn json() {
        return __py_import__("json").loads(self.body)
    }
    
    fn text() {
        return self.body
    }
}

# -----------------------------------------------------------------------------
# HTTP Methods
# -----------------------------------------------------------------------------

# GET request
fn http_get(url, params, headers, timeout) {
    if params == none { params = {} }
    if headers == none { headers = {} }
    if timeout == none { timeout = 30 }
    
    try {
        let response = _requests.get(url, params=params, headers=headers, timeout=timeout)
        return HttpResponse.new(
            response.status_code,
            dict(response.headers),
            response.text,
            response.url
        )
    } catch(e) {
        return HttpResponse.new(0, {}, "", url)
    }
}

# POST request
fn http_post(url, data, json_data, headers, timeout) {
    if data == none { data = {} }
    if json_data == none { json_data = none }
    if headers == none { headers = {} }
    if timeout == none { timeout = 30 }
    
    try {
        let response
        if json_data != none {
            response = _requests.post(url, json=json_data, headers=headers, timeout=timeout)
        } else {
            response = _requests.post(url, data=data, headers=headers, timeout=timeout)
        }
        return HttpResponse.new(
            response.status_code,
            dict(response.headers),
            response.text,
            response.url
        )
    } catch(e) {
        return HttpResponse.new(0, {}, "", url)
    }
}

# PUT request
fn http_put(url, data, json_data, headers, timeout) {
    if data == none { data = {} }
    if json_data == none { json_data = none }
    if headers == none { headers = {} }
    if timeout == none { timeout = 30 }
    
    try {
        let response
        if json_data != none {
            response = _requests.put(url, json=json_data, headers=headers, timeout=timeout)
        } else {
            response = _requests.put(url, data=data, headers=headers, timeout=timeout)
        }
        return HttpResponse.new(
            response.status_code,
            dict(response.headers),
            response.text,
            response.url
        )
    } catch(e) {
        return HttpResponse.new(0, {}, "", url)
    }
}

# PATCH request
fn http_patch(url, data, json_data, headers, timeout) {
    if data == none { data = {} }
    if json_data == none { json_data = none }
    if headers == none { headers = {} }
    if timeout == none { timeout = 30 }
    
    try {
        let response
        if json_data != none {
            response = _requests.patch(url, json=json_data, headers=headers, timeout=timeout)
        } else {
            response = _requests.patch(url, data=data, headers=headers, timeout=timeout)
        }
        return HttpResponse.new(
            response.status_code,
            dict(response.headers),
            response.text,
            response.url
        )
    } catch(e) {
        return HttpResponse.new(0, {}, "", url)
    }
}

# DELETE request
fn http_delete(url, headers, timeout) {
    if headers == none { headers = {} }
    if timeout == none { timeout = 30 }
    
    try {
        let response = _requests.delete(url, headers=headers, timeout=timeout)
        return HttpResponse.new(
            response.status_code,
            dict(response.headers),
            response.text,
            response.url
        )
    } catch(e) {
        return HttpResponse.new(0, {}, "", url)
    }
}

# HEAD request
fn http_head(url, headers, timeout) {
    if headers == none { headers = {} }
    if timeout == none { timeout = 30 }
    
    try {
        let response = _requests.head(url, headers=headers, timeout=timeout)
        return HttpResponse.new(
            response.status_code,
            dict(response.headers),
            "",
            response.url
        )
    } catch(e) {
        return HttpResponse.new(0, {}, "", url)
    }
}

# OPTIONS request
fn http_options(url, headers, timeout) {
    if headers == none { headers = {} }
    if timeout == none { timeout = 30 }
    
    try {
        let response = _requests.options(url, headers=headers, timeout=timeout)
        return HttpResponse.new(
            response.status_code,
            dict(response.headers),
            response.text,
            response.url
        )
    } catch(e) {
        return HttpResponse.new(0, {}, "", url)
    }
}

# -----------------------------------------------------------------------------
# Convenience Functions
# -----------------------------------------------------------------------------

# Fetch JSON from URL
fn http_get_json(url, params, headers, timeout) {
    let response = http_get(url, params, headers, timeout)
    if response.ok() {
        return response.json()
    }
    return none
}

# Fetch text from URL
fn http_get_text(url, params, headers, timeout) {
    let response = http_get(url, params, headers, timeout)
    if response.ok() {
        return response.text()
    }
    return ""
}

# Post and get JSON response
fn http_post_json(url, data, headers, timeout) {
    let response = http_post(url, data, none, headers, timeout)
    if response.ok() {
        return response.json()
    }
    return none
}

# Download file
fn http_download(url, filepath, timeout) {
    if timeout == none { timeout = 60 }
    
    try {
        let response = _requests.get(url, timeout=timeout, stream=true)
        if response.status_code == 200 {
            let _f = __py_import__("open")(filepath, "wb")
            for chunk in response.iter_content(chunk_size=8192) {
                _f.write(chunk)
            }
            _f.close()
            return true
        }
        return false
    } catch(e) {
        return false
    }
}

# -----------------------------------------------------------------------------
# Session Management
# -----------------------------------------------------------------------------

class HttpSession {
    fn new() {
        self._session = _requests.Session()
        self.base_url = ""
        self.default_headers = {}
        return self
    }
    
    fn set_base_url(url) {
        self.base_url = url
        return self
    }
    
    fn set_header(key, value) {
        self.default_headers[key] = value
        return self
    }
    
    fn set_auth(username, password) {
        self._session.auth = (username, password)
        return self
    }
    
    fn set_timeout(timeout) {
        self.timeout = timeout
        return self
    }
    
    fn _merge_headers(headers) {
        let merged = {}
        for key in self.default_headers {
            merged[key] = self.default_headers[key]
        }
        if headers != none {
            for key in headers {
                merged[key] = headers[key]
            }
        }
        return merged
    }
    
    fn _build_url(path) {
        if self.base_url == "" {
            return path
        }
        return self.base_url + path
    }
    
    fn get(path, params, headers) {
        return http_get(
            self._build_url(path),
            params,
            self._merge_headers(headers),
            self.timeout
        )
    }
    
    fn post(path, data, json_data, headers) {
        return http_post(
            self._build_url(path),
            data,
            json_data,
            self._merge_headers(headers),
            self.timeout
        )
    }
    
    fn put(path, data, json_data, headers) {
        return http_put(
            self._build_url(path),
            data,
            json_data,
            self._merge_headers(headers),
            self.timeout
        )
    }
    
    fn delete(path, headers) {
        return http_delete(
            self._build_url(path),
            self._merge_headers(headers),
            self.timeout
        )
    }
    
    fn close() {
        self._session.close()
    }
}

# -----------------------------------------------------------------------------
# URL Utilities
# -----------------------------------------------------------------------------

# URL encode
fn url_encode(params) {
    return __py_import__("urllib.parse").urlencode(params)
}

# URL decode
fn url_decode(str) {
    return __py_import__("urllib.parse").parse_qs(str)
}

# Parse URL
fn url_parse(url) {
    let parsed = __py_import__("urllib.parse").urlparse(url)
    return {
        "scheme": parsed.scheme,
        "netloc": parsed.netloc,
        "path": parsed.path,
        "params": parsed.params,
        "query": parsed.query,
        "fragment": parsed.fragment
    }
}

# Build URL from parts
fn url_build(parts) {
    return __py_import__("urllib.parse").urlunparse((
        parts["scheme"] or "",
        parts["netloc"] or "",
        parts["path"] or "",
        parts["params"] or "",
        parts["query"] or "",
        parts["fragment"] or ""
    ))
}

# Join URL paths
fn url_join(base, path) {
    return __py_import__("urllib.parse").urljoin(base, path)
}

# -----------------------------------------------------------------------------
# Status Code Helpers
# -----------------------------------------------------------------------------

fn http_status_name(code) {
    let names = {
        200: "OK",
        201: "Created",
        202: "Accepted",
        204: "No Content",
        301: "Moved Permanently",
        302: "Found",
        304: "Not Modified",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        408: "Request Timeout",
        409: "Conflict",
        429: "Too Many Requests",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout"
    }
    return names[code] or "Unknown"
}

# -----------------------------------------------------------------------------
# Export all
# -----------------------------------------------------------------------------

export HttpResponse
export http_get, http_post, http_put, http_patch, http_delete, http_head, http_options
export http_get_json, http_get_text, http_post_json, http_download
export HttpSession
export url_encode, url_decode, url_parse, url_build, url_join
export http_status_name
