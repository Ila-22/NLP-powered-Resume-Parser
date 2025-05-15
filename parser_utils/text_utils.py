import re
import dateparser
from datetime import datetime



class TextUtils:
    def __init__(self):
        pass

    def split_columns(self, lines):
        """
        Splits a list of line dicts into two separate columns.
        Filters out empty strings.
        """
        column_1 = [line['left'] for line in lines if line['left'].strip()]
        column_2 = [line['right'] for line in lines if line['right'].strip()]
        return column_1, column_2

    def group_sections_from_single_column(self, column, known_headers=None):
        """
        Groups lines under section headers from a single column.
        Headers must be explicitly listed in known_headers.
        """
        if known_headers is None:
            known_headers = {
                "Contact", "Experience", "Education", 
                "Certifications", "Top Skills", "Languages",
            }

        sections = {}
        current_section = None

        for line in column:
            line_clean = line.strip()
            if line_clean in known_headers:
                current_section = line_clean
                sections[current_section] = []
            elif current_section:
                sections[current_section].append(line_clean)

        return sections

    def merge_section_dicts(self, dict1, dict2):
        """
        Merges two section dictionaries by combining their lists of items.
        """
        merged = {}
        all_keys = set(dict1.keys()).union(dict2.keys())

        for key in all_keys:
            merged[key] = dict1.get(key, []) + dict2.get(key, [])

        return merged
    
    
    
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
            r"(?P<start>[\w]+\s+\d{4}|\d{4})\s*-\s*(?P<end>Present|[\w]+\s+\d{4}|\d{4})",
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
    

    def remove_dates_and_durations(self, text):
        """
        Removes date ranges and durations from a given text string.
        """
        date_range = r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|" \
                     r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)" \
                     r"\s+\d{4}\s*-\s*(?:Present|\w+\s+\d{4})"

        duration = r"\(\d+\s+(?:year|month)s?(?:\s+\d+\s+months?)?\)"

        cleaned = re.sub(f"{date_range}|{duration}", "", text)
        return cleaned.strip()
    

    def clean_all_sections_dates(self, sections_dict):
        """
        Removes dates and durations from all entries in all sections.
        Returns a new cleaned sections dictionary.
        """
        cleaned_dict = {}
        for section, items in sections_dict.items():
            cleaned_items = [self.remove_dates_and_durations(line) for line in items]
            cleaned_dict[section] = cleaned_items
        return cleaned_dict



    def clean_text_entries(self, items):
        """
        Cleans up a list of text items:
        - Removes empty strings and whitespace
        - Removes orphaned punctuation or parentheses
        - Cleans up artifacts like '· ()'
        """
        cleaned = []
        for item in items:
            # Step 1: Remove trailing orphaned symbols
            item = re.sub(r"[\s·•\-–—]*\(\s*\)", "", item)  # remove '· ()', ' - ()', etc.
            item = re.sub(r"[\s·•\-–—]+$", "", item)        # remove trailing dashes/bullets
            item = item.strip()
    
            # Step 2: Keep only meaningful lines
            if item and not re.fullmatch(r"[\W_]+", item):  # filter lines with only symbols
                cleaned.append(item)
    
        return cleaned


    
    def clean_all_sections(self, sections_dict):
        """
        Cleans all entries across all sections.
        Applies general text cleanup on top of date removal.
        """
        cleaned_all = {}
        for section, items in sections_dict.items():
            no_dates = [self.remove_dates_and_durations(line) for line in items]
            cleaned_items = self.clean_text_entries(no_dates)
            cleaned_all[section] = cleaned_items
        return cleaned_all

