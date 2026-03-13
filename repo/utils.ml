# =============================================================================
# MyLang Utils Package v1.0.0
# =============================================================================
# General utility functions for MyLang
# Author: MyLang Team
# Repository: https://github.com/Botan-linux/mylang
# =============================================================================

# -----------------------------------------------------------------------------
# String Utilities
# -----------------------------------------------------------------------------

# Split a string by delimiter
fn str_split(str, delimiter) {
    return __py_import__("str").split(str, delimiter)
}

# Join array elements with delimiter
fn str_join(arr, delimiter) {
    return __py_import__("str").join(delimiter, arr)
}

# Trim whitespace from both ends
fn str_trim(str) {
    return __py_import__("str").strip(str)
}

# Check if string starts with prefix
fn str_starts_with(str, prefix) {
    return __py_import__("str").startswith(str, prefix)
}

# Check if string ends with suffix
fn str_ends_with(str, suffix) {
    return __py_import__("str").endswith(str, suffix)
}

# Replace all occurrences
fn str_replace(str, old, new) {
    return __py_import__("str").replace(str, old, new)
}

# Convert to lowercase
fn str_lower(str) {
    return __py_import__("str").lower(str)
}

# Convert to uppercase
fn str_upper(str) {
    return __py_import__("str").upper(str)
}

# Reverse a string
fn str_reverse(str) {
    return __py_import__("str")[::-1] if len(str) > 0 else str
}

# Check if string contains substring
fn str_contains(str, substring) {
    return __py_import__("in").__contains__(substring, str)
}

# Get character at index
fn str_char_at(str, index) {
    if index < 0 or index >= len(str) {
        return none
    }
    return str[index]
}

# Repeat string n times
fn str_repeat(str, n) {
    let result = ""
    let i = 0
    loop {
        if i >= n { break }
        result = result + str
        i = i + 1
    }
    return result
}

# Pad string left
fn str_pad_left(str, length, pad_char) {
    if pad_char == none { pad_char = " " }
    let diff = length - len(str)
    if diff <= 0 { return str }
    return str_repeat(pad_char, diff) + str
}

# Pad string right
fn str_pad_right(str, length, pad_char) {
    if pad_char == none { pad_char = " " }
    let diff = length - len(str)
    if diff <= 0 { return str }
    return str + str_repeat(pad_char, diff)
}

# -----------------------------------------------------------------------------
# Array Utilities
# -----------------------------------------------------------------------------

# Get first element
fn arr_first(arr) {
    if len(arr) == 0 { return none }
    return arr[0]
}

# Get last element
fn arr_last(arr) {
    if len(arr) == 0 { return none }
    return arr[len(arr) - 1]
}

# Check if array is empty
fn arr_is_empty(arr) {
    return len(arr) == 0
}

# Push element to end
fn arr_push(arr, element) {
    arr[len(arr)] = element
    return arr
}

# Pop last element
fn arr_pop(arr) {
    if len(arr) == 0 { return none }
    let last = arr[len(arr) - 1]
    # Remove last element (create new array without it)
    let result = []
    let i = 0
    loop {
        if i >= len(arr) - 1 { break }
        result[i] = arr[i]
        i = i + 1
    }
    return result
}

# Reverse array
fn arr_reverse(arr) {
    let result = []
    let i = len(arr) - 1
    loop {
        if i < 0 { break }
        result[len(result)] = arr[i]
        i = i - 1
    }
    return result
}

# Check if element exists in array
fn arr_contains(arr, element) {
    for item in arr {
        if item == element { return true }
    }
    return false
}

# Find index of element
fn arr_index_of(arr, element) {
    let i = 0
    for item in arr {
        if item == element { return i }
        i = i + 1
    }
    return -1
}

# Remove element at index
fn arr_remove_at(arr, index) {
    if index < 0 or index >= len(arr) { return arr }
    let result = []
    let j = 0
    let i = 0
    loop {
        if i >= len(arr) { break }
        if i != index {
            result[j] = arr[i]
            j = j + 1
        }
        i = i + 1
    }
    return result
}

# Insert element at index
fn arr_insert(arr, index, element) {
    if index < 0 { index = 0 }
    if index > len(arr) { index = len(arr) }
    let result = []
    let j = 0
    let i = 0
    loop {
        if i > len(arr) { break }
        if i == index {
            result[j] = element
            j = j + 1
        }
        if i < len(arr) {
            result[j] = arr[i]
            j = j + 1
        }
        i = i + 1
    }
    return result
}

# Flatten nested array
fn arr_flatten(arr) {
    let result = []
    for item in arr {
        if __py_import__("isinstance")(item, __py_import__("list")) {
            let flattened = arr_flatten(item)
            for sub_item in flattened {
                result[len(result)] = sub_item
            }
        } else {
            result[len(result)] = item
        }
    }
    return result
}

