from flask import Flask, jsonify, Response
import subprocess
import json

# Define the endpoint variable at the top
NODE_ENDPOINT = "http://127.0.0.1:8379/quilibrium.node.node.pb.NodeService"

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
    print(quil_metrics)
    # Return the combined data as JSON
    #return jsonify(quil_metrics)

    # Format the data for Prometheus
    prometheus_data = "\n".join(format_to_prometheus(quil_metrics))

    # Return the formatted data with the appropriate content type
    return Response(prometheus_data, content_type="text/plain")

def format_to_prometheus(data, prefix="", labels={}):
    """Recursively format JSON data to Prometheus text format."""
    output = []

    if isinstance(data, dict):
        for key, value in data.items():
            # Check if the child key string matches the parent key string and remove the child key string if it's an exact match
            new_prefix = prefix if prefix.lower() == key.lower() else f"{prefix}_{key}" if prefix else key
            output.extend(format_to_prometheus(value, new_prefix, labels))

    elif isinstance(data, list):
        if prefix and "index" not in labels:  # Only add index label if the list is nested directly inside a dictionary
            for index, item in enumerate(data):
                new_labels = labels.copy()
                new_labels["index"] = str(index)
                output.extend(format_to_prometheus(item, prefix, new_labels))
        else:
            for item in data:
                output.extend(format_to_prometheus(item, prefix, labels))

    elif isinstance(data, (str, int, float, bool)):
        label_str = ",".join([f'{k}="{v}"' for k, v in labels.items()]) if labels else ""
        label_part = "{" + label_str + "}" if label_str else ""
        metric = f"{prefix}{label_part} {data}"
        output.append(metric)

    return output


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8380)
