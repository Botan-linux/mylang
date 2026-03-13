# =============================================================================
# MyLang JSON Package v1.0.0
# =============================================================================
# JSON utilities for MyLang
# Author: MyLang Team
# Repository: https://github.com/Botan-linux/mylang
# =============================================================================

let _json = __py_import__("json")

# -----------------------------------------------------------------------------
# Basic JSON Operations
# -----------------------------------------------------------------------------

# Parse JSON string to object
fn json_parse(str) {
    try {
        return _json.loads(str)
    } catch(e) {
        return none
    }
}

# Convert object to JSON string
fn json_stringify(obj, indent) {
    if indent == none { indent = none }
    try {
        return _json.dumps(obj, indent=indent, ensure_ascii=false)
    } catch(e) {
        return ""
    }
}

# Convert object to pretty JSON string
fn json_pretty(obj) {
    return json_stringify(obj, 2)
}

# Convert object to compact JSON string
fn json_compact(obj) {
    return json_stringify(obj, none)
}

# -----------------------------------------------------------------------------
# File Operations
# -----------------------------------------------------------------------------

# Read JSON from file
fn json_read_file(filepath) {
    try {
        let _f = __py_import__("open")(filepath, "r", encoding="utf-8")
        let content = _f.read()
        _f.close()
        return json_parse(content)
    } catch(e) {
        return none
    }
}

# Write JSON to file
fn json_write_file(filepath, obj, indent) {
    if indent == none { indent = 2 }
    try {
        let _f = __py_import__("open")(filepath, "w", encoding="utf-8")
        _f.write(json_stringify(obj, indent))
        _f.close()
        return true
    } catch(e) {
        return false
    }
}

# -----------------------------------------------------------------------------
# Validation
# -----------------------------------------------------------------------------

# Check if string is valid JSON
fn json_is_valid(str) {
    try {
        _json.loads(str)
        return true
    } catch(e) {
        return false
    }
}

# Get JSON type
fn json_type(value) {
    if value == none { return "null" }
    if __py_import__("isinstance")(value, __py_import__("bool")) { return "boolean" }
    if __py_import__("isinstance")(value, __py_import__("int")) { return "number" }
    if __py_import__("isinstance")(value, __py_import__("float")) { return "number" }
    if __py_import__("isinstance")(value, __py_import__("str")) { return "string" }
    if __py_import__("isinstance")(value, __py_import__("list")) { return "array" }
    if __py_import__("isinstance")(value, __py_import__("dict")) { return "object" }
    return "unknown"
}

# -----------------------------------------------------------------------------
# Path-based Access
# -----------------------------------------------------------------------------

# Get value at path (e.g., "user.address.city")
fn json_get_path(obj, path, default) {
    if default == none { default = none }
    
    let parts = __py_import__("str").split(path, ".")
    let current = obj
    
    for part in parts {
        if current == none { return default }
        
        # Handle array index
        if __py_import__("str").startswith(part, "[") and __py_import__("str").endswith(part, "]") {
            let index = __py_import__("int")(__py_import__("str")[1:-1])
            if __py_import__("isinstance")(current, __py_import__("list")) {
                if index >= 0 and index < len(current) {
                    current = current[index]
                } else {
                    return default
                }
            } else {
                return default
            }
        } else {
            if __py_import__("isinstance")(current, __py_import__("dict")) {
                if part in current {
                    current = current[part]
                } else {
                    return default
                }
            } else {
                return default
            }
        }
    }
    
    return current
}

# Set value at path
fn json_set_path(obj, path, value) {
    let parts = __py_import__("str").split(path, ".")
    let current = obj
    
    let i = 0
    loop {
        if i >= len(parts) - 1 { break }
        let part = parts[i]
        
        if part in current {
            current = current[part]
        } else {
            current[part] = {}
            current = current[part]
        }
        i = i + 1
    }
    
    current[parts[len(parts) - 1]] = value
    return obj
}

# Delete value at path
fn json_delete_path(obj, path) {
    let parts = __py_import__("str").split(path, ".")
    let current = obj
    
    let i = 0
    loop {
        if i >= len(parts) - 1 { break }
        let part = parts[i]
        
        if part in current {
            current = current[part]
        } else {
            return obj
        }
        i = i + 1
    }
    
    let last_key = parts[len(parts) - 1]
    if last_key in current {
        # Delete key (Python del)
        __py_import__("del")(current[last_key])
    }
    
    return obj
}

# Check if path exists
fn json_has_path(obj, path) {
    let result = json_get_path(obj, path, __py_import__("object")())
    return result != __py_import__("object")()
}

# -----------------------------------------------------------------------------
# Query Operations
# -----------------------------------------------------------------------------

