from flask import Flask, jsonify
import subprocess
import json

# Define the endpoint variable at the top
NODE_ENDPOINT = "http://127.0.0.1:8417/quilibrium.node.node.pb.NodeService"

app = Flask(__name__)

def fetch_data(command):
    """Helper function to fetch data using curl command."""
    result = subprocess.run(command, capture_output=True, text=True)
    return json.loads(result.stdout)

@app.route('/metrics')
def combined_data():
    # Use the NODE_ENDPOINT variable in the curl commands
    network_info = fetch_data(['curl', '-X', 'POST', f'{NODE_ENDPOINT}/GetNetworkInfo'])
    peer_info = fetch_data(['curl', '-X', 'POST', f'{NODE_ENDPOINT}/GetPeerInfo'])

    # Combine the data
    quil_metrics = {
        "NetworkInfo": network_info,
        "PeerInfo": peer_info
    }

    # Return the combined data as JSON
    return jsonify(quil_metrics)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8380)
