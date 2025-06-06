# imports

import os
import re
import math
import json
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from datasets import load_dataset
import chromadb
from items import Item
from testing import Tester
from agents.agent import Agent
import requests
from dotenv import load_dotenv
import torch 
from together import Together





class FrontierAgent(Agent):

    name = "Frontier Agent"
    color = Agent.BLUE

    MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
    
    def __init__(self, collection):
       
        load_dotenv(override=True)
        os.environ['TOGETHER_API_KEY'] = os.getenv('TOGETHER_API_KEY')
        self.TOGETHER_API_KEY=os.environ['TOGETHER_API_KEY']

        self.log("Initializing Frontier Agent")
        
        self.collection = collection
        # device="cuda" if torch.cuda.is_available() else "cpu"

        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        # self.model.to(torch.device(device))
        self.log("Frontier Agent is ready")

    def make_context(self, similars: List[str], prices: List[float]) -> str:
        
        message = "To provide some context, here are some other items that might be similar to the item you need to estimate.\n\n"
        for similar, price in zip(similars, prices):
            message += f"Potentially related product:\n{similar}\nPrice is ${price:.2f}\n\n"
        return message

    def messages_for(self, description: str, similars: List[str], prices: List[float]) -> List[Dict[str, str]]:
       
        system_message = "You estimate prices of items. Reply only with the price, no explanation"
        user_prompt = self.make_context(similars, prices)
        user_prompt += "And now the question for you:\n\n"
        user_prompt += "How much does this cost?\n\n" + description
        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": "Price is $"}
        ]

    def find_similars(self, description: str):
        
        self.log("Frontier Agent is performing a RAG search of the Chroma datastore to find 5 similar products")
        vector = self.model.encode([description])
        results = self.collection.query(query_embeddings=vector.astype(float).tolist(), n_results=5)
        documents = results['documents'][0][:]
        prices = [m['price'] for m in results['metadatas'][0][:]]
        self.log("Frontier Agent has found similar products")
        return documents, prices

    def get_price(self, s) -> float:
      
        s = s.replace('$','').replace(',','')
        match = re.search(r"[-+]?\d*\.\d+|\d+", s)
        return float(match.group()) if match else 0.0

    def price(self, description: str) -> float:
        
        documents, prices = self.find_similars(description)
        self.log(f"Frontier Agent is about to call {self.MODEL} with context including 5 similar products")

        

        client = Together() 

        response = client.chat.completions.create(
            model=self.MODEL,
            messages=self.messages_for(description, documents, prices),
        )
        


        data = response.choices[0].message.content
        reply = data.replace('$','').replace(',','')
        self.log(f"Frontier Agent completed - predicting ${result:.2f}")
        return self.get_price(reply)
        
        
        
        
       
        
