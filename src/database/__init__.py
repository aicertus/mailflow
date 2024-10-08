from mailextractor import ExtractedMail
from pydantic import BaseModel
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.core import StorageContext, ServiceContext, set_global_service_context
from llama_index.core import VectorStoreIndex
from llama_index.core import Document
from llama_index.llms.ollama import Ollama

import chromadb
import os
import logging

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

class database_storer(BaseModel):
    db_path: os.path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'chroma'))
    extractedMail: ExtractedMail
    embed_model:HuggingFaceEmbedding = HuggingFaceEmbedding(model_name='BAAI/bge-m3', trust_remote_code=True)

    def getDbPath(self) -> os.path:
        return self.db_path
    
    def saveMail2DB(self):
        print(self.extractedMail.model_dump_json(exclude="texto"))
        document = Document(
            text = self.extractedMail.texto,
            metadata = self.extractedMail.to_custom_dict()
        )
        print(document)

        db = chromadb.PersistentClient(
            path = self.db_path
        )

        chroma_collection = db.get_or_create_collection("quickstart")
        vector_store = ChromaVectorStore(chroma_collection = chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store = vector_store)

        index = VectorStoreIndex([document],
            llm=None,
            embed_model=self.embed_model,
            storage_context=storage_context
        )

    class Config:
        arbitrary_types_allowed = True

if __name__ == "__main__":
    pass