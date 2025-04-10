from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receive_json', methods=['POST'])
def receive_json():
    # Parse JSON data from the request
    print("Received JSON request")
    data = request.get_json()
    print("Received JSON:", data)
    
    # Respond with a success message
    return jsonify({"status": "success", "received_data": data})

if __name__ == '__main__':
    app.run(port=5000)
