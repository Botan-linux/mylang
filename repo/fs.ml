# =============================================================================
# MyLang File System Package v1.0.0
# =============================================================================
# File system utilities for MyLang
# Author: MyLang Team
# Repository: https://github.com/Botan-linux/mylang
# =============================================================================

let _os = __py_import__("os")
let _shutil = __py_import__("shutil")
let _path = __py_import__("os.path")
let _glob = __py_import__("glob")

# -----------------------------------------------------------------------------
# Path Utilities
# -----------------------------------------------------------------------------

# Join paths
fn path_join(paths) {
    return _path.join(*paths)
}

# Get absolute path
fn path_abs(path) {
    return _path.abspath(path)
}

# Get directory name
fn path_dirname(path) {
    return _path.dirname(path)
}

# Get file name
fn path_basename(path) {
    return _path.basename(path)
}

# Get file extension
fn path_extname(path) {
    let name = path_basename(path)
    let dot_index = __py_import__("str").rfind(name, ".")
    if dot_index > 0 {
        return __py_import__("str")(name[dot_index:])
    }
    return ""
}

# Get file name without extension
fn path_stem(path) {
    let name = path_basename(path)
    let ext = path_extname(path)
    if ext != "" {
        return __py_import__("str")(name[:-len(ext)])
    }
    return name
}

# Normalize path
fn path_normalize(path) {
    return _path.normpath(path)
}

# Get relative path
fn path_relative(from_path, to_path) {
    return _path.relpath(to_path, from_path)
}

# Split path into parts
fn path_split(path) {
    return _path.split(path)
}

# Check if path is absolute
fn path_is_absolute(path) {
    return _path.isabs(path)
}

# -----------------------------------------------------------------------------
# File Operations
# -----------------------------------------------------------------------------

# Read file content
fn file_read(filepath, encoding) {
    if encoding == none { encoding = "utf-8" }
    try {
        let _f = __py_import__("open")(filepath, "r", encoding=encoding)
        let content = _f.read()
        _f.close()
        return content
    } catch(e) {
        return none
    }
}

# Write to file
fn file_write(filepath, content, encoding) {
    if encoding == none { encoding = "utf-8" }
    try {
        let _f = __py_import__("open")(filepath, "w", encoding=encoding)
        _f.write(content)
        _f.close()
        return true
    } catch(e) {
        return false
    }
}

# Append to file
fn file_append(filepath, content, encoding) {
    if encoding == none { encoding = "utf-8" }
    try {
        let _f = __py_import__("open")(filepath, "a", encoding=encoding)
        _f.write(content)
        _f.close()
        return true
    } catch(e) {
        return false
    }
}

# Read file as lines
fn file_read_lines(filepath, encoding) {
    if encoding == none { encoding = "utf-8" }
    try {
        let _f = __py_import__("open")(filepath, "r", encoding=encoding)
        let lines = _f.readlines()
        _f.close()
        # Strip newline characters
        let result = []
        let i = 0
        for line in lines {
            result[i] = __py_import__("str").rstrip(line, "\n\r")
            i = i + 1
        }
        return result
    } catch(e) {
        return []
    }
}

# Write lines to file
fn file_write_lines(filepath, lines, encoding) {
    if encoding == none { encoding = "utf-8" }
    try {
        let _f = __py_import__("open")(filepath, "w", encoding=encoding)
        for line in lines {
            _f.write(line + "\n")
        }
        _f.close()
        return true
    } catch(e) {
        return false
    }
}

# Read binary file
fn file_read_binary(filepath) {
    try {
        let _f = __py_import__("open")(filepath, "rb")
        let content = _f.read()
        _f.close()
        return content
    } catch(e) {
        return none
    }
}

# Write binary file
fn file_write_binary(filepath, content) {
    try {
        let _f = __py_import__("open")(filepath, "wb")
        _f.write(content)
        _f.close()
        return true
    } catch(e) {
        return false
    }
}

# Copy file
fn file_copy(src, dst) {
    try {
        _shutil.copy2(src, dst)
        return true
    } catch(e) {
        return false
    }
}

# Move file
fn file_move(src, dst) {
    try {
        _shutil.move(src, dst)
        return true
    } catch(e) {
        return false
    }
}

# Delete file
fn file_delete(filepath) {
    try {
        _os.remove(filepath)
        return true
    } catch(e) {
        return false
    }
}

# Check if file exists
fn file_exists(filepath) {
    return _path.isfile(filepath)
}

# Get file size in bytes
fn file_size(filepath) {
    try {
        return _os.path.getsize(filepath)
    } catch(e) {
        return -1
    }
}

