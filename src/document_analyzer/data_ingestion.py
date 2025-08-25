import os
import uuid # for generating unique session ids
from langchain_community.document_loaders import PyMuPDFLoader
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException


class DocumentHandler():
    """Handles document loading and processing.
    Automatically logs all actions and supports session-based organization
    """
    def __init__(self, data_dir=None, session_id=None):
        try:
            self.logger = CustomLogger().get_logger(__name__)
            self.data_dir = data_dir or os.getenv(
                "DATA_STORAGE_PATH", 
                os.path.join(os.getcwd(), "data", "document_analysis")
            )
            self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)

            self.logger.info(f"PDF Handler initialized with session ID: {self.session_id} at {self.session_path}")
            
        except Exception as e:
            self.logger.error(f"Error initializing DocumentHandler: {e}")
            raise DocumentPortalException("Error initializing DocumentHandler", e) from e
        
    def save_pdf_to_session_path(self, pdf_file) -> str:
        try:
            filename = os.path.basename(pdf_file.name)

            if not filename.lower().endswith('.pdf'):
                raise DocumentPortalException("Only PDF files are supported", None)
            
            save_path = os.path.join(self.session_path, filename)
            with open(save_path, "wb") as f:
                f.write(pdf_file.getbuffer()) ## for in-memory file processing or saving
            
            self.logger.info(f"PDF saved to session_path: {save_path}")
            return save_path
        
        except Exception as e:
            self.logger.error(f"Error saving PDF: {e}")
            raise DocumentPortalException("Error saving PDF", e) from e
        
    def read_pdf(self, pdf_path: str) -> str:
        """Reads a PDF file and extracts its text content using LangChain's PyMuPDFLoader."""
        try:
            loader = PyMuPDFLoader(pdf_path)
            documents = loader.load()
            
            text_chunks = []
            for i, doc in enumerate(documents, start=1):
                text_chunks.append(f"\n--- Page {i} ---\n{doc.page_content}")
            
            text = "\n".join(text_chunks)
            self.logger.info("PDF read successfully", pdf_path=pdf_path, session_id=self.session_id)
            return text
            
        except Exception as e:
            self.logger.error(f"Error reading PDF: {e}")
            raise DocumentPortalException("Error reading PDF", e) from e    
            
if __name__ == "__main__":
    from pathlib import Path
    from io import BytesIO  # processing file in memory
    handler = DocumentHandler()
    pdf_path = r"C:\\Users\\s1296718\\OneDrive - Syngenta\\Desktop\\LLMOPs_course_KrishNaik\\document_portal\\data\\document_analysis\NIPS-2017-attention-is-all-you-need-Paper.pdf"
    
    # for testing purpose only
    class DummyFile:
        def __init__(self, file_path):
            self.name = Path(file_path).name # system compatible file name
            self._file_path = file_path
                    
        def getbuffer(self):
            return open(self._file_path,  "rb").read()        

    dummy_pdf = DummyFile(pdf_path)

    handler = DocumentHandler(session_id="test_session_001")

    try:
        saved_path = handler.save_pdf_to_session_path(dummy_pdf)
        print(f"PDF saved at: {saved_path}")
        content = handler.read_pdf(saved_path)
        print(f"Extracted {len(content)} characters from PDF.")
        print(content[:500])  # print first 500 characters
        
    except Exception as e:
        print(f"Error: {e}")

