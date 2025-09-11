# import streamlit as st
# from models.vector_db import VectorDB
# from llm_api import LLMResponseGenerator  # Updated to use the Groq API
# from ingestion import extractors, preprocessors

# def main():
#     st.title("Personal Knowledge Assistant")

#     # File uploader for multiple PDFs
#     uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    
#     if uploaded_files:
#         st.write("Processing the PDFs...")

#         # Initialize the vector database
#         vector_db = VectorDB()

#         # Iterate over each uploaded file
#         for uploaded_file in uploaded_files:
#             # Extract and preprocess text from the uploaded PDF
#             text = extractors.extract_text_from_pdf(uploaded_file)
#             cleaned_text = preprocessors.preprocess_text(text)

#             # Add document to the vector database
#             metadata = {"source": uploaded_file.name, "doc_type": "pdf"}
#             vector_db.upsert_embedding(doc_id=uploaded_file.name, document_text=cleaned_text, metadata=metadata)

#         # Provide a query option
#         query = st.text_input("Enter your query")
#         if query:
#             # Query the vector database
#             query_result = vector_db.query_embedding(query_text=query, top_k=2)
            
#             if query_result['documents']:
#                 st.write("Query results:")
#                 context = query_result['documents'][0]  # Use first document as context

#                 # Initialize the Groq-based response generator
#                 response_generator = LLMResponseGenerator()

#                 # Generate a response using Groq API
#                 response = response_generator.generate_response(query=query, context=context)
                
#                 # Display the LLM response
#                 st.write("LLM Response:")
#                 st.write(response)
#             else:
#                 st.write("No relevant documents found.")

# if __name__ == "__main__":
#     main()








# import streamlit as st
# import pandas as pd
# from llm_api import LLMResponseGenerator
# from ingestion import extractors, preprocessors

# def main():
#     st.title("Personal Knowledge Assistant")

#     # Initialize the LLM response generator
#     response_generator = LLMResponseGenerator()

#     # Continuous chat history display
#     chat_history_display = st.empty()

#     # File uploader for PDFs or DataFrames (CSV)
#     uploaded_files = st.file_uploader("Upload PDFs or CSV", type=["pdf", "csv"], accept_multiple_files=True)

#     # If the user uploads files, extract the context and add to chat history
#     if uploaded_files:
#         for uploaded_file in uploaded_files:
#             if uploaded_file.type == "application/pdf":
#                 # Extract text from PDF
#                 text = extractors.extract_text_from_pdf(uploaded_file)
#                 cleaned_text = preprocessors.preprocess_text(text)
#                 response_generator.add_message_to_history("system", f"Context from {uploaded_file.name}: {cleaned_text}")
#                 #uncomment the line below to verify the document uploaded
#                 # st.write(f"Context from {uploaded_file.name} has been added.")
#             elif uploaded_file.type == "text/csv":
#                 # Process CSV as a DataFrame
#                 df = pd.read_csv(uploaded_file)
#                 st.write(f"DataFrame from {uploaded_file.name} has been added.")
#                 # Optionally you can summarize or extract useful information from the DataFrame
#                 df_summary = df.describe().to_string()
#                 response_generator.add_message_to_history("system", f"Summary from {uploaded_file.name}: {df_summary}")

#     # User text input
#     user_query = st.text_input("Ask a question")

#     if user_query:
#         # Generate response using chat history
#         response = response_generator.generate_response(user_query)
        
#         # Update chat history in the Streamlit UI
#         chat_history_display.write(response_generator.chat_history)

#         # Display the LLM's response
#         st.write("LLM Response:", response)

# if __name__ == "__main__":
#     main()





import streamlit as st
import pandas as pd
from llm_api import LLMResponseGenerator
from ingestion import extractors, preprocessors
from models import vector_db
import os

def main():
    st.set_page_config(page_title="AI Chatbot", layout="wide")  
    st.title("AI Chatbot with File & URL Support")
    api_key = st.secrets["GROQ_API_KEY"]



    # Sidebar: File Upload & URL Input
    with st.sidebar:
        st.header("Upload Files & URLs")
        uploaded_file = st.file_uploader("Upload PDF/CSV", type=["pdf", "csv"])
        url_input = st.text_input("Enter a URL to fetch text:")

        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

    
    v_db=vector_db.VectorDB()


    if "chat_history" not in st.session_state:
        st.session_state.chat_history=[]

    if uploaded_file:
        doc_id = f"{uploaded_file.name}_{os.urandom(4).hex()}"  # Unique ID for each doc

        if uploaded_file.type == "application/pdf":
            extracted_text=extractors.extract_text_from_pdf(uploaded_file)
            cleaned_text = preprocessors.preprocess_text(extracted_text)
            v_db.upsert_embedding(doc_id, cleaned_text, {"type": "pdf", "name": uploaded_file.name})
            st.session_state.chat_history.append({"role":"system","content":f"Context from {uploaded_file.name}"})

        elif uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            df_summary = df.describe().to_string()
            v_db.upsert_embedding(doc_id, df_summary, {"type": "csv", "name": uploaded_file.name})
            st.session_state.chat_history.append({"role": "system", "content": f"CSV summary from {uploaded_file.name} has been added."})   

    if url_input:
        doc_id = f"url_{os.urandom(4).hex()}"
        extracted_text = extractors.extract_text_from_url(url_input)
        cleaned_text = preprocessors.preprocess_text(extracted_text)
        v_db.upsert_embedding(doc_id, cleaned_text, {"type": "url", "source": url_input})
        st.session_state.chat_history.append({"role": "system", "content": f"Context from URL has been added."})
        st.session_state.chat_history.append({"role": "system", "content": f"Context from URL: {extracted_text}"})


    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])


    user_input=st.chat_input("Ask your query here:")

    if user_input:

        source_filter = None
        query_text = user_input
        if user_input.lower().startswith("url"):
            source_filter="url"
            query_text = user_input[4:].strip()
        

        elif user_input.lower().startswith("pdf:"):
            source_filter = "pdf"
            query_text = user_input[4:].strip()


        st.session_state.chat_history.append({"role":"user","content":user_input})

        with st.chat_message("You:"):
            st.write(user_input)
        results = v_db.query_embedding(query_text,"personal_knowledge_assistant",source_filter=source_filter, top_k=2)
        context=" ".join(results["documents"][0]) if results["documents"] else "No relevant context found."

     #response
        response_generator = LLMResponseGenerator()
        truncated_context = response_generator.truncate_text(response_generator.clean_text(context), max_tokens=1500)

        combined_query = f"Context: {truncated_context}\n\nUser Question: {query_text}"
        
        response =response_generator.generate_response(combined_query)

        st.session_state.chat_history.append({"role": "assistant", "content": response})

        # Display response
        with st.chat_message("assistant"):
            st.write(response)

if __name__ == "__main__":
    main()