# Get file modification time
fn file_mtime(filepath) {
    try {
        return _os.path.getmtime(filepath)
    } catch(e) {
        return -1
    }
}

# Get file creation time
fn file_ctime(filepath) {
    try {
        return _os.path.getctime(filepath)
    } catch(e) {
        return -1
    }
}

# Touch file (create if not exists, update mtime if exists)
fn file_touch(filepath) {
    try {
        let _f = __py_import__("open")(filepath, "a")
        _f.close()
        return true
    } catch(e) {
        return false
    }
}

# -----------------------------------------------------------------------------
# Directory Operations
# -----------------------------------------------------------------------------

# Create directory
fn dir_create(path) {
    try {
        _os.makedirs(path, exist_ok=true)
        return true
    } catch(e) {
        return false
    }
}

# Create directory (only if parent exists)
fn dir_create_single(path) {
    try {
        _os.mkdir(path)
        return true
    } catch(e) {
        return false
    }
}

# Remove empty directory
fn dir_remove(path) {
    try {
        _os.rmdir(path)
        return true
    } catch(e) {
        return false
    }
}

# Remove directory and all contents
fn dir_remove_all(path) {
    try {
        _shutil.rmtree(path)
        return true
    } catch(e) {
        return false
    }
}

# Check if directory exists
fn dir_exists(path) {
    return _path.isdir(path)
}

# List directory contents
fn dir_list(path) {
    try {
        return _os.listdir(path)
    } catch(e) {
        return []
    }
}

# List only files in directory
fn dir_list_files(path) {
    let files = []
    try {
        for item in _os.listdir(path) {
            let full_path = _path.join(path, item)
            if _path.isfile(full_path) {
                files[len(files)] = item
            }
        }
    } catch(e) {}
    return files
}

# List only directories in directory
fn dir_list_dirs(path) {
    let dirs = []
    try {
        for item in _os.listdir(path) {
            let full_path = _path.join(path, item)
            if _path.isdir(full_path) {
                dirs[len(dirs)] = item
            }
        }
    } catch(e) {}
    return dirs
}

# List files recursively
fn dir_list_recursive(path) {
    let files = []
    try {
        for root, dirs, filenames in _os.walk(path) {
            for filename in filenames {
                files[len(files)] = _path.join(root, filename)
            }
        }
    } catch(e) {}
    return files
}

# Copy directory
fn dir_copy(src, dst) {
    try {
        _shutil.copytree(src, dst)
        return true
    } catch(e) {
        return false
    }
}

# Get current working directory
fn dir_cwd() {
    return _os.getcwd()
}

# Change working directory
fn dir_chdir(path) {
    try {
        _os.chdir(path)
        return true
    } catch(e) {
        return false
    }
}

# Get home directory
fn dir_home() {
    return _path.expanduser("~")
}

# Get temp directory
fn dir_temp() {
    return _os.tempdir if hasattr(_os, "tempdir") else "/tmp"
}

# -----------------------------------------------------------------------------
# Path Checks
# -----------------------------------------------------------------------------

# Check if path exists (file or directory)
fn fs_exists(path) {
    return _path.exists(path)
}

# Check if path is file
fn fs_is_file(path) {
    return _path.isfile(path)
}

# Check if path is directory
fn fs_is_dir(path) {
    return _path.isdir(path)
}

# Check if path is symlink
fn fs_is_symlink(path) {
    return _path.islink(path)
}

# Check if path is mount point
fn fs_is_mount(path) {
    return _path.ismount(path)
}

# -----------------------------------------------------------------------------
# Glob Pattern Matching
# -----------------------------------------------------------------------------

# Find files matching pattern
fn fs_glob(pattern) {
    return _glob.glob(pattern)
}

# Find files matching pattern (recursive)
fn fs_glob_recursive(pattern) {
    return _glob.glob(pattern, recursive=true)
}

# Find all Python files
fn fs_find_python(dir) {
    return fs_glob(path_join([dir, "**", "*.py"]))
}

# Find all files with extension
fn fs_find_by_ext(dir, ext) {
    if not __py_import__("str").startswith(ext, ".") {
        ext = "." + ext
    }
    return fs_glob(path_join([dir, "**", "*" + ext]))
}

# -----------------------------------------------------------------------------
# File Permissions
# -----------------------------------------------------------------------------

# Get file permissions
fn fs_get_permissions(path) {
    try {
        return _os.stat(path).st_mode & 0o777
    } catch(e) {
        return -1
    }
}

# Set file permissions
fn fs_set_permissions(path, mode) {
    try {
        _os.chmod(path, mode)
        return true
    } catch(e) {
        return false
    }
}

