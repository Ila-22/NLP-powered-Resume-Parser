
from nltk.corpus import stopwords
import nltk
import string 
import re

# run this only once
#nltk.download('stopwords')

class CleaningUtils:
    """ Functions that clean or normalize text """
    def __init__(self):
        pass

    def remove_dates_and_durations(self, text):
        """
        Removes date ranges and durations from a given text string.
        """
        date_range = r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|" \
                     r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)" \
                     r"\s+\d{4}\s*[-–—]\s*(?:Present|\w+\s+\d{4})"

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
    
    def compress_section_to_keywords(self, lines, min_word_length=3):
        """
        Filters out non-informative words and returns compressed content using only high-value terms.
        This works on any section format (paragraph, bullets, lists).
        """
        stop_words = set(stopwords.words("english"))
        keywords = []
    
        for line in lines:
            # Lowercase and tokenize
            tokens = re.findall(r'\b\w+\b', line.lower())
    
            # Filter
            filtered = [
                word for word in tokens
                if word not in stop_words
                and len(word) >= min_word_length
                and word not in string.punctuation
            ]
            keywords.extend(filtered)
    
        return sorted(set(keywords))
