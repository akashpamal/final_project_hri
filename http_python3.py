import requests

# Define the URL of the Flask server endpoint
url = "http://127.0.0.1:5001/receive_json"

# Define the JSON payload to send
data = {
    # "key": "value"
    "movementType": "coordinate",
    'chainName': "LArm",
    'position': [0.21874918639659882, 0.233122056722641, 0.05574030280113221, -1.2169694900512695, 0.4153057932853699, 0.012793183326721191],  # Example coordinates
}

# Send the POST request
print('sending request')
response = requests.post(url, json=data)
print('request sent')

# Print the server's response
print("Response status code:", response.status_code)
print('response:', response.text)
# print("Response JSON:", response.json())
