
import pdfplumber
import re


pdf_path = "data/LinkedInCV.pdf"


with pdfplumber.open(pdf_path) as pdf:
    
    # get number of pages 
    for page_num, page in enumerate(pdf.pages, start=1):
        print(f"\n--- Page {page_num} ---")

    # Extract words with positional info
    lines = page.extract_text(layout=True).split('\n')
    for i, line in enumerate(lines):
        print(f"Line {i+1}: {line}")



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
                    # No visible gap — use indentation heuristic
                    leading_spaces = len(raw_line) - len(raw_line.lstrip())

                    if leading_spaces >= indent_threshold:
                        left = ""
                        right = split_line[0]
                    else:
                        left = split_line[0]
                        right = ""
                else:
                    # More than 2 segments — treat first as left, rest as right
                    left = split_line[0]
                    right = " ".join(split_line[1:])
                    
                structured_lines.append({
                    "left": left.strip(),
                    "right": right.strip()
                })

    return structured_lines

lines = extract_by_visual_gap(pdf_path)

def split_columns(lines):
    column_1 = [line['left'] for line in lines if line['left'].strip()]
    column_2 = [line['right'] for line in lines if line['right'].strip()]
    return column_1, column_2
column_1, column_2 = split_columns(lines)

























