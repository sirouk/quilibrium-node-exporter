# Quilibrium Node Exporter

Quilibrium Metrics Exporter for Prometheus provides insights into the Quilibrium network node by exposing essential metrics to Prometheus. This enables node operators to monitor node health, performance, and other vital statistics. 

I will continue to add additional metrics as they become available. Feel free to open an issue for suggestions!

## Features

- Designed to work out-of-the-box with the latest release of Quilibrium node
- Gathers detailed metrics from the Quilibrium node, including peer information, network status, and more.
- Suitable for monitoring individual nodes.

## Prerequisites

- Python 3.x
- Flask
- A running instance of Quilibrium network node with REST endpoint exposed (locally)
- Prometheus & Grafana (for visualization, steps and template will be added later)

## Installation

1. Clone the repository:

   ```bash
   cd ~
   git clone https://github.com/YourUsername/quilibrium-node-exporter.git
   
   ```

2. Install the required packages:

   ```bash
   cd ~/quilibrium-node-exporter
   make install
   ```

## Usage

3. Start the exporter:

   ```bash
   make start-cron
   ```

   By default, the exporter will run on port 8380. You can run this in a cron by the minute, it will only run once.

   To stop:
   ```bash
   make stop-cron
   ```
4. Test the output:

   ```bash
   make check
   ```

   You will see the repo files and one output frame:
   ```
      cd ~/quilibrium-node-exporter
      ls
      exporter.log  Makefile  quilibrium-node-exporter.py  README.md
      curl 127.0.0.1:8380/metrics | jq
        % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                       Dload  Upload   Total   Spent    Left  Speed
      100 59906  100 59906    0     0  3265k      0 --:--:-- --:--:-- --:--:-- 3656k
      {
        "NetworkInfo": {
          "networkInfo": [
            {
              "multiaddrs": [
                "/ip4/51.81.214.68/udp/8336/quic"
              ],
              "peerId": "EiB89GnA0DEEes4RXAyLBJesXJSYjplUSkgpTNaoWBLsEw==",
              "peerScore": 0
            },
            {
              "multiaddrs": [
                "/ip4/147.135.105.209/udp/8336/quic"
              ],
              "peerId": "EiDyQ/H+unN8ABzy3jMO8AXqqRWMkdpp9S5Qo5KxsRk0yA==",
              "peerScore": 0
            },
      ...
   ```

4. Configure Prometheus to scrape from the exporter.
    
   Add the following to your `prometheus.yml`:
   ```yaml
   scrape_configs:
     - job_name: 'quilibrium_node_exporter'
       static_configs:
       - targets: ['localhost:8380']
   ```

5. Visualize the metrics in Grafana by connecting them to your Prometheus data source and creating custom dashboards.

## Contributing

I love contributions! Feel free to 

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more details.
