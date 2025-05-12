import os
import pdfplumber
import docx

class FileReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.extension = os.path.splitext(file_path)[1].lower()

    def read(self):
        if self.extension == '.pdf':
            return self._read_pdf()
        elif self.extension == '.docx':
            return self._read_docx()
        elif self.extension == '.txt':
            return self._read_txt()
        else:
            raise ValueError(f"Unsupported file type: {self.extension}")

    def _read_pdf(self):
        text = ""
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def _read_docx(self):
        doc = docx.Document(self.file_path)
        return "\n".join(para.text for para in doc.paragraphs)

    def _read_txt(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return f.read()