from pydantic import BaseModel, Field
from typing import List, Callable, Optional, Dict, Any

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.core import StorageContext, ServiceContext
from llama_index.core import VectorStoreIndex, SimpleKeywordTableIndex
from llama_index.core import Document

from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.retrievers import KeywordTableSimpleRetriever
from llama_index.core import Response
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.postprocessor import MetadataReplacementPostProcessor

from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)

from llama_index.core.vector_stores.types import VectorStoreQueryResult
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.postprocessor import (
    PrevNextNodePostprocessor,
    AutoPrevNextNodePostprocessor,
)
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.llms.ollama import Ollama

from llama_index.core import Settings

from typing import Literal
from pydantic import model_validator

import logging
import sys

import json

import instructor
from openai import OpenAI
OpenAI.api_key = 'ollama'

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

Settings.llm = Ollama(model="llama3.1", request_timeout=1500.0)
#Settings.embed_model = HuggingFaceEmbedding(model_name='BAAI/bge-m3')


class Email(BaseModel):
    de: Optional[str] = ""
    para: Optional[List[str]] = []
    asunto: Optional[str] = ""
    texto: Optional[str] = ""

class ExtractedInfo(BaseModel):
    cups: Optional[List[str]] = Field(description="Una lista de todos los cups sobre los que se refiere el mensaje. Los cups suelen empezar por ES o PT y están seguidos de unos 20 caracteres")
    cif: Optional[List[str]] = Field(description="Extrae todos los CIFs que aparecen en el email")
    summary: Optional[str] = Field(description="Resume el email en bullets")

class ExtractedMail(BaseModel):
    de: Optional[str] = ""
    para: Optional[List[str]] = []
    asunto: Optional[str] = ""
    texto: Optional[str]= ""
    cif: Optional[List[str]] = []
    cups: Optional[List[str]] = []
    summary: Optional[str] = ""
    

class EmailExtractor(BaseModel):
    """
    Clase encargada de extraer la información de los emails.
    """
    email: Email# Reemplaza Any con la clase Email si está definida
    resp: Optional[Any] = None
    extractedEmail: Optional[ExtractedMail] = None
    extractedInfo: Optional[ExtractedInfo] = None
    client: Optional[Any] = None

    # Validador que se ejecuta después de la creación del modelo
    @model_validator(mode='before')
    def validate_and_initialize(cls, values):
        # Se ejecuta después de que el modelo ha sido inicializado
        #values['extractedEmail'] = ExtractedMail()
        #values['extractedInfo'] = ExtractedInfo()

        instance = values.get('client')
        if instance is None:
            # Inicializamos el cliente si aún no ha sido asignado
            values['client'] = instructor.from_openai(
                OpenAI(
                    base_url="http://localhost:11434/v1",
                    api_key="ollama",
                ),
                mode=instructor.Mode.JSON,
            )
        
        return values

    @model_validator(mode='after')
    def extractEmailInfo(self):
        logging.info("Extrayendo información del mail")
        content = "Extrae la información del email en español. No te inventes nada: " + self.email.texto
        self.resp = self.client.chat.completions.create(
            model="llama3.1",
            messages=[
                {
                    "role": "assistant",
                    "content": content
                }
            ],
            response_model=ExtractedInfo,
        )

        self.extractedEmail = ExtractedMail(
            de = self.email.de,
            para = self.email.para,
            asunto = self.email.asunto,
            texto = self.email.texto,
            cif = self.resp.cif,
            cups = self.resp.cups,
            summary = self.resp.summary
        )

        return self

    class Config:
        arbitrary_types_allowed = True

if __name__ == "__main__":
    pass