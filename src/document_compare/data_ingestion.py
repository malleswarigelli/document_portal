import sys
from pathlib import Path
import fitz  # PyMuPDF
import os
from langchain_community.document_loaders import PyMuPDFLoader
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException


class DocumentComparator():
    def __init__(self, logger: CustomLogger):
        self.logger = logger

    def delete_existing_files(self, directory: str):
        '''Deletes all files in the specified directory.'''
        pass

    def save_uploaded_files(self):
        '''Saves uploaded files to a specified directory with a timestamp.'''):
        pass

    def read_pdf(self):
        '''Reads a PDF file and returns text from each page.'''
        pass