# MyLang Package Test

import json
import fs
import datetime

# Test json
print("=== JSON Test ===")
let data = json.json_parse('{"name": "MyLang", "version": 1.0}')
print("Name: " + data["name"])
print("Pretty: " + json.json_pretty(data))

# Test fs
print("\n=== FS Test ===")
print("Home: " + fs.dir_home())
print("CWD: " + fs.dir_cwd())

# Test datetime
print("\n=== DateTime Test ===")
let now = datetime.datetime_now()
print("Now: " + now.format("%Y-%m-%d %H:%M:%S"))
print("Is weekend: " + now.is_weekend())

print("\n=== All Tests Passed! ===")
