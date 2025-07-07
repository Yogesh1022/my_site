import PyPDF2
import pdfplumber
import io


class PDFProcessor:
    """Handles PDF text extraction using multiple methods for best results"""
    
    def __init__(self):
        pass
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from PDF using multiple methods
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            # Try pdfplumber first (better for complex layouts)
            text = self._extract_with_pdfplumber(file_path)
            
            if len(text.strip()) < 100:  # If pdfplumber fails, try PyPDF2
                text = self._extract_with_pypdf2(file_path)
            
            return self._clean_text(text)
            
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
    
    def _extract_with_pdfplumber(self, file_path: str) -> str:
        """Extract text using pdfplumber"""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"PDFPlumber extraction failed: {e}")
            
        return text
    
    def _extract_with_pypdf2(self, file_path: str) -> str:
        """Extract text using PyPDF2"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                        
        except Exception as e:
            print(f"PyPDF2 extraction failed: {e}")
            
        return text
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line:  # Only keep non-empty lines
                cleaned_lines.append(line)
        
        # Join lines and normalize spacing
        cleaned_text = ' '.join(cleaned_lines)
        
        # Remove multiple spaces
        import re
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        
        return cleaned_text.strip()
    
    def extract_metadata(self, file_path: str) -> dict:
        """Extract metadata from PDF"""
        metadata = {}
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                if pdf_reader.metadata:
                    metadata = {
                        'title': pdf_reader.metadata.get('/Title', ''),
                        'author': pdf_reader.metadata.get('/Author', ''),
                        'subject': pdf_reader.metadata.get('/Subject', ''),
                        'creator': pdf_reader.metadata.get('/Creator', ''),
                        'producer': pdf_reader.metadata.get('/Producer', ''),
                        'creation_date': pdf_reader.metadata.get('/CreationDate', ''),
                        'modification_date': pdf_reader.metadata.get('/ModDate', ''),
                        'pages': len(pdf_reader.pages)
                    }
                    
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            
        return metadata
