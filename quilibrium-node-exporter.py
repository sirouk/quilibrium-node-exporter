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
                            # Check if the value is an integer or an integer represented as a string
                            if isinstance(value, int) or (isinstance(value, str) and value.isdigit()):
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
    app.run(host='127.0.0.1', port=8380)
