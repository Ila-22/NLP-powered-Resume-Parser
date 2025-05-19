import re
import dateparser
from datetime import datetime
from nltk.corpus import stopwords
import string
import nltk

# run this only once
#nltk.download('stopwords')



class TextUtils:
    """ General Text Utilities"""
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
        Accepts flexible header names (e.g., 'Work Experience' → 'Experience').
        """
    
        # Canonical headers and their variants
        default_header_map = {
            "Contact": ["contact", "contact info", "contact information"],
            "Experience": ["experience", "work experience", "professional experience", "experiences"],
            "Education": ["education", "academic background", "educational background"],
            "Certifications": ["certifications", "certification", "licenses"],
            "Top Skills": ["top skills", "skills", "technical skills", "key skills", "Skills & abilities"],
            "Languages": ["languages", "language proficiency"],
            "Portfolio": ["portfolio", "projects"],
            "Summary": ["about me", "summary", "professional summary", "profile"]
        }
    
        if known_headers is None:
            known_headers = default_header_map
    
        # Reverse-lookup: flattened map of all variants
        variant_map = {}
        for canonical, variants in known_headers.items():
            for variant in variants:
                variant_map[variant.lower()] = canonical
    
        sections = {}
        current_section = None
        contact_lines = []
    
        for line in column:
            line_clean = line.strip()
            line_normalized = line_clean.lower()
    
            matched_header = variant_map.get(line_normalized)
    
            if matched_header:
                current_section = matched_header
                sections[current_section] = []
            elif current_section:
                sections[current_section].append(line_clean)
            else:
                contact_lines.append(line_clean)

            if contact_lines:
                sections["contact"] = contact_lines
    
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
    
    
    

