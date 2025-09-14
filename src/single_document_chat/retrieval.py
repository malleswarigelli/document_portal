import os, sys
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from utils.model_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from prompt.prompt_library import PROMPT_REGISTRY
from model.models import PromptType


class ConversationalRAG:
    def __init__(self, session_id: str, retriever):
        try:
            self.log = CustomLogger(os.path.basename(__file__))

        except Exception as e:
            self.log.error("Error initializing ConversationalRAG class", error=str(e), session_id=session_id)
            raise DocumentPortalException("Failed to initialize ConversationalRAG", sys)
        
    def _load_llm(self, session_id: str):
        try:
            load_dotenv()
            model_loader = ModelLoader(session_id=session_id)
            llm = model_loader.load_model()
            return llm
        except Exception as e:
            self.log.error("Error loading LLM", error=str(e), session_id=session_id)
            raise DocumentPortalException("Failed to load LLM", sys)
        
    def _get_history(self, session_id: str) -> BaseChatMessageHistory:
        try:
            history = ChatMessageHistory(session_id=session_id)
            return history
        except Exception as e:
            self.log.error("Failed to access session history", error=str(e), session_id=session_id)
            raise DocumentPortalException("Failed to retrieve chat history", sys)        
        
    def load_retirever_from_FAISS(self, session_id: str) -> FAISS:
        try:
            persist_directory = os.getenv("PERSIST_DIRECTORY", "db")
            vectorstore = FAISS.load_local(persist_directory, embeddings=None)
            return vectorstore.as_retriever()
        except Exception as e:
            self.log.error("Error loading retriever", error=str(e), session_id=session_id)
            raise DocumentPortalException("Failed to load retriever", sys)        
        
    def invoke(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to invoke coversational RAG", error=str(e), session_id=self.session_id)")
            raise DocumentPortalException("Failed to invoke RAG chain", sys)