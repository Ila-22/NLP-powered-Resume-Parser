from parser_utils.file_reader import FileReader
from parser_utils.text_cleaner import TextCleaner
from parser_utils.ner_extractor import NERExtractor


file_path = "data/LinkedInCV.pdf"  # Change to .docx or .txt if needed


try:
    # read file
    reader = FileReader(file_path)
    raw_text = reader.read()

    # clean resume
    cleaner = TextCleaner(raw_text)
    text = cleaner.clean()

    # Extract entities
    extractor = NERExtractor()
    entities = extractor.extract_entities(text)
    
    print("\n🎯 Extracted Entities:")
    for key, value in entities.items():
        print(f"{key.title()}: {value}")
except Exception as e:
    print(f"Error reading file: {e}")