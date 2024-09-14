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

class LLMResponseGenerator:
    def __init__(self):
        # Retrieve the API key from the environment
        api_key = "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"
        self.client = Groq(api_key=api_key)
        self.chat_history = []  # Keep track of the conversation

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
