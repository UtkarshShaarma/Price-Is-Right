# imports

import os
import re
from typing import List
from sentence_transformers import SentenceTransformer
import joblib
from agents.agent import Agent



class RandomForestAgent(Agent):

    name = "Random Forest Agent"
    color = Agent.MAGENTA

    def __init__(self):
       
        self.log("Random Forest Agent is initializing")
        # device="cuda" if torch.cuda.is_available() else "cpu"

        # self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        # self.model.to(torch.device(device))
        self.vectorizer = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.model = joblib.load('random_forest_model.pkl')
        self.log("Random Forest Agent is ready")

    def price(self, description: str) -> float:
         
        self.log("Random Forest Agent is starting a prediction")
        vector = self.vectorizer.encode([description])
        result = max(0, self.model.predict(vector)[0])
        self.log(f"Random Forest Agent completed - predicting ${result:.2f}")
        return result

    # def __del__(self):
    #     print("Destructor called")
