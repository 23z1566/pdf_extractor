import os
import json
import fitz  # PyMuPDF
from datetime import datetime

# --- Helper: Extract headings and their page numbers from a PDF ---
def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                line_text = " ".join(span["text"].strip() for span in line["spans"])
                if 6 < len(line_text) < 90 and not line_text.islower() and not line_text.isdigit():
                    size = max([span["size"] for span in line["spans"]])
                    headings.append({
                        "text": line_text.strip(),
                        "page": page_num + 1,
                        "size": size
                    })
    headings = sorted(headings, key=lambda x: (-x["size"], x["page"]))
    seen = set()
    deduped = []
    for h in headings:
        t = h["text"]
        if t not in seen:
            deduped.append(h)
            seen.add(t)
    return deduped

# --- Helper: Extract relevant paragraph under a heading ---
def extract_section_text(pdf_path, heading, page_number):
    doc = fitz.open(pdf_path)
    page = doc[page_number - 1]
    text = page.get_text()
    idx = text.lower().find(heading.lower())
    if idx == -1:
        return ""
    snippet = text[idx:]
    lines = snippet.splitlines()
    para = []
    for l in lines[1:]:
        if not l.strip() or (l.strip() == l.strip().upper() and len(l.strip()) < 100):
            break
        para.append(l.strip())
        if len(" ".join(para)) > 700:
            break
    return " ".join(para).strip()

def assign_importance(section_title):
    title = section_title.lower()
    if "guide" in title or "major cities" in title or "overview" in title:
        return 1
    if "things to do" in title or "coastal adventure" in title or "activities" in title:
        return 2
    if "cuisine" in title or "culinary" in title or "wine" in title:
        return 3
    if "tips" in title or "tricks" in title or "packing" in title:
        return 4
    if "nightlife" in title or "entertainment" in title:
        return 5
    return 10  # fallback

def main(input_json_path, pdf_dir, output_json_path):
    with open(input_json_path, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    metadata = {
        "input_documents": [d["filename"] for d in input_data["documents"]],
        "persona": input_data["persona"]["role"],
        "job_to_be_done": input_data["job_to_be_done"]["task"],
        "processing_timestamp": datetime.now().isoformat()
    }

    section_candidates = []
    for doc in input_data["documents"]:
        pdf_file = os.path.join(pdf_dir, doc["filename"])
        headings = extract_headings(pdf_file)
        for h in headings[:7]:
            rank = assign_importance(h["text"])
            if rank <= 5:
                section_candidates.append({
                    "document": doc["filename"],
                    "section_title": h["text"],
                    "importance_rank": rank,
                    "page_number": h["page"]
                })

    section_candidates = sorted(section_candidates, key=lambda x: (x["importance_rank"], x["page_number"]))
    extracted_sections = section_candidates[:5]

    subsection_analysis = []
    for sec in extracted_sections:
        refined_text = extract_section_text(
            os.path.join(pdf_dir, sec["document"]),
            sec["section_title"],
            sec["page_number"]
        )
        subsection_analysis.append({
            "document": sec["document"],
            "refined_text": refined_text,
            "page_number": sec["page_number"]
        })

    output = {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"Output written to {output_json_path}")

if __name__ == "__main__":
    main("challenge1b_input.json", "input", "challenge1b_output.json")
