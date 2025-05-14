import pdfplumber
import re

def extract_by_visual_gap(pdf_path, gap_spaces=6, indent_threshold=6):
    structured_lines = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            print(f"\n--- Page {page_num} ---")
            text = page.extract_text(layout=True)
            if not text:
                continue

            for raw_line in text.split("\n"):
                stripped_line = raw_line.strip()
                
                # Use gap-based splitting first
                split_line = re.split(r'\s{' + str(gap_spaces) + r',}', stripped_line)
                if len(split_line) == 2:
                    left, right = split_line
                elif len(split_line) == 1:
                    leading_spaces = len(raw_line) - len(raw_line.lstrip())
                    if leading_spaces >= indent_threshold:
                        left = ""
                        right = split_line[0]
                    else:
                        left = split_line[0]
                        right = ""
                else:
                    left = split_line[0]
                    right = " ".join(split_line[1:])
                    
                structured_lines.append({
                    "left": left.strip(),
                    "right": right.strip()
                })

    return structured_lines
