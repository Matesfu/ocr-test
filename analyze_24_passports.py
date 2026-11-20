import json
import re

with open("csharp_test_passport_benchmark.json", "r", encoding="utf-8") as f:
    cs_data = json.load(f)

with open("python_test_passport_benchmark.json", "r", encoding="utf-8") as f:
    py_data = json.load(f)

def extract_mrz_lines(blocks):
    mrz = []
    for b in blocks:
        txt = b if isinstance(b, str) else b.get("Text", b.get("text", ""))
        clean = txt.strip().replace(" ", "")
        # ICAO Doc 9303 Type 3 passports have 2 lines of 44 chars each.
        # Often starts with P< or has multiple <<
        if len(clean) >= 20 and (clean.startswith("P<") or clean.startswith("P") or "<<" in clean or clean.count("<") >= 2):
            # check if it looks like an MRZ line (alphanumeric + <)
            if re.match(r'^[A-Z0-9<]+$', clean):
                mrz.append((txt, clean))
    return mrz

print(f"{'Image Name':<35} | {'C# Time':<8} | {'Py Time':<8} | {'Match?':<12} | Details")
print("-" * 110)

cs_total_time = 0
py_total_time = 0
match_count = 0
total_images = len(cs_data)

detailed_records = []

for img_name in sorted(cs_data.keys()):
    cs_entry = cs_data.get(img_name, {})
    py_entry = py_data.get(img_name, {})

    cs_t = cs_entry.get("TimeMs", 0)
    py_t = int(py_entry.get("time_ms", 0))

    cs_total_time += cs_t
    py_total_time += py_t

    cs_blocks = [b.get("Text", "") for b in cs_entry.get("Blocks", [])]
    py_blocks = [b.get("text", "") for b in py_entry.get("lines", [])]

    cs_mrz = extract_mrz_lines(cs_blocks)
    py_mrz = extract_mrz_lines(py_blocks)

    cs_mrz_texts = [m[0] for m in cs_mrz]
    py_mrz_texts = [m[0] for m in py_mrz]

    is_identical = (cs_mrz_texts == py_mrz_texts)
    if is_identical:
        match_count += 1

    status = "IDENTICAL" if is_identical else "DIFFERENT"
    print(f"{img_name:<35} | {cs_t:>5} ms | {py_t:>5} ms | {status:<12} | Lines: CS={len(cs_mrz_texts)}, Py={len(py_mrz_texts)}")

    detailed_records.append({
        "image": img_name,
        "cs_time": cs_t,
        "py_time": py_t,
        "identical": is_identical,
        "cs_mrz": cs_mrz_texts,
        "py_mrz": py_mrz_texts,
        "cs_all": cs_blocks,
        "py_all": py_blocks
    })

print("-" * 110)
print(f"Summary: {match_count}/{total_images} MRZ outputs identical.")
print(f"Total Inference Time: C# = {cs_total_time} ms, Python = {py_total_time} ms (C# is {((py_total_time - cs_total_time)/py_total_time)*100:.1f}% faster)")

with open("test_passport_mrz_analysis.json", "w", encoding="utf-8") as f:
    json.dump(detailed_records, f, ensure_ascii=False, indent=2)
