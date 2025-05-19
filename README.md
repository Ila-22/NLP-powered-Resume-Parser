NLP-POWERED-RESUME-PARSER
==========================

A Python-based Natural Language Processing (NLP) tool designed to extract and analyze information from resume PDFs. This project automatically detects layout structures, estimates years of experience, cleans and compresses the extracted data for downstream processing and more!

------------
📁 Structure
------------
```text
NLP-POWERED-RESUME-PARSER
│
├── data/ # Sample resume PDFs
│ ├── sample_1.pdf
│ └── sample_2.pdf
│
├── parser_utils/ # Core utility modules
│ ├── init.py
│ ├── cleaning_utils.py
│ ├── extraction_utils.py
│ ├── pdf_parser.py
│ └── text_utils.py
│
├── .gitignore
├── main.py # Main script for parsing and analysis
└── README.md
```

----------------
📦 Dependencies
----------------
Make sure the following packages are installed:

- pdfplumber – for PDF text extraction

- nltk, spacy – for NLP tasks

- re, datetime – built-in, for regex/date processing

----------------
🧪 Samples
----------------
Sample resumes (sample_1.pdf, sample_2.pdf) are included in the data/ directory to test the pipeline.
