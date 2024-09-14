import chromadb
# import openai
from chromadb.config import Settings
from langchain_community.llms import GPT4All
from langchain_core.prompts import PromptTemplate
import tiktoken
import re
from groq import Groq
import os


# client = Groq(
#     api_key=os.environ.get("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"),
# )



class VectorDB:
    def __init__(self):
        # Initialize the ChromaDB client (in-memory for prototyping)
        self.client = chromadb.Client()
        # Check if the collection exists; if not, create it
        existing_collections = self.client.list_collections()
        collection_name = "personal_knowledge_assistant"
        
        if collection_name in [col.name for col in existing_collections]:
            self.collection = self.client.get_collection(collection_name)
        else:
            self.collection = self.client.create_collection(collection_name)

    def upsert_embedding(self, doc_id, document_text, metadata):
        # Add document text with metadata
        self.collection.add(
            documents=[document_text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        print(f"Inserted document with ID: {doc_id}")

    
    def query_embedding(self, query_text, top_k=5):
        # Query the collection for the most similar documents
        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k
        )
        return results


class LLMResponseGenerator:
    def __init__(self, model_path):
        self.model_path = model_path
        # Load GPT4All model
        self.llm = GPT4All(model=self.model_path, streaming=False)
        self.prompt_template = PromptTemplate.from_template(
        """
              You are a detailed and helpful assistant. Please answer the question in the following format:
    
        1. Definition:
        2. Key Points:
        3. Example (if applicable):

        Context: {context}

        Q: {question}
        A:
        """
        )
        self.encoding = tiktoken.get_encoding("cl100k_base")  # Adjust as needed

    
    def clean_text(self,text):
        # If text is a list, join it into a single string
        if isinstance(text, list):
            text = " ".join(text)
        
        # Use regex to replace non-ASCII characters with a space
        cleaned_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        
        return cleaned_text

    def count_tokens(self, text):
        tokens = self.encoding.encode(text)
        return len(tokens)

    def truncate_text(self, text, max_tokens=1500):

        # cleaned_text=clean_text(text)
        tokens = self.encoding.encode(text)
        
        if len(tokens) > max_tokens:
            tokens = tokens[:max_tokens]
        return self.encoding.decode(tokens)

    def generate_response(self, combined_query):
        # Check token length
        total_tokens = self.count_tokens(combined_query)
        if total_tokens > 2048:
            combined_query = self.truncate_text(combined_query, max_tokens=2048)
        
        # Run the model with the combined query
        response = self.llm.invoke(combined_query)
        
        return response