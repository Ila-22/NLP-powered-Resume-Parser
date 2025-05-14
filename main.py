

from parser_utils import TextUtils, extract_by_visual_gap


pdf_path = "data/LinkedInCV.pdf"

lines = extract_by_visual_gap(pdf_path, gap_spaces=4, indent_threshold=4)


column_1, column_2 = TextUtils.split_columns(lines)

sections_col1 = TextUtils.group_sections_from_single_column(column_1)
sections_col2 = TextUtils.group_sections_from_single_column(column_2)


















