import json

patterns = [
    r"\"card\"\\s*:\\s*\"(\d{16})\"",
    r"\"name\"\\s*:\\s*\"(.*)\""
]

test_str = json.dumps(patterns)
print("test_str =", test_str)
parsed = json.loads(test_str)
print("parsed =", parsed)
