from parser_utils import TextUtils, extract_by_visual_gap

# Instantiate the utility class
utils = TextUtils()

# Set the path to the PDF resume
pdf_path = "data/LinkedInCV.pdf"

# Extract lines from the PDF using visual gap and indentation logic
lines = extract_by_visual_gap(pdf_path, gap_spaces=4, indent_threshold=4)

# Split extracted lines into two logical columns based on layout
column_1, column_2 = utils.split_columns(lines)

# extract CV sections independently from both columns
sections_1 = utils.group_sections_from_single_column(column_1)
sections_2 = utils.group_sections_from_single_column(column_2)
    # Merge the grouped sections from both columns
sections = utils.merge_section_dicts(sections_1, sections_2)

# Clean out date ranges and durations from section content
sections_no_date = utils.clean_all_sections_dates(sections)

# Apply general text cleanup to remove artifacts, empty lines, etc.
sections_cleaned = utils.clean_all_sections(sections_no_date)














