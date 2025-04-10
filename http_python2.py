from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receive_json', methods=['POST'])
def receive_json():
    # Parse JSON data from the request
    data = request.get_json()
    print("Received JSON:", data)
    
    # Respond with a success message
    return jsonify({"status": "success", "received_data": data})

if __name__ == '__main__':
    app.run(port=5001)
    
"""
{
    "movement_type": "coordinate" // or "angle",
    "joint_name": "LShoulderRoll",
    "joint_angles": [0.5, 0.6, 0.7], // or "joint_coordinates": [0.1, 0.2, 0.3]
}
"""
