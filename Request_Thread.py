import requests
import threading
import json
import time

class Request_Thread(threading.Thread):
    

    def __init__(self, url):
        super().__init__()
        self.response = {}
        self.status_code = 0
        self.url = url

    def run(self):
        response = requests.get(f"{self.url}")
        self.status_code = response.status_code
        response = requests.get(self.url)
        self.status_code = response.status_code

        if response.status_code == 200:
            print(f"Fetching data: {self.url}")
            self.response = response.json()
        
        else:
            print(f'Response Error: {response.status_code} - {response.text}')