import spacy
import re

class NERExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")

    def extract_entities(self, text):
        doc = self.nlp(text)
        entities = {
            "name": self._extract_name(doc),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "organizations": self._extract_by_label(doc, "ORG"),
            "titles": self._extract_by_label(doc, "JOB_TITLE"),
            "dates": self._extract_by_label(doc, "DATE"),
        }
        return entities

    def _extract_email(self, text):
        match = re.search(r'[\w\.-]+@[\w\.-]+', text)
        return match.group(0) if match else None

    def _extract_phone(self, text):
        match = re.search(r'(\+?\d{1,3}[\s\-]?)?\(?\d{2,4}\)?[\s\-]?\d{3,5}[\s\-]?\d{3,5}', text)
        return match.group(0) if match else None

    def _extract_name(self, doc):
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return None

    def _extract_by_label(self, doc, label):
        return list({ent.text for ent in doc.ents if ent.label_ == label})
