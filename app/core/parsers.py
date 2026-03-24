import io
from pypdf import PdfReader
import docx

def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extracts text from TXT, PDF, and DOCX files."""
    ext = filename.split('.')[-1].lower()
    text = ""
    
    try:
        if ext == 'txt':
            text = file_bytes.decode('utf-8')
            
        elif ext == 'pdf':
            reader = PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
                    
        elif ext in ['doc', 'docx']:
            doc = docx.Document(io.BytesIO(file_bytes))
            for para in doc.paragraphs:
                text += para.text + "\n"
                
        else:
            raise ValueError(f"Unsupported file format: .{ext}. Please upload a PDF, DOCX, or TXT file.")
            
    except Exception as e:
        raise ValueError(f"Error parsing file: {str(e)}")
        
    return text.strip()