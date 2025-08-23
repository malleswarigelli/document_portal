import os
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser


class DocumentAnalyzer:
    """
    A class to analyze documents using loaded models.
    It uses the ModelLoader to get the necessary models for analysis.
    """
    
    def __init__(self):
        self.model_loader = ModelLoader()
        self.logger = CustomLogger().get_logger(__name__)
    
    def analyze_document(self, document: str) -> Dict[str, Any]:
        """
        Analyze a document and return structured data.
        
        Args:
            document (str): The text content of the document to analyze.
        
        Returns:
            Dict[str, Any]: Structured analysis results.
        """
        try:
            self.logger.info("Starting document analysis.")
            embeddings = self.model_loader.load_embeddings()
            llm = self.model_loader.load_llm()
            
            # Example of using embeddings and LLM for analysis
            # This is a placeholder for actual analysis logic
            analysis_result = {
                "document": document,
                "embeddings": embeddings.embed(document),
                "llm_response": llm.generate([document])
            }
            
            self.logger.info("Document analysis completed successfully.")
            return analysis_result
        
        except Exception as e:
            self.logger.error("Error during document analysis", error=str(e))
            raise DocumentPortalException("Failed to analyze document", sys) from e