import uuid
from pathlib import Path
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader



class SingleDocIngestor:
    """Class for ingesting and processing documents.
    This class handles loading documents, splitting them into chunks,
    generating embeddings, and storing them in a vector store.
    """
    def __init__(self):
        self.logger = CustomLogger.get_logger(__name__)
        self.model_loader = ModelLoader()
        self.document_store = FAISS()

    def ingest_files(self):
        """Ingests a document, splits it into chunks, and stores it in a vector store.
        Args:
            file_path (str): Path to the document file.
            chunk_size (int): Size of each text chunk.
            chunk_overlap (int): Overlap between text chunks.   
        """
        try:
            self.logger.info(f"Starting ingestion for document: {file_path}")
            # Load the document
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            self.logger.info(f"Loaded {len(documents)} pages from the document.")

            # Split the document into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            docs = text_splitter.split_documents(documents)
            self.logger.info(f"Split document into {len(docs)} chunks.")

            # Generate embeddings
            embedding_model = self.model_loader.get_embedding_model()
            embeddings = [embedding_model.embed(doc.page_content) for doc in docs]
            self.logger.info("Generated embeddings for document chunks.")

            # Store in vector store
            self.document_store.add_texts([doc.page_content for doc in docs], embeddings)
            self.logger.info("Document chunks stored in vector store successfully.")

        except Exception as e:
            self.log.error("Document ingestion failed.", error=str(e))
            raise DocumentPortalException("Failed to ingest document", sys)


    def _create_retrieval(self):
        try:
            pass

        except Exception as e:
            self.log.error("Retriever creation failed.", error=str(e))
            raise DocumentPortalException("Error creating FAISS retriever", sys)