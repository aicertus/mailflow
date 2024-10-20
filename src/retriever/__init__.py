from pydantic import BaseModel
from llama_index.core import Settings

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import Response
import chromadb
import os

Settings.embed_model = HuggingFaceEmbedding = HuggingFaceEmbedding(model_name='BAAI/bge-m3', trust_remote_code=True)
Settings.llm = Ollama(model="llama3.1", request_timeout=1500.0)

class rag_retrieval(BaseModel):
    db_path: os.path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'chroma'))
    retriever: VectorIndexRetriever = None

    def read_db(self):
        db = chromadb.PersistentClient(path=self.db_path)
        chroma_collection = db.get_or_create_collection("quickstart")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex([], llm=None, embed_model=Settings.embed_model, storage_context=storage_context)
        retriever = VectorIndexRetriever(index=index, similarity_top_k=3, filters=None)
        response_synthesizer = get_response_synthesizer(response_mode="tree_summarize", llm=Settings.llm)
        self.retriever = RetrieverQueryEngine(retriever=retriever, response_synthesizer=response_synthesizer,
                                                   node_postprocessors=None)

    def query(self, text_query: str) -> Response:
        """
        Realiza una consulta sobre el RAG inicializado y devuelve la respuesta.
        """
        return self.retriever.query(text_query)
    
    class Config:
        arbitrary_types_allowed = True