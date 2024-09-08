from models.vector_db import VectorDB, LLMResponseGenerator
from ingestion import extractors, preprocessors

def run_pipeline():
    # Initialize the vector database
    vector_db = VectorDB()

    # Extract and preprocess text from Heart Disease PDF
    text_heart_disease = extractors.extract_text_from_pdf("Heart Disease Model project.pdf")
    cleaned_text_heart_disease = preprocessors.preprocess_text(text_heart_disease)
    
    # Store heart disease PDF text in ChromaDB
    metadata_heart = {"source": "Heart Disease Model project.pdf", "doc_type": "pdf"}
    vector_db.upsert_embedding(doc_id="id1", document_text=cleaned_text_heart_disease, metadata=metadata_heart)

    # Extract and preprocess text from Drone Navigation PDF
    text_drone_nav = extractors.extract_text_from_pdf("drones-07-00089.pdf")
    cleaned_text_drone_nav = preprocessors.preprocess_text(text_drone_nav)
    
    # Store drone navigation PDF text in ChromaDB
    metadata_drone = {"source": "drones-07-00089.pdf", "doc_type": "pdf"}
    vector_db.upsert_embedding(doc_id="id2", document_text=cleaned_text_drone_nav, metadata=metadata_drone)

    # Query the database with a sample query or the relevant pdf you want to take refference from
    query_result = vector_db.query_embedding(query_text="drone", top_k=2)
    
    # Check if documents are returned
    if query_result['documents']:
        context = query_result['documents'][0]  # Use the first document's content as context

        # Initialize the LLM response generator
        response_generator = LLMResponseGenerator(model_path=r"C:\Users\navpa\Downloads\Phi-3-mini-4k-instruct.Q4_0.gguf")

        # Truncate the context to fit within token limits
        truncated_context = response_generator.truncate_text(response_generator.clean_text(context), max_tokens=1500)
        
        # Combine context and query the original query you want response about
        combined_query = f"{truncated_context}\n\nQ:medical emergencies\nA:"
        # print("Combined Query:", combined_query)
        
        # Ensure combined query is within token limits
        total_tokens = response_generator.count_tokens(combined_query)
        if total_tokens > 2048:
            combined_query = response_generator.truncate_text(combined_query, max_tokens=2048)
        
        # Generate a response from the LLM using the combined query
        response = response_generator.generate_response(combined_query)
        print("LLM Response:", response)
    else:
        print("No relevant documents found.")

if __name__ == "__main__":
    run_pipeline()



if __name__ == "__main__":
    run_pipeline()





