import json

with open("csharp_test_passport_benchmark.json", "r", encoding="utf-8") as f:
    cs_data = json.load(f)

for b in cs_data["passport-challenging-16.png"]["Blocks"]:
    if "GAIMU" in b["Text"] or "JPN" in b["Text"]:
        print("C# block:", b["Text"], "Score:", b["Score"])

for b in cs_data["passport-test-15.png"]["Blocks"]:
    if "SAKURA" in b["Text"] or "TR" in b["Text"]:
        print("C# block:", b["Text"], "Score:", b["Score"])
