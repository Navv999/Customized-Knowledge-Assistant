
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb
# import openai
from chromadb.config import Settings
from langchain_community.llms import GPT4All
from langchain_core.prompts import PromptTemplate
import tiktoken
from groq import Groq
import os


class VectorDB:
    def __init__(self):
        # Initialize the ChromaDB client (in-memory for prototyping)
        self.client = chromadb.PersistentClient(path="./chroma_db")
        # Check if the collection exists; if not, create it
        existing_collections = self.client.list_collections()
        print("existing_collections::",existing_collections)
        collection_name = "personal_knowledge_assistant"
        
        if collection_name in [col.name for col in existing_collections]:
            self.collection = self.client.get_collection(collection_name)
        else:
            self.collection = self.client.create_collection(collection_name)

    def upsert_embedding(self, doc_id, document_text, metadata):
        """
        Inserts or updates document embeddings in ChromaDB.
        
        :param doc_id: Unique identifier for the document.
        :param document_text: The text content of the document.
        :param metadata: Dictionary containing metadata (e.g., {"type": "pdf", "name": uploaded_file.name}).
        """

        if not isinstance(metadata, dict):
            raise ValueError("Metadata must be a dictionary.")

        # Ensure metadata contains 'type' and 'name' fields
        metadata.setdefault("type", "pdf")

        self.collection.add(
            documents=[document_text],
            metadatas=[metadata],  # Use the provided metadata
            ids=[doc_id]
        )
        print(f"Inserted document with ID: {doc_id}")


    
    def query_embedding(self, query_text, doc_id=None, source_filter=None, top_k=5):
        """
        Queries the ChromaDB collection for the most similar documents.
        
        :param query_text: The query string.
        :param doc_id: The document ID to filter results to a specific document's collection.
        :param source_filter: Filter based on metadata type (e.g., "pdf", "url").
        :param top_k: Number of top results to retrieve.
        :return: Query results from ChromaDB.
        """
        
        if not doc_id:
            raise ValueError("doc_id is required to query a specific document's collection.")

        # Ensure the requested collection exists
        collection_names = [col.name for col in self.client.list_collections()]
        if doc_id not in collection_names:
            raise ValueError(f"Collection '{doc_id}' does not exist.")

        collection = self.client.get_collection(doc_id)

        # Apply filtering
        filters = {}
        if source_filter:
            filters = {"type": source_filter}  # Match the metadata key in `upsert_embedding`

        # Perform the query
        results = collection.query(
            query_texts=[query_text],
            n_results=top_k,
            where=filters
        )

        return results


# class LLMResponseGenerator:
#     def __init__(self, model_path):
#         self.model_path = model_path
#         self.llm = GPT4All(model=self.model_path, streaming=False)
#         self.prompt_template = PromptTemplate.from_template(
#         """
#               You are a detailed and helpful assistant. Please answer the question in the following format:
    
#         1. Definition:
#         2. Key Points:
#         3. Example (if applicable):

#         Context: {context}

#         Q: {question}
#         A:
#         """
#         )
#         self.encoding = tiktoken.get_encoding("cl100k_base")  # Adjust as needed

    


#     def count_tokens(self, text):
#         tokens = self.encoding.encode(text)
#         return len(tokens)

#     def truncate_text(self, text, max_tokens=1500):

#         # cleaned_text=clean_text(text)
#         tokens = self.encoding.encode(text)
        
#         if len(tokens) > max_tokens:
#             tokens = tokens[:max_tokens]
#         return self.encoding.decode(tokens)

#     # def generate_response(self, combined_query):
#     #     # Check token length
#     #     total_tokens = self.count_tokens(combined_query)
#     #     if total_tokens > 2000:
#     #         combined_query = self.truncate_text(combined_query, max_tokens=2048)
        
#     #     # Run the model with the combined query
#     #     response = self.llm.invoke(combined_query)
        
#     #     return response