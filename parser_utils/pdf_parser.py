import pdfplumber
import re

def extract_by_word_position(pdf_path, column_gap=200):
    """
    Extracts lines from PDF and splits into left/right columns
    based on word x-positions rather than spaces in text.
    * Use this method if the whole document is in a two-column 
        layout and can be split into two!
    """
    structured_lines = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words()

            # Group words by Y (top) line
            lines_by_y = {}
            for word in words:
                y = round(word["top"], 1)  # bucket lines
                lines_by_y.setdefault(y, []).append(word)

            for y in sorted(lines_by_y):
                left = []
                right = []
                for word in sorted(lines_by_y[y], key=lambda w: w["x0"]):
                    if word["x0"] < column_gap:
                        left.append(word["text"])
                    else:
                        right.append(word["text"])

                structured_lines.append({
                    "left": " ".join(left).strip(),
                    "right": " ".join(right).strip()
                })

    return structured_lines

