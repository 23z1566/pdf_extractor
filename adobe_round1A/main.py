import fitz
import os
import json
from heading_extractor import extract_headings

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdfs = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    for pdf_name in pdfs:
        pdf_path = os.path.join(INPUT_DIR, pdf_name)
        doc = fitz.open(pdf_path)
        result = extract_headings(doc)
        out_path = os.path.join(OUTPUT_DIR, os.path.splitext(pdf_name)[0] + ".json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Processed: {pdf_name} -> {os.path.basename(out_path)}")
