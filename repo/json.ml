# =============================================================================
# MyLang JSON Package v1.0.0
# =============================================================================

let _json = __py_import__("json")

# Parse JSON string to object
export fn json_parse(s) {
    try {
        return _json.loads(s)
    } catch(e) {
        return none
    }
}

# Convert object to JSON string
export fn json_stringify(obj, indent) {
    try {
        if indent == none {
            return _json.dumps(obj)
        }
        return _json.dumps(obj, indent)
    } catch(e) {
        return ""
    }
}

# Convert object to pretty JSON string
export fn json_pretty(obj) {
    return _json.dumps(obj, 2)
}

# Read JSON from file
export fn json_read_file(filepath) {
    try {
        let f = __py_import__("open")(filepath, "r")
        let content = f.read()
        f.close()
        return json_parse(content)
    } catch(e) {
        return none
    }
}

# Write JSON to file
export fn json_write_file(filepath, obj) {
    try {
        let f = __py_import__("open")(filepath, "w")
        f.write(_json.dumps(obj, 2))
        f.close()
        return true
    } catch(e) {
        return false
    }
}

# Check if string is valid JSON
export fn json_is_valid(s) {
    try {
        _json.loads(s)
        return true
    } catch(e) {
        return false
    }
}

# Get all keys
export fn obj_keys(obj) {
    return __py_import__("list")(obj.keys())
}

# Get all values  
export fn obj_values(obj) {
    return __py_import__("list")(obj.values())
}

# Check if key exists
export fn obj_has_key(obj, key) {
    return key in obj
}
