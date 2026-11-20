from rapidocr import RapidOCR

# Initializes the engine and auto-downloads the models on the first run
engine = RapidOCR()

passports = ["passport-test-3.png", "passport-test-2.png", "dim-pasport-test4.png"]

for img_path in passports:
    print(f"\n--- Scanning {img_path} ---")
    result = engine(img_path)
    
    if result.txts:
        for text, score in zip(result.txts, result.scores):
            print(f"[{score:.2f}] {text}")
            
    # Saves an annotated image showing the detected bounding boxes
    result.vis(f"vis_{img_path}")
