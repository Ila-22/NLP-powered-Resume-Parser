class TextUtils:
    @staticmethod
    def split_columns(lines):
        """
        Splits a list of line dicts into two separate columns.
        Filters out empty strings.
        """
        column_1 = [line['left'] for line in lines if line['left'].strip()]
        column_2 = [line['right'] for line in lines if line['right'].strip()]
        return column_1, column_2

    @staticmethod
    def group_sections_from_single_column(column, known_headers=None):
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
