
from datetime import datetime
import dateparser
import re 

class ExtractionUtils:
    """ Extraction-focused utilities """
    def __init__(self):
        pass

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
        






