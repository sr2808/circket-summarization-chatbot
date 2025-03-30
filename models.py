import os
from langchain_ollama import OllamaEmbeddings, ChatOllama

class Models:
    def __init__(self):
        self.embeddings_ollama = OllamaEmbeddings(
            model = "nomic-embed-text",   
        )

        self.model_ollama = ChatOllama(
            model = "mistral:7b-instruct-q4_K_M",
            temperature = 0,
        )

        


