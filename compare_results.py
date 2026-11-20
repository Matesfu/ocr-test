import json
import re

with open("csharp_benchmark_results.json", "r", encoding="utf-8") as f:
    cs_data = json.load(f)

with open("python_v6_benchmark_results.json", "r", encoding="utf-8") as f:
    py_data = json.load(f)

def find_mrz_candidates(lines):
    mrz = []
    for l in lines:
        txt = l if isinstance(l, str) else l.get("Text", l.get("text", ""))
        # MRZ lines typically start with P< or have multiple < characters or are uppercase alphanumeric + <
        clean = txt.strip().replace(" ", "")
        if "P<" in clean or "<<" in clean or clean.count("<") >= 2 or (len(clean) >= 28 and re.match(r'^[A-Z0-9<]+$', clean)):
            mrz.append(txt)
    return mrz

print("=" * 80)
print(f"{'Image':<32} | {'C# Time':<8} | {'Py Time':<8} | Comparison")
print("=" * 80)

for img in cs_data:
    cs_entry = cs_data.get(img, {})
    py_entry = py_data.get(img, {})

    cs_time = cs_entry.get("TimeMs", 0)
    py_time = int(py_entry.get("time_ms", 0))

    cs_blocks = [b.get("Text", "") for b in cs_entry.get("Blocks", [])]
    py_blocks = [b.get("text", "") for b in py_entry.get("lines", [])]

    cs_mrz = find_mrz_candidates(cs_blocks)
    py_mrz = find_mrz_candidates(py_blocks)

    print(f"\n--- {img} --- (C#: {cs_time}ms | Py: {py_time}ms)")
    print("  [C# MRZ lines]:")
    for m in cs_mrz:
        print("    ", m)
    if not cs_mrz:
        print("    (No specific MRZ pattern detected - all lines:)")
        for l in cs_blocks[-4:]:
            print("      ", l)

    print("  [Python MRZ lines]:")
    for m in py_mrz:
        print("    ", m)
    if not py_mrz:
        print("    (No specific MRZ pattern detected - all lines:)")
        for l in py_blocks[-4:]:
            print("      ", l)