# Get unique elements
fn arr_unique(arr) {
    let result = []
    let seen = {}
    for item in arr {
        let key = __py_import__("str")(item)
        if seen[key] == none {
            seen[key] = true
            result[len(result)] = item
        }
    }
    return result
}

# Take first n elements
fn arr_take(arr, n) {
    let result = []
    let i = 0
    loop {
        if i >= n or i >= len(arr) { break }
        result[i] = arr[i]
        i = i + 1
    }
    return result
}

# Skip first n elements
fn arr_skip(arr, n) {
    let result = []
    let j = 0
    let i = n
    loop {
        if i >= len(arr) { break }
        result[j] = arr[i]
        j = j + 1
        i = i + 1
    }
    return result
}

# -----------------------------------------------------------------------------
# Math Utilities
# -----------------------------------------------------------------------------

# Absolute value
fn math_abs(n) {
    if n < 0 { return -n }
    return n
}

# Power function
fn math_pow(base, exp) {
    return __py_import__("pow")(base, exp)
}

# Square root
fn math_sqrt(n) {
    return __py_import__("math").sqrt(n)
}

# Floor
fn math_floor(n) {
    return __py_import__("math").floor(n)
}

# Ceiling
fn math_ceil(n) {
    return __py_import__("math").ceil(n)
}

# Round
fn math_round(n, decimals) {
    if decimals == none { decimals = 0 }
    return __py_import__("round")(n, decimals)
}

# Minimum
fn math_min(arr) {
    if len(arr) == 0 { return none }
    let min_val = arr[0]
    for item in arr {
        if item < min_val { min_val = item }
    }
    return min_val
}

# Maximum
fn math_max(arr) {
    if len(arr) == 0 { return none }
    let max_val = arr[0]
    for item in arr {
        if item > max_val { max_val = item }
    }
    return max_val
}

# Sum
fn math_sum(arr) {
    let total = 0
    for item in arr {
        total = total + item
    }
    return total
}

# Average
fn math_avg(arr) {
    if len(arr) == 0 { return 0 }
    return math_sum(arr) / len(arr)
}

# Random integer between min and max
fn math_random_int(min, max) {
    return __py_import__("random").randint(min, max)
}

# Random float between 0 and 1
fn math_random() {
    return __py_import__("random").random()
}

# Clamp value between min and max
fn math_clamp(n, min_val, max_val) {
    if n < min_val { return min_val }
    if n > max_val { return max_val }
    return n
}

# Check if number is even
fn math_is_even(n) {
    return n % 2 == 0
}

# Check if number is odd
fn math_is_odd(n) {
    return n % 2 != 0
}

# Factorial
fn math_factorial(n) {
    if n <= 1 { return 1 }
    let result = 1
    let i = 2
    loop {
        if i > n { break }
        result = result * i
        i = i + 1
    }
    return result
}

# Fibonacci
fn math_fibonacci(n) {
    if n <= 0 { return 0 }
    if n == 1 { return 1 }
    let a = 0
    let b = 1
    let i = 2
    loop {
        if i > n { break }
        let temp = a + b
        a = b
        b = temp
        i = i + 1
    }
    return b
}

# GCD (Greatest Common Divisor)
fn math_gcd(a, b) {
    while b != 0 {
        let temp = b
        b = a % b
        a = temp
    }
    return a
}

# LCM (Least Common Multiple)
fn math_lcm(a, b) {
    return math_abs(a * b) / math_gcd(a, b)
}

# -----------------------------------------------------------------------------
# Object/Dict Utilities
# -----------------------------------------------------------------------------

# Get all keys
fn obj_keys(obj) {
    return __py_import__("list")(obj.keys())
}

# Get all values
fn obj_values(obj) {
    return __py_import__("list")(obj.values())
}

# Check if key exists
fn obj_has_key(obj, key) {
    return key in obj
}

# Get value with default
fn obj_get(obj, key, default) {
    if obj[key] != none { return obj[key] }
    return default
}

# Merge two objects
fn obj_merge(obj1, obj2) {
    let result = {}
    for key in obj_keys(obj1) {
        result[key] = obj1[key]
    }
    for key in obj_keys(obj2) {
        result[key] = obj2[key]
    }
    return result
}

# Deep clone object
fn obj_clone(obj) {
    return __py_import__("copy").deepcopy(obj)
}

# -----------------------------------------------------------------------------
# Type Utilities
# -----------------------------------------------------------------------------

# Check type
fn is_string(val) {
    return __py_import__("isinstance")(val, __py_import__("str"))
}

fn is_number(val) {
    return __py_import__("isinstance")(val, __py_import__("numbers").Number)
}

fn is_array(val) {
    return __py_import__("isinstance")(val, __py_import__("list"))
}

fn is_dict(val) {
    return __py_import__("isinstance")(val, __py_import__("dict"))
}

fn is_bool(val) {
    return __py_import__("isinstance")(val, __py_import__("bool"))
}

