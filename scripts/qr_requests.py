import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
  'Authorization': 'Bearer %s' % GITHUB_TOKEN,
    'Content-Type': 'application/json'
}

def run_query(url: str, query, variables=None):
    time.sleep(0.01)
    
    response = requests.post(
        url, json={"query": query, "variables": variables}, headers=HEADERS)
    if response.status_code == 200:
        return response.json(), response.status_code
    
    print(f"Erro na consulta GraphQL ({response.status_code})")
    time.sleep(1)
    
    return False, response.status_code

def run_rest(url: str):
    time.sleep(0.01)
    
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json(), response.status_code
    
    print(f"Erro na consulta REST ({response.status_code})")
    time.sleep(1)
    
    return False, response.status_code