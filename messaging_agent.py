import os
from agents.deals import Opportunity
import http.client
import urllib
from agents.agent import Agent


DO_TEXT = False
DO_PUSH = True

class MessagingAgent(Agent):

    name = "Messaging Agent"
    color = Agent.WHITE

    def __init__(self):
    
        self.log(f"Messaging Agent is initializing")
 
        self.pushover_user = os.getenv('PUSHOVER_USER')
        self.pushover_token = os.getenv('PUSHOVER_TOKEN')
        self.log("Messaging Agent has initialized Pushover")

    def message(self, text):
        
        self.log("Messaging Agent is sending a text message")
        message = self.client.messages.create(
          from_=self.me_from,
          body=text,
          to=self.me_to
        )

    def push(self, text):
        

        self.log("Messaging Agent is sending a push notification")
        
        
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        
        conn.request("POST", "/1/messages.json",
        
          urllib.parse.urlencode({
            "token": self.pushover_token,
            "user": self.pushover_user,
            "message": text,
            "sound": "cashregister"
          }), { "Content-type": "application/x-www-form-urlencoded" })
        
        conn.getresponse()

    def alert(self, opportunity: Opportunity):
   
        text = f"Deal Alert! Price=${opportunity.deal.price:.2f}, "
        text += f"Estimate=${opportunity.estimate:.2f}, "
        text += f"Discount=${opportunity.discount:.2f} :"
        text += opportunity.deal.product_description[:10]+'... '
        text += opportunity.deal.url
        if DO_TEXT:
            self.message(text)
        if DO_PUSH:
            self.push(text)
        self.log("Messaging Agent has completed")
        
    
        