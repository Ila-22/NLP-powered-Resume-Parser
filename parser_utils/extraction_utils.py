
from datetime import datetime
import dateparser
import re 

class ExtractionUtils:
    """ Extraction-focused utilities """
    def __init__(self):
        pass


    def parse_experience_section(self, lines):
        experiences = []
        current_exp = {}
        current_description = []

        # Regex to identify new experience entries
        job_header_pattern = re.compile(
            r'^(?P<company>.+?)\s*\|\s*(?P<role>.+?)\s+(?P<start_month>\w+)\s+(?P<start_year>\d{4})\s*[–-]\s*(?P<end_month>\w+)?\s*(?P<end_year>\d{4}|Present)?',
            re.IGNORECASE
        )

        for line in lines:
            match = job_header_pattern.match(line)
            if match:
                # Save previous job experience if it exists
                if current_exp:
                    current_exp["responsibilities"] = current_description
                    experiences.append(current_exp)

                # Start a new job experience
                current_exp = {
                    "company": match.group("company").strip(),
                    "role": match.group("role").strip(),
                    "start_date": f"{match.group('start_month')} {match.group('start_year')}",
                    "end_date": f"{match.group('end_month')} {match.group('end_year')}" if match.group("end_month") and match.group("end_year") else "Present",
                }
                current_description = []
            else:
                if current_exp:
                    current_description.append(line.strip())

        # Add the last experience
        if current_exp:
            current_exp["responsibilities"] = current_description
            experiences.append(current_exp)

        return experiences


    def estimate_years_of_experience(self, text_lines):
        """
        Extracts and calculates total years of experience from a list of text lines.
        Recognizes flexible date formats like:
        - March 2020 - July 2023
        - Jan 2018 - Present
        - 2021 - 2023
        """
        date_ranges = []
        now = datetime.now()

        # Regex to match common date ranges
        date_pattern = re.compile(
            r"(?P<start>[\w]+\s+\d{4}|\d{4})\s*[-–—]\s*(?P<end>Present|[\w]+\s+\d{4}|\d{4})",
            re.IGNORECASE
        )

        for line in text_lines:
            for match in date_pattern.finditer(line):
                start_str = match.group("start")
                end_str = match.group("end")

                start_date = dateparser.parse(start_str)
                end_date = now if "present" in end_str.lower() else dateparser.parse(end_str)

                if start_date and end_date and end_date > start_date:
                    duration_years = (end_date - start_date).days / 365.25
                    date_ranges.append(duration_years)

        total_experience = sum(date_ranges)
        return round(total_experience, 1)
        

    def parse_education_section(self, lines):
        education_entries = []
        current_entry = {}
        additional_info = []

        # Pattern to detect main education line
        edu_header_pattern = re.compile(
            r'^(?P<institution>.+?),\s*(?P<degree>.+?)\s+(?P<start_month>\w+)\s+(?P<start_year>\d{4})\s*[–-]\s*(?P<end_month>\w+)?\s*(?P<end_year>\d{4}|Present)?',
            re.IGNORECASE
        )

        for line in lines:
            match = edu_header_pattern.match(line)
            if match:
                # Save the previous education entry
                if current_entry:
                    current_entry['details'] = additional_info
                    education_entries.append(current_entry)

                # Start a new one
                current_entry = {
                    "institution": match.group("institution").strip(),
                    "degree": match.group("degree").strip(),
                    "start_date": f"{match.group('start_month')} {match.group('start_year')}",
                    "end_date": f"{match.group('end_month')} {match.group('end_year')}" if match.group("end_month") and match.group("end_year") else "Present",
                }
                additional_info = []
            else:
                if current_entry:
                    additional_info.append(line.strip())

        # Append the last entry
        if current_entry:
            current_entry["details"] = additional_info
            education_entries.append(current_entry)

        return education_entries


    def extract_skills(self, lines):
        skills = []

        for line in lines:
            # Remove category prefix if present
            if ":" in line:
                _, skill_part = line.split(":", 1)
            else:
                skill_part = line

            # Split by comma, clean spacing
            skill_list = [s.strip() for s in skill_part.split(",") if s.strip()]
            skills.extend(skill_list)

        return sorted(set(skills)) 

