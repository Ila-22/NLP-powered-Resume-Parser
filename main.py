from parser_utils.file_reader import FileReader
from parser_utils.text_cleaner import TextCleaner


file_path = "data/LinkedInCV.pdf"  # Change to .docx or .txt if needed


try:
    # read file
    reader = FileReader(file_path)
    raw_text = reader.read()

    cleaner = TextCleaner(raw_text)
    text = cleaner.clean()
    
    print("cleaned Resume Text:\n")
    print(text)  
except Exception as e:
    print(f"Error reading file: {e}")