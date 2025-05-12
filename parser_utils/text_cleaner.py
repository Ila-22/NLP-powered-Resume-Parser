import re
import string

class TextCleaner:

    def __init__(self, text):
        self.text = text

    def clean(self):
        text = self._remove_non_ascii(self.text)
        text = self._normalize_whitespace(text)
        text = self._strip_weird_characters(text)
        return text.strip()

    def _normalize_whitespace(self, text):
        # Keeps line breaks, but normalizes spaces around them
        text = re.sub(r'[ \t]+', ' ', text)        # collapse spaces/tabs
        text = re.sub(r'\s*\n\s*', '\n', text)     # tidy line breaks
        return text

    def _remove_non_ascii(self, text):
        return text.encode("ascii", errors="ignore").decode()

    def _strip_weird_characters(self, text):
        # Remove non-text clutter like multiple dashes, stars, etc.
        text = re.sub(r'[•●–—]', '-', text)
        return text