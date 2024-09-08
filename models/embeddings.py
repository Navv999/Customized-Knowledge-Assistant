from transformers import AutoTokenizer, AutoModel
import torch

# Example with Hugging Face's BERT model
class Embedder:
    def __init__(self, model_name='bert-base-uncased'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
    
    def generate_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():   
            outputs = self.model(**inputs)
        # Pool the model outputs (mean pooling)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.squeeze().numpy()
