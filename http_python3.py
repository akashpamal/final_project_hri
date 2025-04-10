import requests

# Define the URL of the Flask server endpoint
url = "http://127.0.0.1:5000/receive_json"

# Define the JSON payload to send
data = {
    "key": "value"
}

# Send the POST request
response = requests.post(url, json=data)

# Print the server's response
print("Response status code:", response.status_code)
print("Response JSON:", response.json())
