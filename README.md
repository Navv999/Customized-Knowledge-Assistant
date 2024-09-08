# Customized-Knowledge-Assistant

Personal Knowledge Assistant is a simple, lightweight chatbot built to assist in answering queries based on personal documents and notes. This project showcases the power of Retrieval-Augmented Generation (RAG) combined with a locally hosted Language Model (LLM), all while being optimized for systems with minimal hardware, without the need for a GPU.

Key Features
Retrieval-Augmented Generation (RAG): Efficiently retrieves relevant information from documents and augments it with the query for a more context-aware response.
Locally Hosted LLM: Uses a locally hosted language model, GPT4All, which runs on CPU without needing GPU acceleration.
ChromaDB Integration: Stores document embeddings in a vector database for fast and relevant document retrieval.
PDF Processing: Extracts and processes text from PDF documents for storage and retrieval.
Minimal Hardware Requirement: Optimized to run on low-spec hardware with minimal dependencies.
Project Structure
extraction.py: Handles extracting text from PDF documents using PyMuPDF.
preprocessors.py: Preprocesses text by cleaning, tokenizing, and lemmatizing it.
embeddings.py: Generates document embeddings using Hugging Face's bert-base-uncased model.
vector_db.py: Manages interactions with ChromaDB, stores and retrieves document embeddings, and integrates with GPT4All for query generation.
main.py: Orchestrates the pipeline—extracting, preprocessing, embedding, and querying the documents, as well as generating the response using the LLM.
How it Works
Document Ingestion:

Text is extracted from PDF files.
The extracted text is preprocessed (tokenized, cleaned, and lemmatized).
Document embeddings are generated using BERT and stored in ChromaDB.
Retrieval-Augmented Generation (RAG):

When a query is made, ChromaDB retrieves the most relevant documents by comparing the query to the stored document embeddings.
The retrieved context is combined with the user query to form an augmented prompt for the LLM.
LLM Response:

GPT4All, a locally hosted LLM, generates a response based on the augmented query, providing a context-aware answer.
Example
The project stores two example documents: one on Heart Disease and another on Drone Navigation.
When you query for "heart disease remedies", the system retrieves the relevant information from the Heart Disease document, combines it with the query, and generates a detailed response using the LLM.
Python 3.8+
ChromaDB
Hugging Face Transformers
GPT4All
PyMuPDF (for PDF text extraction)
NLTK (for text preprocessing)