# Find all values matching a key
fn json_find_all(obj, key) {
    let results = []
    
    fn _search(current) {
        if __py_import__("isinstance")(current, __py_import__("dict")) {
            for k in current {
                if k == key {
                    results[len(results)] = current[k]
                }
                _search(current[k])
            }
        } elif __py_import__("isinstance")(current, __py_import__("list")) {
            for item in current {
                _search(item)
            }
        }
    }
    
    _search(obj)
    return results
}

# Get all keys at depth
fn json_keys_at_depth(obj, depth) {
    if depth == none { depth = 1 }
    let keys = []
    
    fn _collect(current, current_depth) {
        if current_depth > depth { return }
        
        if __py_import__("isinstance")(current, __py_import__("dict")) {
            if current_depth == depth {
                for k in current {
                    keys[len(keys)] = k
                }
            } else {
                for k in current {
                    _collect(current[k], current_depth + 1)
                }
            }
        }
    }
    
    _collect(obj, 1)
    return keys
}

# Count occurrences of key
fn json_count_key(obj, key) {
    let count = 0
    
    fn _count(current) {
        if __py_import__("isinstance")(current, __py_import__("dict")) {
            for k in current {
                if k == key { count = count + 1 }
                _count(current[k])
            }
        } elif __py_import__("isinstance")(current, __py_import__("list")) {
            for item in current {
                _count(item)
            }
        }
    }
    
    _count(obj)
    return count
}

# -----------------------------------------------------------------------------
# Transformation
# -----------------------------------------------------------------------------

# Deep merge two JSON objects
fn json_merge(obj1, obj2) {
    let result = {}
    
    for key in obj1 {
        result[key] = obj1[key]
    }
    
    for key in obj2 {
        let val2 = obj2[key]
        if key in result {
            let val1 = result[key]
            if __py_import__("isinstance")(val1, __py_import__("dict")) and 
               __py_import__("isinstance")(val2, __py_import__("dict")) {
                result[key] = json_merge(val1, val2)
            } else {
                result[key] = val2
            }
        } else {
            result[key] = val2
        }
    }
    
    return result
}

# Deep clone
fn json_clone(obj) {
    return __py_import__("copy").deepcopy(obj)
}

# Map over all values
fn json_map_values(obj, fn) {
    if __py_import__("isinstance")(obj, __py_import__("dict")) {
        let result = {}
        for key in obj {
            result[key] = json_map_values(obj[key], fn)
        }
        return result
    } elif __py_import__("isinstance")(obj, __py_import__("list")) {
        let result = []
        let i = 0
        for item in obj {
            result[i] = json_map_values(item, fn)
            i = i + 1
        }
        return result
    } else {
        return fn(obj)
    }
}

# Filter keys
fn json_filter_keys(obj, predicate) {
    let result = {}
    for key in obj {
        if predicate(key) {
            result[key] = obj[key]
        }
    }
    return result
}

# Pick specific keys
fn json_pick(obj, keys) {
    let result = {}
    for key in keys {
        if key in obj {
            result[key] = obj[key]
        }
    }
    return result
}

# Omit specific keys
fn json_omit(obj, keys) {
    let result = {}
    for key in obj {
        let found = false
        for k in keys {
            if k == key {
                found = true
                break
            }
        }
        if not found {
            result[key] = obj[key]
        }
    }
    return result
}

# -----------------------------------------------------------------------------
# Diff Operations
# -----------------------------------------------------------------------------

# Compare two JSON objects
fn json_diff(obj1, obj2) {
    let added = {}
    let removed = {}
    let changed = {}
    
    # Find added and changed
    for key in obj2 {
        if not (key in obj1) {
            added[key] = obj2[key]
        } elif obj1[key] != obj2[key] {
            changed[key] = {"old": obj1[key], "new": obj2[key]}
        }
    }
    
    # Find removed
    for key in obj1 {
        if not (key in obj2) {
            removed[key] = obj1[key]
        }
    }
    
    return {
        "added": added,
        "removed": removed,
        "changed": changed
    }
}

# Check if two JSON objects are equal
fn json_equals(obj1, obj2) {
    return obj1 == obj2
}

# -----------------------------------------------------------------------------
# Export all
# -----------------------------------------------------------------------------

export json_parse, json_stringify, json_pretty, json_compact
export json_read_file, json_write_file
export json_is_valid, json_type
export json_get_path, json_set_path, json_delete_path, json_has_path
export json_find_all, json_keys_at_depth, json_count_key
export json_merge, json_clone, json_map_values, json_filter_keys
export json_pick, json_omit
export json_diff, json_equals
