# MyLang Test File
# Demonstrates all language features

# =============================================================================
# Variables
# =============================================================================

let name = "MyLang"
let version = 1.0
const PI = 3.14159

print("=== Variables ===")
print("Name:", name)
print("Version:", version)
print("PI:", PI)

# =============================================================================
# Data Types
# =============================================================================

print("\n=== Data Types ===")
let num = 42
let float_num = 3.14
let text = "Hello, World!"
let is_active = true
let items = [1, 2, 3, 4, 5]
let person = {"name": "John", "age": 30}

print("Number:", num)
print("Float:", float_num)
print("String:", text)
print("Boolean:", is_active)
print("List:", items)
print("Dict:", person)

# =============================================================================
# Functions
# =============================================================================

print("\n=== Functions ===")

fn greet(name) {
    print("Hello, " + name + "!")
}

fn add(a, b) {
    return a + b
}

fn factorial(n) {
    if n <= 1 {
        return 1
    }
    return n * factorial(n - 1)
}

greet("Developer")
print("5 + 3 =", add(5, 3))
print("Factorial of 5:", factorial(5))

# =============================================================================
# Conditionals
# =============================================================================

print("\n=== Conditionals ===")

let score = 85

if score >= 90 {
    print("Grade: A")
} elif score >= 80 {
    print("Grade: B")
} elif score >= 70 {
    print("Grade: C")
} else {
    print("Grade: F")
}

# =============================================================================
# Loops
# =============================================================================

print("\n=== Loops ===")

print("For loop:")
for i in range(5) {
    print("  i =", i)
}

print("While loop:")
let count = 0
while count < 3 {
    print("  count =", count)
    count = count + 1
}

print("Loop with range:")
loop i in range(3) {
    print("  iteration", i)
}

# =============================================================================
# List Operations
# =============================================================================

print("\n=== List Operations ===")

let numbers = [1, 2, 3, 4, 5]

print("Original list:", numbers)
print("First element:", numbers[0])
print("Length:", len(numbers))

# List comprehension
let squares = [x * x for x in numbers]
print("Squares:", squares)

# Filter
let evens = [x for x in numbers if x % 2 == 0]
print("Evens:", evens)

# =============================================================================
# Dictionary Operations
# =============================================================================

print("\n=== Dictionary Operations ===")

let user = {"name": "Alice", "age": 25, "city": "NYC"}

print("User:", user)
print("Name:", user["name"])
print("Keys:", keys(user))
print("Values:", values(user))

# =============================================================================
# Classes
# =============================================================================

print("\n=== Classes ===")

class Animal {
    name = "Unknown"

    fn __init__(name) {
        self.name = name
    }

    fn speak() {
        print(self.name, "makes a sound")
    }
}

class Dog extends Animal {
    fn speak() {
        print(self.name, "says: Woof!")
    }

    fn fetch() {
        print(self.name, "is fetching the ball")
    }
}

let dog = Dog("Buddy")
dog.speak()
dog.fetch()

# =============================================================================
# Error Handling
# =============================================================================

print("\n=== Error Handling ===")

fn divide(a, b) {
    try {
        if b == 0 {
            throw "Division by zero"
        }
        return a / b
    } catch(e) {
        print("Error:", e)
        return none
    }
}

print("10 / 2 =", divide(10, 2))
print("10 / 0 =", divide(10, 0))

# =============================================================================
# Built-in Functions
# =============================================================================

print("\n=== Built-in Functions ===")

print("abs(-5):", abs(-5))
print("min(3, 1, 4):", min(3, 1, 4))
print("max(3, 1, 4):", max(3, 1, 4))
print("sum([1,2,3,4,5]):", sum([1, 2, 3, 4, 5]))
print("sorted([3,1,4,1,5]):", sorted([3, 1, 4, 1, 5]))

# =============================================================================
# Math Functions
# =============================================================================

print("\n=== Math Functions ===")

print("sqrt(16):", sqrt(16))
print("pow(2, 8):", pow(2, 8))
print("floor(3.7):", floor(3.7))
print("ceil(3.2):", ceil(3.2))

# =============================================================================
# String Operations
# =============================================================================

print("\n=== String Operations ===")

let s = "Hello, MyLang!"

print("Original:", s)
print("Length:", len(s))
print("Upper:", upper(s))
print("Lower:", lower(s))
print("Replace:", replace(s, "MyLang", "World"))

# =============================================================================
# JSON Operations
# =============================================================================

print("\n=== JSON Operations ===")

let data = {"name": "Test", "values": [1, 2, 3]}
let json_str = stringifyJSON(data)
print("To JSON:", json_str)

# =============================================================================
# Summary
# =============================================================================

print("\n=== All Tests Passed! ===")
print("MyLang is working correctly!")
