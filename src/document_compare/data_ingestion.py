import sys
from pathlib import Path
import fitz
import os
from langchain_community.document_loaders import PyMuPDFLoader
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException


class DocumentIngestion():
    def __init__(self, base_dir="data/document_compare"):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)    

    def delete_existing_files(self, directory: str):
        '''Deletes all files in the specified directory.'''
        try:
            if self.base_dir.exists() and self.base_dir.is_dir():
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                self.log.info(f"All files deleted in directory: {directory}")
        except Exception as e:
            self.log.error(f"Error deleting files in {directory}: {e}")
            raise DocumentPortalException(f"An error occurred while deleting files in {directory}", sys)

    def save_uploaded_files(self, reference_file, actual_file):
        '''Saves uploaded files to a specified directory with a timestamp.'''
        try:            
            self.delete_existing_files(self.base_dir)
            self.log.info(f"Existing files deleted successfully")

            ref_path = self.base_dir/reference_file.name  # reference file path i.e document 1
            actual_path = self.base_dir/actual_file.name # document 2 used to compare with document 1

            if not reference_file.name.lower().endswith('.pdf') or not actual_file.name.lower().endswith('.pdf'):
                raise ValueError("Only PDF files are supported.")
            
            with open(ref_path, "wb") as f:
                f.write(reference_file.getbuffer())
                            
            with open(actual_path, "wb") as f:
                f.write(actual_file.getbuffer())

            self.log.info(f"Files saved successfully", reference_file=str(ref_path), actual_file=str(actual_path))
            return ref_path, actual_path

        except Exception as e:
            # self.log.error(f"Error saving uploaded files: {e}")
            raise DocumentPortalException("An error occurred while saving the uploaded files", sys)

    def read_pdf(self, pdf_path: Path) -> str:
        '''Reads a PDF file and returns text from each page.'''
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError(f"PDF is encrypted: {pdf_path.name}")                
                all_text = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    # strip if white space in the page
                    if text.strip():
                        all_text.append(f"\n --- Page {page_num + 1} ---\n{text}")
                self.log.info(f"Successfully read PDF", file=str(pdf_path), pages=len(all_text))
                return "\n".join(all_text) # Join all page texts with page separators
            
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