fn is_none(val) {
    return val == none
}

fn is_function(val) {
    return __py_import__("callable")(val)
}

# Convert to string
fn to_string(val) {
    return __py_import__("str")(val)
}

# Convert to number
fn to_number(str) {
    return __py_import__("float")(str)
}

# Convert to int
fn to_int(str) {
    return __py_import__("int")(str)
}

# -----------------------------------------------------------------------------
# Time Utilities
# -----------------------------------------------------------------------------

# Get current timestamp
fn time_now() {
    return __py_import__("time").time()
}

# Format timestamp
fn time_format(timestamp, format_str) {
    if timestamp == none { timestamp = time_now() }
    if format_str == none { format_str = "%Y-%m-%d %H:%M:%S" }
    return __py_import__("datetime").datetime.fromtimestamp(timestamp).strftime(format_str)
}

# Sleep for seconds
fn time_sleep(seconds) {
    __py_import__("time").sleep(seconds)
}

# Measure execution time
fn time_it(fn, args) {
    let start = time_now()
    let result = fn(args)
    let end = time_now()
    return { "result": result, "time": end - start }
}

# -----------------------------------------------------------------------------
# Validation Utilities
# -----------------------------------------------------------------------------

# Check if email is valid (basic)
fn is_email(str) {
    return str_contains(str, "@") and str_contains(str, ".")
}

# Check if string is numeric
fn is_numeric(str) {
    try {
        __py_import__("float")(str)
        return true
    } catch(e) {
        return false
    }
}

# Check if string is alphanumeric
fn is_alphanumeric(str) {
    return __py_import__("str").isalnum(str)
}

# Check if string is alphabetic
fn is_alpha(str) {
    return __py_import__("str").isalpha(str)
}

# -----------------------------------------------------------------------------
# Functional Utilities
# -----------------------------------------------------------------------------

# Map function over array
fn func_map(arr, fn) {
    let result = []
    let i = 0
    for item in arr {
        result[i] = fn(item)
        i = i + 1
    }
    return result
}

# Filter array
fn func_filter(arr, predicate) {
    let result = []
    for item in arr {
        if predicate(item) {
            result[len(result)] = item
        }
    }
    return result
}

# Reduce array
fn func_reduce(arr, fn, initial) {
    let acc = initial
    for item in arr {
        acc = fn(acc, item)
    }
    return acc
}

# Find first match
fn func_find(arr, predicate) {
    for item in arr {
        if predicate(item) { return item }
    }
    return none
}

# Check if all match
fn func_every(arr, predicate) {
    for item in arr {
        if not predicate(item) { return false }
    }
    return true
}

# Check if any match
fn func_some(arr, predicate) {
    for item in arr {
        if predicate(item) { return true }
    }
    return false
}

# Compose functions (right to left)
fn func_compose(fns) {
    return fn(x) {
        let result = x
        let reversed = arr_reverse(fns)
        for fn_item in reversed {
            result = fn_item(result)
        }
        return result
    }
}

# Pipe functions (left to right)
fn func_pipe(fns) {
    return fn(x) {
        let result = x
        for fn_item in fns {
            result = fn_item(result)
        }
        return result
    }
}

# Curry a function
fn func_curry(fn, arity) {
    if arity == none { arity = 2 }
    return fn(a) {
        return fn(b) {
            return fn(a, b)
        }
    }
}

# Partial application
fn func_partial(fn, fixed_args) {
    return fn(remaining_args) {
        let all_args = []
        for arg in fixed_args {
            all_args[len(all_args)] = arg
        }
        for arg in remaining_args {
            all_args[len(all_args)] = arg
        }
        return fn(all_args)
    }
}

# -----------------------------------------------------------------------------
# Export all functions
# -----------------------------------------------------------------------------

export str_split, str_join, str_trim, str_starts_with, str_ends_with
export str_replace, str_lower, str_upper, str_reverse, str_contains
export str_char_at, str_repeat, str_pad_left, str_pad_right

export arr_first, arr_last, arr_is_empty, arr_push, arr_pop
export arr_reverse, arr_contains, arr_index_of, arr_remove_at, arr_insert
export arr_flatten, arr_unique, arr_take, arr_skip

export math_abs, math_pow, math_sqrt, math_floor, math_ceil
export math_round, math_min, math_max, math_sum, math_avg
export math_random_int, math_random, math_clamp
export math_is_even, math_is_odd, math_factorial, math_fibonacci
export math_gcd, math_lcm

export obj_keys, obj_values, obj_has_key, obj_get, obj_merge, obj_clone

export is_string, is_number, is_array, is_dict, is_bool, is_none, is_function
export to_string, to_number, to_int

export time_now, time_format, time_sleep, time_it

export is_email, is_numeric, is_alphanumeric, is_alpha

export func_map, func_filter, func_reduce, func_find
export func_every, func_some, func_compose, func_pipe, func_curry, func_partial
