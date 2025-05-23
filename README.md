NLP-POWERED-RESUME-PARSER
==========================

An intelligent resume parsing tool using NLP techniques to extract structured information  from PDF resumes.

------------
📁 Project Structure
------------
```text
NLP-POWERED-RESUME-PARSER/
│
├── data/
│ ├── sample_1.pdf        # Single-column layout resume
│ └── sample_2.pdf        # Multi-column layout resume
│
├── parser_utils/         # Core logic for parsing resumes
│ ├── init.py
│ ├── cleaning_utils.py   # Text preprocessing and cleaning utilities
│ ├── cvformatter.py      # Format extracted data into a dictionary or readable format
│ ├── extraction_utils.py # Education, experience, and skills extraction logic
│ ├── resume_reader.py    # PDF reading and layout-specific text structuring
│ └── text_utils.py       # Section splitting and contact parsing
│
├── main.py               # the pipeline script
├── .gitignore
└── README.md
```

## 🚀 Features
- Extracts structured information from resumes:
  - 📇 Contact Information
  - 🎓 Education History
  - 💼 Work Experience
  - 💪 Skill Set
  - 🧮 Years of Experience
- Handles different resume layouts: `"single"` and `"column"`
- Outputs results in a formatted structure for easy consumption

## 🧠 Core Technologies

- Python
- NLP-based text segmentation and pattern matching
- PDF text extraction
- Regex and rule-based parsing
