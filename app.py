import streamlit as st
from models.vector_db import VectorDB, LLMResponseGenerator
from ingestion import extractors, preprocessors

def main():
    st.title("Personal Knowledge Assistant")

    # File uploader for PDFs
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file:
        st.write("Processing the PDF...")
        # Extract and preprocess text from the uploaded PDF
        text = extractors.extract_text_from_pdf(uploaded_file)
        cleaned_text = preprocessors.preprocess_text(text)
        
        # Initialize the vector database
        vector_db = VectorDB()
        
        # Add document to the vector database
        metadata = {"source": uploaded_file.name, "doc_type": "pdf"}
        vector_db.upsert_embedding(doc_id="doc1", document_text=cleaned_text, metadata=metadata)
        
        # Provide a query option
        query = st.text_input("Enter your query")
        if query:
            # Query the vector database
            query_result = vector_db.query_embedding(query_text=query, top_k=2)
            
            # Display query results
            if query_result['documents']:
                st.write("Query results:")
                for i, doc in enumerate(query_result['documents']):
                    st.write(f"Result {i+1}: {doc}")
            else:
                st.write("No relevant documents found.")

if __name__ == "__main__":
    main()
