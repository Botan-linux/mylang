# =============================================================================
# MyLang File System Package v1.0.0
# =============================================================================

let _os = __py_import__("os")
let _shutil = __py_import__("shutil")
let _path = __py_import__("os.path")

# Path Utilities
export fn path_join(a, b) {
    return _path.join(a, b)
}

export fn path_abs(path) {
    return _path.abspath(path)
}

export fn path_dirname(path) {
    return _path.dirname(path)
}

export fn path_basename(path) {
    return _path.basename(path)
}

export fn path_extname(path) {
    let name = path_basename(path)
    let dot_idx = __py_import__("str").rfind(name, ".")
    if dot_idx > 0 {
        let result = ""
        let i = dot_idx
        loop {
            if i >= len(name) { break }
            result = result + name[i]
            i = i + 1
        }
        return result
    }
    return ""
}

export fn path_exists(path) {
    return _path.exists(path)
}

export fn path_is_file(path) {
    return _path.isfile(path)
}

export fn path_is_dir(path) {
    return _path.isdir(path)
}

# File Operations
export fn file_read(filepath) {
    try {
        let f = __py_import__("open")(filepath, "r")
        let content = f.read()
        f.close()
        return content
    } catch(e) {
        return ""
    }
}

export fn file_write(filepath, content) {
    try {
        let f = __py_import__("open")(filepath, "w")
        f.write(content)
        f.close()
        return true
    } catch(e) {
        return false
    }
}

export fn file_append(filepath, content) {
    try {
        let f = __py_import__("open")(filepath, "a")
        f.write(content)
        f.close()
        return true
    } catch(e) {
        return false
    }
}

export fn file_exists(filepath) {
    return _path.isfile(filepath)
}

export fn file_delete(filepath) {
    try {
        _os.remove(filepath)
        return true
    } catch(e) {
        return false
    }
}

export fn file_copy(src, dst) {
    try {
        _shutil.copy2(src, dst)
        return true
    } catch(e) {
        return false
    }
}

export fn file_move(src, dst) {
    try {
        _shutil.move(src, dst)
        return true
    } catch(e) {
        return false
    }
}

export fn file_size(filepath) {
    try {
        return _os.path.getsize(filepath)
    } catch(e) {
        return -1
    }
}

# Directory Operations
export fn dir_create(path) {
    try {
        _os.makedirs(path)
        return true
    } catch(e) {
        return false
    }
}

export fn dir_exists(path) {
    return _path.isdir(path)
}

export fn dir_list(path) {
    try {
        return _os.listdir(path)
    } catch(e) {
        return []
    }
}

export fn dir_remove(path) {
    try {
        _shutil.rmtree(path)
        return true
    } catch(e) {
        return false
    }
}

export fn dir_cwd() {
    return _os.getcwd()
}

export fn dir_home() {
    return _path.expanduser("~")
}
