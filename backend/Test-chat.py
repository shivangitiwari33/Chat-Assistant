import requests

URL = "http://127.0.0.1:3000/query"

queries = [
    "show me all employees in Sales department",
    "who is the manager of Engineering department?",
    "list all employees hired after 2020-06-10",
    "what is the total salary expense for Marketing department?",
    "show me all employees in HR department",
    "who is the manager of Finance department?",
    "list all employees hired after 2019-01-01",
    "what is the total salary expense for Sales department?",
    "show me all employees in a nonexistent department",
    "who is the manager of an Tech department?",
    "list all employees hired after 2025-01-01",
    "what is the total salary expense for HR department?"
]

for query in queries:
    response = requests.post(URL, json={"query": query})
    print(f"Query: {query}")
    
    # Check if response is valid
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
    
    print("-" * 50)