# Make file executable
fn fs_make_executable(path) {
    try {
        let current = fs_get_permissions(path)
        _os.chmod(path, current | 0o111)
        return true
    } catch(e) {
        return false
    }
}

# Make file read-only
fn fs_make_readonly(path) {
    try {
        let current = fs_get_permissions(path)
        _os.chmod(path, current & 0o444)
        return true
    } catch(e) {
        return false
    }
}

# -----------------------------------------------------------------------------
# File Info
# -----------------------------------------------------------------------------

class FileInfo {
    fn new(path) {
        self.path = path
        self.name = path_basename(path)
        self.ext = path_extname(path)
        self.stem = path_stem(path)
        
        let stat = _os.stat(path) if fs_exists(path) else none
        if stat != none {
            self.size = stat.st_size
            self.mtime = stat.st_mtime
            self.ctime = stat.st_ctime
            self.mode = stat.st_mode
            self.is_file = _path.isfile(path)
            self.is_dir = _path.isdir(path)
        } else {
            self.size = 0
            self.mtime = 0
            self.ctime = 0
            self.mode = 0
            self.is_file = false
            self.is_dir = false
        }
        return self
    }
    
    fn exists() {
        return fs_exists(self.path)
    }
    
    fn is_readable() {
        try {
            let _f = __py_import__("open")(self.path, "r")
            _f.close()
            return true
        } catch(e) {
            return false
        }
    }
    
    fn is_writable() {
        try {
            let _f = __py_import__("open")(self.path, "a")
            _f.close()
            return true
        } catch(e) {
            return false
        }
    }
    
    fn is_executable() {
        return _os.access(self.path, _os.X_OK)
    }
    
    fn size_human() {
        let size = self.size
        let units = ["B", "KB", "MB", "GB", "TB"]
        let i = 0
        loop {
            if i >= len(units) - 1 or size < 1024 { break }
            size = size / 1024
            i = i + 1
        }
        return __py_import__("round")(size, 2) + " " + units[i]
    }
}

# -----------------------------------------------------------------------------
# Temporary Files
# -----------------------------------------------------------------------------

let _tempfile = __py_import__("tempfile")

# Create temporary file
fn temp_file(suffix, prefix) {
    if suffix == none { suffix = "" }
    if prefix == none { prefix = "mylang_" }
    try {
        let _f = _tempfile.NamedTemporaryFile(suffix=suffix, prefix=prefix, delete=false)
        let path = _f.name
        _f.close()
        return path
    } catch(e) {
        return none
    }
}

# Create temporary directory
fn temp_dir(prefix) {
    if prefix == none { prefix = "mylang_" }
    try {
        return _tempfile.mkdtemp(prefix=prefix)
    } catch(e) {
        return none
    }
}

# -----------------------------------------------------------------------------
# Watch (Simple polling-based)
# -----------------------------------------------------------------------------

class FileWatcher {
    fn new(path, callback) {
        self.path = path
        self.callback = callback
        self.last_mtime = file_mtime(path)
        self.running = false
        return self
    }
    
    fn check() {
        let current_mtime = file_mtime(self.path)
        if current_mtime != self.last_mtime {
            self.last_mtime = current_mtime
            self.callback(self.path)
            return true
        }
        return false
    }
    
    fn start(interval) {
        if interval == none { interval = 1 }
        self.running = true
        while self.running {
            self.check()
            __py_import__("time").sleep(interval)
        }
    }
    
    fn stop() {
        self.running = false
    }
}

# -----------------------------------------------------------------------------
# Export all
# -----------------------------------------------------------------------------

export path_join, path_abs, path_dirname, path_basename
export path_extname, path_stem, path_normalize, path_relative
export path_split, path_is_absolute

export file_read, file_write, file_append
export file_read_lines, file_write_lines
export file_read_binary, file_write_binary
export file_copy, file_move, file_delete
export file_exists, file_size, file_mtime, file_ctime, file_touch

export dir_create, dir_create_single, dir_remove, dir_remove_all
export dir_exists, dir_list, dir_list_files, dir_list_dirs
export dir_list_recursive, dir_copy
export dir_cwd, dir_chdir, dir_home, dir_temp

export fs_exists, fs_is_file, fs_is_dir, fs_is_symlink, fs_is_mount
export fs_glob, fs_glob_recursive, fs_find_python, fs_find_by_ext
export fs_get_permissions, fs_set_permissions
export fs_make_executable, fs_make_readonly

export FileInfo
export temp_file, temp_dir
export FileWatcher
