from parser_utils import ResumeREADER
from parser_utils import TextUtils
from parser_utils import CleaningUtils
from parser_utils import ExtractionUtils
from parser_utils import CVFormatter


# Instantiate classes
utils = TextUtils()
cleaner = CleaningUtils()
extractor = ExtractionUtils()


""" TEST 2-columns
resume_reader = ResumeREADER("data/sample_2.pdf", strategy="columns")
lines = resume_reader.structured_lines
column_1, column_2 = utils.split_columns(lines)

# extract CV sections independently from both columns
sections_1 = utils.group_sections_from_single_column(column_1)
sections_2 = utils.group_sections_from_single_column(column_2)
    # Merge the grouped sections from both columns
sections = utils.merge_section_dicts(sections_1, sections_2)

"""



resume_reader = ResumeREADER("data/sample_1.pdf")
lines = resume_reader.structured_lines

# initial clean
lines = [cleaner.initial_cleaner(line) for line in lines]

# extract CV sections 
sections = utils.group_sections_from_single_column(lines)

""" parsing contact info """
contact_info = utils.parse_contact_block(sections.get("contact", []))


""" parsing education """
education_section = sections["Education"]  
education_info = extractor.parse_education_section(education_section)


""" parsing experience """ 
experience_section = sections["Experience"]  
experience_info = extractor.parse_experience_section(experience_section)
approx_years = extractor.estimate_years_of_experience(experience_section)


""" formatter """
formatter = CVFormatter(contact_info, education_info, experience_info)
structured_output = formatter.to_dict()
    # visualization
formatter.display_cv_info(structured_output, approx_years)











# Clean out date ranges and durations from section content
sections_no_date = cleaner.clean_all_sections_dates(sections)

# Apply general text cleanup to remove artifacts, empty lines, etc.
sections_cleaned = cleaner.clean_all_sections(sections_no_date)

# extract keywords and erase the rest
compressed_sections = {
    section: cleaner.compress_section_to_keywords(lines)
    for section, lines in sections_cleaned.items()
}












