import os
import glob
import json
import time
from rapidocr import RapidOCR

engine = RapidOCR()

test_dir = r"test-passport"
image_files = sorted(glob.glob(os.path.join(test_dir, "*.*")))
image_files = [f for f in image_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

print(f"Found {len(image_files)} images in {test_dir}")

python_results = {}

for img_path in image_files:
    file_name = os.path.basename(img_path)
    try:
        t0 = time.time()
        out = engine(img_path)
        t_total = (time.time() - t0) * 1000

        lines = []
        if out and out.txts:
            for box, txt, score in zip(out.boxes, out.txts, out.scores):
                lines.append({
                    "text": txt,
                    "score": float(score),
                    "box": box.tolist() if hasattr(box, 'tolist') else box
                })

        python_results[file_name] = {
            "time_ms": t_total,
            "elapse_list": out.elapse_list if out else [],
            "lines": lines
        }
        print(f"[Python] {file_name}: {int(t_total)} ms, {len(lines)} lines")
    except Exception as e:
        print(f"[Python Error] {file_name}: {e}")
        python_results[file_name] = {"error": str(e)}

out_file = "python_test_passport_benchmark.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(python_results, f, ensure_ascii=False, indent=2)

print(f"Python benchmark completed. Saved {len(python_results)} results to {out_file}")
