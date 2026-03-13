# =============================================================================
# MyLang HTTP Package v1.0.0
# =============================================================================
# Requires: pip install requests
# =============================================================================

let _requests = __py_import__("requests")

# Response Class
export class HttpResponse {
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
    
    fn json() {
        return __py_import__("json").loads(self.body)
    }
    
    fn text() {
        return self.body
    }
}

# HTTP Methods
export fn http_get(url) {
    try {
        let resp = _requests.get(url)
        return HttpResponse.new(resp.status_code, dict(resp.headers), resp.text, resp.url)
    } catch(e) {
        return HttpResponse.new(0, {}, "", url)
    }
}

export fn http_post(url, data) {
    try {
        let resp = _requests.post(url, data)
        return HttpResponse.new(resp.status_code, dict(resp.headers), resp.text, resp.url)
    } catch(e) {
        return HttpResponse.new(0, {}, "", url)
    }
}

export fn http_put(url, data) {
    try {
        let resp = _requests.put(url, data)
        return HttpResponse.new(resp.status_code, dict(resp.headers), resp.text, resp.url)
    } catch(e) {
        return HttpResponse.new(0, {}, "", url)
    }
}

export fn http_delete(url) {
    try {
        let resp = _requests.delete(url)
        return HttpResponse.new(resp.status_code, dict(resp.headers), resp.text, resp.url)
    } catch(e) {
        return HttpResponse.new(0, {}, "", url)
    }
}

# Convenience Functions
export fn http_get_json(url) {
    let resp = http_get(url)
    if resp.ok() {
        return resp.json()
    }
    return none
}

export fn http_get_text(url) {
    let resp = http_get(url)
    if resp.ok() {
        return resp.text()
    }
    return ""
}

# URL Utilities
export fn url_encode(params) {
    return __py_import__("urllib.parse").urlencode(params)
}

export fn url_parse(url) {
    let parsed = __py_import__("urllib.parse").urlparse(url)
    let result = {}
    result["scheme"] = parsed.scheme
    result["netloc"] = parsed.netloc
    result["path"] = parsed.path
    result["query"] = parsed.query
    return result
}
