#NLP-POWERED-RESUME-PARSER
==========================

This project provides a lightweight pipeline to extract and clean structured resume data from PDF files using layout-aware parsing and rule-based cleanup.

------------
📁 Structure
------------
- /data
  - PDF resumes to be parsed

- /parser_utils
  - `pdf_parser.py`: Extracts text from PDFs using visual gap logic
  - `text_utils.py`: Provides helper methods to clean and organize parsed resume content
  - `__init__.py`: Exposes the utilities for import

- main.py
  - Main driver script to:
    1. Load a resume PDF
    2. Extract lines
    3. Split into visual columns
    4. Group by resume sections
    5. Clean up date/duration artifacts
    6. Clean formatting issues

----------------
🚀 Getting Started
----------------
1. Install dependencies (if needed):
   pip install pdfplumber

2. Place your resume PDFs into the `data/` folder.

3. Run the main script:
   python main.py

4. Check the cleaned, sectioned resume output via the `sections_cleaned` variable.
