import re
import dateparser
from datetime import datetime
from nltk.corpus import stopwords
import string
import nltk
import spacy

nlp = spacy.load("en_core_web_md")

# run this only once
#nltk.download('stopwords')



class TextUtils:
    """ General Text Utilities"""
    def __init__(self, strategy="single"):
        self.strategy = strategy

    def get_sections (self, lines):
        self.lines = lines
        if self.strategy == "single":
            sections = self.group_sections_from_single_column()
        return sections

    def split_columns(self, lines):
        """
        Splits a list of line dicts into two separate columns.
        Filters out empty strings.
        """
        column_1 = [line['left'] for line in lines if line['left'].strip()]
        column_2 = [line['right'] for line in lines if line['right'].strip()]
        return column_1, column_2


    def group_sections_from_single_column(self, known_headers=None):
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
            "Skills": ["top skills", "skills", "technical skills", "key skills", "Skills & abilities"],
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
    
        for line in self.lines:
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


    def contains_gpe(self, text):
        # (country/city/state)
        doc = nlp(text)
        return any(ent.label_ == "GPE" for ent in doc.ents)


    def parse_contact_block(self, lines):
        contact = {
            "name": None,
            "headline": None,
            "email": None,
            "phone": None,
            "linkedin": None,
            "address": None,
        }

        email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
        phone_pattern = re.compile(r'(\+?\d[\d\s\-()]{7,})')
        linkedin_pattern = re.compile(r'linkedin\.com\/[^\s|•–]+', re.IGNORECASE)

        # STEP 1: Flatten all fragments
        fragments = []
        for line in lines:
            fragments.extend(part.strip() for part in re.split(r'[|•–]', line) if part.strip())

        # STEP 2: Extract known fields
        unclassified = []

        for frag in fragments:
            if email_pattern.search(frag) and not contact["email"]:
                contact["email"] = email_pattern.search(frag).group()
            elif phone_pattern.search(frag) and not contact["phone"]:
                contact["phone"] = phone_pattern.search(frag).group()
            elif linkedin_pattern.search(frag) and not contact["linkedin"]:
                contact["linkedin"] = linkedin_pattern.search(frag).group()
            else:
                unclassified.append(frag)

        # STEP 3: Infer name, headline, address from leftovers
        for frag in unclassified:
            if not contact["name"] and re.match(r'^[A-Z][a-z]+(?: [A-Z][a-z]+){0,3}$', frag):
                contact["name"] = frag
            elif not contact["headline"] and len(frag.split()) <= 10 and len(frag) <= 80:
                contact["headline"] = frag
            elif not contact["address"] and self.contains_gpe(frag):
                contact["address"] = frag

        return contact


