# import os
# from groq import Groq

# class LLMResponseGenerator:
#     def __init__(self):
#         api_key = "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"
#         self.client = Groq(api_key=api_key)

#     def generate_response(self, query, context=None):
#         # Prepare the messages to be sent to the API
#         messages = [{"role": "user", "content": f"{context}\n\nQ: {query}\nA:"}]
        
#         chat_completion = self.client.chat.completions.create(
#             messages=messages,
#             model="llama3-8b-8192"  # Adjust model as necessary
#         )

#         return chat_completion.choices[0].message.content






import os
from groq import Groq
from dotenv import load_dotenv
from groq import Client
import tiktoken
import re




load_dotenv()


class LLMResponseGenerator:
    def __init__(self):
        # Retrieve the API key from the environment
        groq_api_key= os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("API Key not found! Ensure it's set in the .env file or as an environment variable.")
        
        # print(f"Using API Key: {groq_api_key}")  # Debugging step
        self.client = Client(api_key=groq_api_key)
        self.chat_history = []  # Keep track of the conversation
        self.encoding = tiktoken.get_encoding("cl100k_base")  # Adjust as needed

    def add_message_to_history(self, role, content):
        """Adds a message to the conversation history."""
        self.chat_history.append({
            "role": role,
            "content": content
        })

    def generate_response(self, user_message):
        """Generate response by combining context with chat history."""
        # Add the user message to the history
        self.add_message_to_history("user", user_message)
        
        # Call Groq API with the chat history
        chat_completion = self.client.chat.completions.create(
            messages=self.chat_history,
            model="llama3-8b-8192"
        )
        
        # Extract response and add to the history
        response_content = chat_completion.choices[0].message.content
        self.add_message_to_history("assistant", response_content)

        return response_content
    
    def truncate_text(self, text, max_tokens=1500):

        # cleaned_text=clean_text(text)
        tokens = self.encoding.encode(text)
        
        if len(tokens) > max_tokens:
            tokens = tokens[:max_tokens]
        return self.encoding.decode(tokens)
    
    def clean_text(self,text):
        # If text is a list, join it into a single string
        if isinstance(text, list):
            text = " ".join(text)
        
        # Use regex to replace non-ASCII characters with a space
        cleaned_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        
        return cleaned_text
