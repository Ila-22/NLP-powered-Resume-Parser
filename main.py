from parser.file_reader import read_file

def main():
    file_path = "data/sample_resume.pdf"  # Change to .docx or .txt if needed

    try:
        text = read_file(file_path)
        print("Extracted Resume Text:\n")
        print(text[:1000])  # Show only first 1000 characters for now
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    main()