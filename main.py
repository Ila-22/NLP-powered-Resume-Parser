from parser_utils import TextUtils, left_right_column_format, mixed_paragraph_and_column_layout

# Instantiate the utility class
utils = TextUtils()


#### TEST
lines = mixed_paragraph_and_column_layout("data/sample_2.pdf")
column_1, column_2 = utils.split_columns(lines)


import pdfplumber
with pdfplumber.open("data/sample_2.pdf") as pdf:
    for page in pdf.pages:
        words = page.extract_words()
    
        # Group words by Y (top) line
        lines_by_y = {}
        for word in words:
            y = round(word["top"], 1)
            lines_by_y.setdefault(y, []).append(word)
    
        for y in sorted(lines_by_y):
            line_words = sorted(lines_by_y[y], key=lambda w: w["x0"])



# Set the path to the PDF resume
pdf_path = "data/sample_1.pdf"

# if two-column layout input
lines = left_right_column_format(pdf_path, column_gap=150)
column_1, column_2 = utils.split_columns(lines)


# extract CV sections independently from both columns
sections_1 = utils.group_sections_from_single_column(column_1)
sections_2 = utils.group_sections_from_single_column(column_2)
    # Merge the grouped sections from both columns
sections = utils.merge_section_dicts(sections_1, sections_2)

# estimate years of experience 
experience_section = sections["Experience"]  
approx_years = utils.estimate_years_of_experience(experience_section)
print(f"Estimated years of experience: {approx_years}")

# Clean out date ranges and durations from section content
sections_no_date = utils.clean_all_sections_dates(sections)

# Apply general text cleanup to remove artifacts, empty lines, etc.
sections_cleaned = utils.clean_all_sections(sections_no_date)














