# utils.py
import docx
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error reading DOCX {docx_path}: {e}")
        return ""

def extract_text_from_txt(txt_path):
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT {txt_path}: {e}")
        return ""

def extract_text_from_file(file_path):
    if file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.lower().endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        print(f"Unsupported file format: {file_path}")
        return ""

if __name__ == '__main__':
    # Example usage (assuming you have a sample.pdf, sample.docx, sample.txt in the 'data' folder)
    pdf_text = extract_text_from_file('data/sample.pdf')
    docx_text = extract_text_from_file('data/sample.docx')
    txt_text = extract_text_from_file('data/sample.txt')
    print("PDF Text (first 200 chars):\n", pdf_text[:200] if pdf_text else "No PDF text")
    print("\nDOCX Text (first 200 chars):\n", docx_text[:200] if docx_text else "No DOCX text")
    print("\nTXT Text (first 200 chars):\n", txt_text[:200] if txt_text else "No TXT text")