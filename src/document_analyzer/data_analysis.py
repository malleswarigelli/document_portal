import os
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import Metadata
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from src.document_analyzer.data_ingestion import DocumentHandler
from prompt.prompt_library import prompt


class DocumentAnalyzer:
    """
    A class to analyze documents using pre-trained loaded models.

    It uses the ModelLoader to get the necessary models for analysis.
    """
    
    def __init__(self):
        self.model_loader = ModelLoader()
        self.logger = CustomLogger().get_logger(__name__)

        try:
            # load models
            self.loader = ModelLoader()
            self.llm = self.loader.load_llm()
            # prepare output parser
            self.parser = JsonOutputParser(pydantic_object=Metadata)
            self.output_parser = OutputFixingParser.from_llm(self.llm, self.parser) # parses llm output into json format

            # prompt
            self.prompt = prompt

            self.logger.info("DocumentAnalyzer initialized successfully.")

        except Exception as e:
            self.logger.error("Error initializing DocumentAnalyzer", {e})
            raise DocumentPortalException("Failed to initialize DocumentAnalyzer", sys)
    
    def analyze_document(self, document: str) -> Dict[str, Any]:
        """
        Analyze a document and return structured data.
        
        Args:
            document (str): The text content of the document to analyze.
        
        Returns:
            Dict[str, Any]: Structured analysis results.
        """
        try:
            self.logger.info("Chain is being created for document analysis.")
            chain = self.prompt | self.llm | self.output_parser
            self.logger.info("Chain created successfully.")

            response = chain.invoke({
                "format_instructions": self.parser.get_format_instructions(),
                "document_text": document
            })
            self.logger.info("Metadata extraction is successful", keys=list(response.keys()))

            return response
        
        except Exception as e:
            self.logger.error("Error during document analysis", error=str(e))
            raise DocumentPortalException("Failed to analyze document", sys) from e