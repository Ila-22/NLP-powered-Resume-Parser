import pdfplumber
import re

class PDFTextExtractor:
    
    def __init__(self, pdf_path, strategy="single"):
        """
        Initializes and loads the PDF.
        Strategy options:
        - "auto": intelligently picks best layout method
        - "mixed": allows paragraphs and columns
        - "columns": assumes full two-column layout
        """
        self.pdf_path = pdf_path
        self.strategy = strategy.lower()
        self.pdf = pdfplumber.open(pdf_path)

        # Extract upon initialization
        self.structured_lines = self._run_extraction()
        

    def _run_extraction(self):
        if self.strategy == "columns":
            return self.left_right_column_format()
        elif self.strategy == "mixed":
            return self.mixed_paragraph_and_column_layout()
        elif self.strategy == "single":
            return self.extract_lines_from_pdf()
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")
        

    def extract_lines_from_pdf(self):
        lines = []

        for page in self.pdf.pages:
            raw_text = page.extract_text()
            if not raw_text:
                continue

            page_lines = raw_text.split('\n')
            for line in page_lines:
                clean_line = re.sub(r'\s+', ' ', line.strip())
                if clean_line and not self.is_noise_line(clean_line):
                    lines.append(clean_line)

        return lines

    def is_noise_line(self, line):
        # Heuristic filters for headers, footers, or urls
        noise_patterns = [
            r'^page \d+ of \d+$',
            r'^www\.', r'^https?://',
            r'linkedin\.com', r'^mailto:',
        ]
        return any(re.search(p, line.lower()) for p in noise_patterns)



    def mixed_paragraph_and_column_layout(self, line_tolerance=8, gap_threshold=50, known_headers=None):
        """
        Smart extractor that:
        1. Clusters words into lines with vertical tolerance.
        2. Splits lines into columns only if a wide horizontal gap exists.
        """
        structured_lines = []
        
        # Use the default header map
        if known_headers is None:
            known_headers = {
                "Contact": ["contact", "contact info", "contact information"],
                "Experience": ["experience", "work experience", "professional experience", "experiences"],
                "Education": ["education", "academic background", "educational background"],
                "Certifications": ["certifications", "certification", "licenses"],
                "Top Skills": ["top skills", "skills", "technical skills", "key skills"],
                "Languages": ["languages", "language proficiency"],
                "Portfolio": ["portfolio", "projects"],
                "About Me": ["about me", "summary", "professional summary", "profile"]
            }
    
        all_header_variants = set()
        for variants in known_headers.values():
            all_header_variants.update(variant.lower() for variant in variants)


        def cluster_words_into_lines(words, tolerance):
            lines = []
            words = sorted(words, key=lambda w: (w["top"], w["x0"]))
            current_line = []
            current_top = None

            for word in words:
                if current_top is None or abs(word["top"] - current_top) <= tolerance:
                    current_line.append(word)
                    current_top = word["top"] if current_top is None else min(current_top, word["top"])
                else:
                    lines.append(current_line)
                    current_line = [word]
                    current_top = word["top"]
            if current_line:
                lines.append(current_line)
            return lines

        for page in self.pdf.pages:
            words = page.extract_words()
            lines = cluster_words_into_lines(words, line_tolerance)

            for line_words in lines:
                line_words = sorted(line_words, key=lambda w: w["x0"])
                text_line = " ".join(w["text"] for w in line_words).strip().lower()

                # when 2 or more headers seen in a line >> split sections
                matched_headers = [
                    h for h in all_header_variants if h in text_line
                ]

                if len(matched_headers) >= 2:
                    # Force a semantic split based on matched headers
                    first = matched_headers[0]
                    second = matched_headers[1]
                    structured_lines.append({
                        "left": first.title(),
                        "right": second.title()
                    })
                    continue
                
                # Otherwise, use gap-based logic
                gaps = [
                    line_words[i+1]["x0"] - line_words[i]["x1"]
                    for i in range(len(line_words) - 1)
                ]
                max_gap = max(gaps) if gaps else 0

                if max_gap > gap_threshold:
                    split_index = gaps.index(max_gap) + 1
                    left_words = line_words[:split_index]
                    right_words = line_words[split_index:]

                    structured_lines.append({
                        "left": " ".join(w["text"] for w in left_words).strip(),
                        "right": " ".join(w["text"] for w in right_words).strip()
                    })
                else:
                    full_line = " ".join(w["text"] for w in line_words).strip()
                    structured_lines.append({"left": full_line, "right": ""})

        return structured_lines
    

    def left_right_column_format(self, column_gap=150):
        """
        Extracts text assuming a strict left-right column layout.
        Use this when the entire document follows column structure.
        """
        structured_lines = []

        for page in self.pdf.pages:
            words = page.extract_words()
            lines_by_y = {}

            for word in words:
                y = round(word["top"], 1)
                lines_by_y.setdefault(y, []).append(word)

            for y in sorted(lines_by_y):
                left = []
                right = []
                for word in sorted(lines_by_y[y], key=lambda w: w["x0"]):
                    if word["x0"] < column_gap:
                        left.append(word["text"])
                    else:
                        right.append(word["text"])

                structured_lines.append({
                    "left": " ".join(left).strip(),
                    "right": " ".join(right).strip()
                })

        return structured_lines
    
    
    def merge_adjacent_header_lines(lines, known_headers=None):
        """
        Merges consecutive header-only lines into a single left-right structured line.
        Only merges when both lines contain nothing but known headers.
        """
        if known_headers is None:
            known_headers = {
                "Contact", "Experience", "Education",
                "Certifications", "Top Skills", "Languages",
                "Portfolio", "About Me", "Projects"
            }
    
        headers_normalized = {h.lower() for h in known_headers}
        merged_lines = []
        i = 0
    
        while i < len(lines):
            line = lines[i]
            left = line.get("left", "").strip()
            right = line.get("right", "").strip()
    
            is_left_header_only = left.lower() in headers_normalized and not right
            is_right_header_only = right.lower() in headers_normalized and not left
    
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                next_left = next_line.get("left", "").strip()
                next_right = next_line.get("right", "").strip()
    
                is_next_left_header_only = next_left.lower() in headers_normalized and not next_right
                is_next_right_header_only = next_right.lower() in headers_normalized and not next_left
    
                if is_left_header_only and is_next_left_header_only:
                    merged_lines.append({
                        "left": left,
                        "right": next_left
                    })
                    i += 2
                    continue
                elif is_right_header_only and is_next_right_header_only:
                    merged_lines.append({
                        "left": right,
                        "right": next_right
                    })
                    i += 2
                    continue
    
            # Default: keep line
            merged_lines.append(line)
            i += 1
    
        return merged_lines

