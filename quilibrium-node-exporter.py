import os
import base64
import base58
from flask import Flask, jsonify, Response
import subprocess
import json


FRAME_FILE = "next_frame_number"
NODE_ENDPOINT = "http://127.0.0.1:8379/quilibrium.node.node.pb.NodeService"

base58_keys = ["peerId"]
bigEndianKeys = ["unconfirmedTokenSupply", "confirmedTokenSupply", "ownedTokens"]

app = Flask(__name__)


def fetch_data(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return json.loads(result.stdout)

def is_valid_base64(input_string):
    try:
        decoded_string = base64.b64decode(input_string, validate=True)
        return True
    except Exception as e:
        return False

def get_last_frame():
    if os.path.exists(FRAME_FILE):
        with open(FRAME_FILE, 'r') as file:
            return int(file.read().strip())
    return get_peer_max_frame()

def set_next_frame(frame_number):
    with open(FRAME_FILE, 'w') as file:
        file.write(str(frame_number))

def get_peer_max_frame():
    peer_info = fetch_data(['curl', '-sX', 'POST', f'{NODE_ENDPOINT}/GetPeerInfo'])
    max_frames = 0
    for peer in peer_info.get('peerInfo'):
        peer_mf = int(peer.get('maxFrame', 0))
        if peer_mf > max_frames:
            max_frames = peer_mf
    return max_frames

def fetch_frame_data(from_frame, to_frame):
    command = [
        'curl', '-sX', 'POST', f'{NODE_ENDPOINT}/GetFrames',
        '-H', 'Content-Type: application/json',
        '-d', f'{{"from_frame_number":{from_frame}, "to_frame_number":{to_frame}, "include_candidates": true}}'
    ]
    #print(command)
    result = subprocess.run(command, capture_output=True, text=True)
    return json.loads(result.stdout)

def get_latest_frame():
    last_frame = get_last_frame()
    last_data = []
    direction = -1  # start by going backwards

    while True:
        from_frame = last_frame
        to_frame = last_frame + 1

        #print(f"Trying frame: {to_frame}")

        # fetching data
        data = fetch_frame_data(from_frame, to_frame)
        #print("Data:")
        #print(data)

        frame_exists = data.get('truncatedClockFrames') and \
                       data['truncatedClockFrames'][0].get('frameNumber')

        # If frame doesn't exist and we're going backwards
        if not frame_exists and direction == -1:
            last_frame += direction

        # If frame exists and we're going backwards
        elif frame_exists and direction == -1:
            direction = 1  # change direction to forwards
            last_data = data  # update last_data
            last_frame += direction

        # If frame exists and we're going forwards
        elif frame_exists and direction == 1:
            last_data = data  # update last_data
            last_frame += direction

        # If frame doesn't exist and we're going forwards
        elif not frame_exists and direction == 1:
            break

    # Update the file to contain the next frame pointer
    set_next_frame(from_frame)
    return last_data


@app.route('/metrics')
def combined_data():
    # Use the NODE_ENDPOINT variable in the curl commands
    latest_frame = get_latest_frame()
    network_info = fetch_data(['curl', '-sX', 'POST', f'{NODE_ENDPOINT}/GetNetworkInfo'])
    peer_info = fetch_data(['curl', '-sX', 'POST', f'{NODE_ENDPOINT}/GetPeerInfo'])
    token_info = fetch_data(['curl', '-sX', 'POST', f'{NODE_ENDPOINT}/GetTokenInfo'])
    
    # Combine the data
    quil_metrics = {
	    "LatestFrame": latest_frame,
        "NetworkInfo": network_info,
        "PeerInfo": peer_info,
        "TokenInfo": {"tokenInfo": [token_info]}
    }
    #print(quil_metrics)

    # Return the combined data as JSON
    #return jsonify(quil_metrics)

    # Format the data for Prometheus
    prometheus_data = "\n".join(format_to_prometheus(quil_metrics))

    # Return the formatted data with the appropriate content type
    return Response(prometheus_data, content_type="text/plain")

def format_to_prometheus(data):
    """Format data to Prometheus text format ensuring non-repetitive key names."""
    output = []

    for main_key, main_value in data.items():
        if isinstance(main_value, dict):
            for sub_key, sub_value in main_value.items():
                if isinstance(sub_value, list):
                    for index, item in enumerate(sub_value):
                        labels = {}
                        # Avoid extending the key name with the same value
                        metric_name = f"Quilibrium_{main_key}" if main_key.lower() == sub_key.lower() else f"Quilibrium_{main_key}_{sub_key}"

                        for key, value in item.items():
                            #print(value)

                            if key in bigEndianKeys and is_valid_base64(value):
                                 # Base64 decode the value
                                decoded_bytes = base64.b64decode(value)

                                # Convert the value to big endian
                                value = int.from_bytes(decoded_bytes, byteorder='big')

                                # Combine the base metric name with the current key to create a unique metric name
                                complete_metric_name = metric_name + f"_{key}"
                                label_str = ",".join([f'{k}="{v}"' for k, v in labels.items()])
                                label_part = "{" + label_str + "}" if label_str else ""
                                metric = f"{complete_metric_name}{label_part} {int(value)}"
                                output.append(metric)

                            elif key in base58_keys and is_valid_base64(value):
                                # Base64 decode the value
                                decoded_bytes = base64.b64decode(value)
                                # Base58 encode the decoded bytes
                                encoded_peerId = base58.b58encode(decoded_bytes).decode('utf-8')
                                # Update the labels dictionary with the newly encoded value
                                labels[key] = encoded_peerId

                            # Check if the value is an integer or an integer represented as a string
                            elif isinstance(value, int) or (isinstance(value, str) and value.isdigit()):
                                # Combine the base metric name with the current key to create a unique metric name
                                complete_metric_name = metric_name + f"_{key}"
                                label_str = ",".join([f'{k}="{v}"' for k, v in labels.items()])
                                label_part = "{" + label_str + "}" if label_str else ""
                                metric = f"{complete_metric_name}{label_part} {int(value)}"
                                output.append(metric)

                            else:
                                labels[key] = value

    return output


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8381)
