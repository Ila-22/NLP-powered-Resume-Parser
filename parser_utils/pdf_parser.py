import pdfplumber


def mixed_paragraph_and_column_layout(pdf_path, line_tolerance=8, gap_threshold=50):
    """
    Smart extractor that:
    1. Clusters words into lines with vertical tolerance.
    2. Splits lines into columns only if a wide horizontal gap exists.
    """
    structured_lines = []

    def cluster_words_into_lines(words, tolerance):
        """Group words into lines by 'top' position using tolerance."""
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

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words()
            lines = cluster_words_into_lines(words, line_tolerance)

            for line_words in lines:
                # Calculate gaps
                line_words = sorted(line_words, key=lambda w: w["x0"])
                gaps = [
                    line_words[i+1]["x0"] - line_words[i]["x1"]
                    for i in range(len(line_words) - 1)
                ]
                max_gap = max(gaps) if gaps else 0

                if max_gap > gap_threshold:
                    # Column layout
                    split_index = gaps.index(max_gap) + 1
                    left_words = line_words[:split_index]
                    right_words = line_words[split_index:]

                    structured_lines.append({
                        "left": " ".join(w["text"] for w in left_words).strip(),
                        "right": " ".join(w["text"] for w in right_words).strip()
                    })
                else:
                    # Paragraph
                    full_line = " ".join(w["text"] for w in line_words).strip()
                    structured_lines.append({
                        "left": full_line,
                        "right": ""
                    })

    return structured_lines





def left_right_column_format(pdf_path, column_gap=200):
    """
    Extracts lines from PDF and splits into left/right columns
    based on word x-positions rather than spaces in text.
    * Use this method if the whole document is in a two-column 
        layout and can be split into two!
    """
    structured_lines = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words()

            # Group words by Y (top) line
            lines_by_y = {}
            for word in words:
                y = round(word["top"], 1)  # bucket lines
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

