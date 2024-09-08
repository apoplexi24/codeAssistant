import json
import os
import uvicorn
from fastapi import FastAPI
from routes.email_route import email_router

class codingAssistant():
    def __init__(self) -> None:
        self.app = FastAPI()
        
        self.routes_list = [
            email_router
        ]
    
    def initialize_api_routes(self):
        for router in self.routes_list:
            try:
                self.app.include_router(router)
            except Exception as e:
                print(f"Error while initializing route {router}. Error => ", e)

    def run(self):
        self.initialize_api_routes()
        uvicorn.run(self.app, host="0.0.0.0", port=8000)
    
    