from parser_utils.pdf_parser import extract_by_visual_gap
from parser_utils.text_utils import split_columns

pdf_path = "data/LinkedInCV.pdf"

lines = extract_by_visual_gap(pdf_path)
column_1, column_2 = split_columns(lines)

# Example output
print("--- Column 1 ---")
for line in column_1:
    print(line)

print("\n--- Column 2 ---")
for line in column_2:
    print(line)























