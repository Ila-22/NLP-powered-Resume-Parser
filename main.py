from parser_utils import ResumeREADER
from parser_utils import TextUtils
from parser_utils import CleaningUtils
from parser_utils import ExtractionUtils
from parser_utils import CVFormatter


# Instantiate classes
cleaner = CleaningUtils()
extractor = ExtractionUtils()


""" CV reader + cleanser """
CV_format = "single" # either "single" or "column" layout
resume_reader = ResumeREADER("data/sample_1.pdf", CV_format=CV_format)
lines = resume_reader.structured_lines
    # initial cleaning
lines = cleaner.clean_lines(lines, CV_format=CV_format)


""" extract CV sections """ 
utils = TextUtils(CV_format=CV_format)
sections = utils.get_sections(lines)


""" parsing contact info """
contact_info = utils.parse_contact_block(sections.get("contact", []))


""" parsing education """
education_section = sections["Education"]  
education_info = extractor.parse_education_section(education_section)


""" parsing experience """ 
experience_section = sections["Experience"]  
experience_info = extractor.parse_experience_section(experience_section)
approx_years = extractor.estimate_years_of_experience(experience_section)


""" parsing skills """
skill_section = sections["Skills"]  
skill_set = extractor.extract_skills(skill_section)


""" formatter """
formatter = CVFormatter(contact_info, education_info, experience_info, skill_set)
structured_output = formatter.to_dict()
    # visualization
formatter.display_cv_info(structured_output, approx_years)


#cleaner.compress_section_to_keywords(skill_section)








