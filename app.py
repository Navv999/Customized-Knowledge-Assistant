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

# Initialize session state for chat history and input if not already present
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'message' not in st.session_state:
    st.session_state['message'] = ''

def main():
    st.title("Personal Knowledge Assistant - Chat Interface")

    # Initialize the LLM response generator
    response_generator = LLMResponseGenerator()

    # File uploader for PDFs or DataFrames (CSV)
    uploaded_files = st.file_uploader("Upload PDFs or CSV", type=["pdf", "csv"], accept_multiple_files=True)

    # Process uploaded files and add context to the chat history
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.type == "application/pdf":
                # Extract text from PDF
                text = extractors.extract_text_from_pdf(uploaded_file)
                cleaned_text = preprocessors.preprocess_text(text)
                # Add system message about the file context
                st.session_state['chat_history'].append(f"System: Context from {uploaded_file.name} has been added.")
                response_generator.add_message_to_history("system", f"Context from {uploaded_file.name}: {cleaned_text}")
            elif uploaded_file.type == "text/csv":
                # Process CSV as a DataFrame
                df = pd.read_csv(uploaded_file)
                # Add system message about the CSV context
                st.session_state['chat_history'].append(f"System: DataFrame from {uploaded_file.name} has been added.")
                df_summary = df.describe().to_string()
                response_generator.add_message_to_history("system", f"Summary from {uploaded_file.name}: {df_summary}")

    # Display chat history
    for message in st.session_state['chat_history']:
        st.write(message)

    # Text input for user's message
    user_input = st.text_input("Your message:", key="user_input")

    # Button to send the message
    if st.button("Send"):
        if user_input:
            # Add user's message to chat history
            st.session_state['chat_history'].append(f"You: {user_input}")

            # Generate response using the LLM
            response = response_generator.generate_response(user_input)

            # Add LLM's response to the chat history
            st.session_state['chat_history'].append(f"Assistant: {response}")

            # Clear the input field indirectly by setting a different session key
            st.session_state['message'] = ''  # This won't conflict with 'user_input'

if __name__ == "__main__":
    main()
