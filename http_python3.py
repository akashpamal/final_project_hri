import requests

# Define the URL of the Flask server endpoint
url = "http://127.0.0.1:5001/receive_json"

# Define the JSON payload to send
data = {
    # "key": "value"
    "movementType": "coordinate",
    'chainName': "RArm",
    'position': [0.11874917894601822, -0.1331220269203186, -0.0442596971988678, 1.216969609260559, 0.4153057336807251, -0.012792954221367836],  # Example coordinates
}

# Send the POST request
print('sending request')
response = requests.post(url, json=data)
print('request sent')

# Print the server's response
print("Response status code:", response.status_code)
print('response:', response.text)
# print("Response JSON:", response.json())
