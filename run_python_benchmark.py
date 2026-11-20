import os
import json
import time
from rapidocr import RapidOCR

engine = RapidOCR()

images = [
    "kaleb-passport.jpg",
    "photo_2026-11-20_19-44-48.jpg",
    "photo_2026-11-20_19-45-08.jpg",
    "photo_2026-11-20_19-45-15.jpg",
    "photo_2026-11-20_19-45-22.jpg",
    "photo_2026-11-20_19-45-27.jpg",
    "photo_2026-11-20_19-45-33.jpg",
]

python_results = {}

for img in images:
    if not os.path.exists(img):
        continue
    
    t0 = time.time()
    out = engine(img)
    t_total = (time.time() - t0) * 1000

    lines = []
    if out and out.txts:
        for box, txt, score in zip(out.boxes, out.txts, out.scores):
            lines.append({
                "text": txt,
                "score": float(score),
                "box": box.tolist() if hasattr(box, 'tolist') else box
            })

    python_results[img] = {
        "time_ms": t_total,
        "elapse_list": out.elapse_list if out else [],
        "lines": lines
    }

with open("python_v6_benchmark_results.json", "w", encoding="utf-8") as f:
    json.dump(python_results, f, ensure_ascii=False, indent=2)

print("Python benchmark completed successfully!")
