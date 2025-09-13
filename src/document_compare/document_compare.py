import sys
from dotenv import load_dotenv
import pandas as pd
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from prompt.prompt_library import PROMPT_REGISTRY
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser


class DocumentComparatorLLM():
    def __init__(self, logger: CustomLogger):
        load_dotenv()  # load environment variables
        self.log = logger
        self.model_loader = ModelLoader()
        self.embedding_model = self.model_loader.load_embeddings()
        self.llm_model = self.model_loader.load_llm()
        self.json_parser = JsonOutputParser(pydantic_object=SummaryResponse)
        self.output_parser = OutputFixingParser.from_llm(
            llm=self.llm_model,
            parser=self.json_parser,
            max_tries=3,
            verbose=True
        )
        self.prompt = PROMPT_REGISTRY["document_compare_prompt"]
        self.chain = self.prompt | self.llm_model | self.json_parser | self.output_parser
        self.log.info("DocumentComparatorLLM initialized with model and parser successfully")

    def compare_documents(self, combined_docs):
        '''Compares two documents and returns the differences.'''
        try:
            inputs = {
                "combined_docs": combined_docs,
                "format_instructions": self.json_parser.get_format_instructions()
            }
            self.log.info("Starting Comparing documents using LLM", inputs=inputs)
            response = self.chain.invoke(inputs)
            self.log.info("Document comparison completed successfully", response=response)  
            return self._format_response(response)

        except Exception as e:
            self.log.error(f"Error comparing documents, {e}")
            raise DocumentPortalException("Error occurred while comparing documents", sys)

    def _format_response(self, response_parsed: list[dict]) -> pd.DataFrame:
        '''Formats the LLM response into a structured format.'''
        try:
            df = pd.DataFrame(response_parsed)
            self.log.info("Response formatted into DataFrame successfully", dataframe=df)
            return df

        except Exception as e:
            self.log.error("Error formatting response into DataFrame", error=str(e))
            raise DocumentPortalException("Error formatting response", sys)
