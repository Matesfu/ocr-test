import json

with open("test_passport_mrz_analysis.json", "r", encoding="utf-8") as f:
    records = json.load(f)

for r in records:
    if not r["identical"]:
        print("=" * 80)
        print(f"IMAGE: {r['image']}")
        print("  C# MRZ:")
        for m in r["cs_mrz"]:
            print("    ", m)
        print("  Python MRZ:")
        for m in r["py_mrz"]:
            print("    ", m)
        print("\n  C# ALL LINES:")
        for l in r["cs_all"][-6:]:
            print("    ", l)
        print("  Py ALL LINES:")
        for l in r["py_all"][-6:]:
            print("    ", l)
