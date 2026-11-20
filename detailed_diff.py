import json

with open("csharp_benchmark_results.json", "r", encoding="utf-8") as f:
    cs_data = json.load(f)

with open("python_v6_benchmark_results.json", "r", encoding="utf-8") as f:
    py_data = json.load(f)

diff_count = 0
total_lines = 0

for img in cs_data:
    cs_lines = [b["Text"] for b in cs_data[img].get("Blocks", [])]
    py_lines = [b["text"] for b in py_data[img].get("lines", [])]
    
    total_lines += max(len(cs_lines), len(py_lines))
    print(f"\n==================== {img} ====================")
    print(f"Counts: C# = {len(cs_lines)}, Python = {len(py_lines)}")
    
    min_len = min(len(cs_lines), len(py_lines))
    for i in range(min_len):
        if cs_lines[i] != py_lines[i]:
            diff_count += 1
            print(f"Diff @ {i}:")
            print(f"  C# : {cs_lines[i]}")
            print(f"  Py : {py_lines[i]}")
            
    if len(cs_lines) != len(py_lines):
        print(f"Line count mismatch! C# has {len(cs_lines)}, Py has {len(py_lines)}")
        if len(cs_lines) > len(py_lines):
            print("Extra in C#:", cs_lines[min_len:])
        else:
            print("Extra in Py:", py_lines[min_len:])

print(f"\nTotal differences detected: {diff_count} across {total_lines} lines.")
