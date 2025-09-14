import sys
from pathlib import Path
import fitz
import os
from langchain_community.document_loaders import PyMuPDFLoader
from datetime import datetime, timezone
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
import uuid


class DocumentIngestion():
    def __init__(self, base_dir: str = "data/document_compare", session_id: str = None):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.session_id = session_id or f"session_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        self.session_path = self.base_dir/self.session_id
        self.session_path.mkdir(parents=True, exist_ok=True)   
        self.log.info(f"DocumentIngestion initialized", session_id=self.session_id, session_path=str(self.session_path))    

    def save_uploaded_files(self, reference_file, actual_file):
        '''Saves uploaded files to a specified directory with a timestamp.'''
        try:            
            ref_path = self.base_dir/reference_file.name  # reference file path i.e document 1
            actual_path = self.base_dir/actual_file.name # document 2 used to compare with document 1

            if not reference_file.name.lower().endswith('.pdf') or not actual_file.name.lower().endswith('.pdf'):
                raise ValueError("Only PDF files are supported.")
            
            with open(ref_path, "wb") as f:
                f.write(reference_file.getbuffer())
                            
            with open(actual_path, "wb") as f:
                f.write(actual_file.getbuffer())

            self.log.info("Files saved successfully", reference_file=str(ref_path), actual_file=str(actual_path), session=self.session_id)
            return ref_path, actual_path

        except Exception as e:
            self.log.error("Error saving PDF files", error=str(e), session=self.session_id)
            raise DocumentPortalException("An error occurred while saving the uploaded files", sys)

    def read_pdf(self, pdf_path: Path) -> str:
        '''Reads a PDF file and returns text from each page.'''
        try:
            loader = PyMuPDFLoader(str(pdf_path))
            documents = loader.load()
            
            all_text = []
            for i, doc in enumerate(documents):
                if doc.page_content.strip():
                    all_text.append(f"\n --- Page {i + 1} ---\n{doc.page_content}")
            
            self.log.info("Successfully read PDF", file=str(pdf_path), pages=len(all_text))
            return "\n".join(all_text)
            
        except Exception as e:
            self.log.error(f"Error reading PDF files: {e}")
            raise DocumentPortalException("An error occurred while reading the PDF", sys)
            
    def combine_documents(self) -> str:
        '''Combines text from two documents for comparison.'''
        try:
            content_dict = {}
            doc_parts = []

            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix.lower() == '.pdf':
                    content_dict[filename.name] = self.read_pdf(filename)

            for filename, content in content_dict.items():
                doc_parts.append(f"Document: {filename}\n{content}")

            combined_text = "\n\n".join(doc_parts)
            self.log.info("Documents combined successfully", count=len(doc_parts))
            return combined_text

                    
        except Exception as e:
            self.log.error(f"Error combining documents: {e}")
            raise DocumentPortalException("An error occurred while combining the documents", sys)