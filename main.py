from parser_utils import TextUtils
from parser_utils.pdf_parser import PDFTextExtractor


# Instantiate the utility class
utils = TextUtils()


# Option 1: Auto-detect or mixed
extractor = PDFTextExtractor("data/sample_1.pdf", strategy="columns")
lines = extractor.structured_lines
column_1, column_2 = utils.split_columns(lines)


# Option 2: Auto-detect or mixed
extractor = PDFTextExtractor("data/sample_2.pdf", strategy="mixed")
lines = extractor.structured_lines
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














