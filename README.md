# Quilibrium Node Exporter

Quilibrium Metrics Exporter for Prometheus provides access to your Quilibrium network node by exposing essential metrics to Prometheus. This should help make the job of monitoring your node health, performance, and other vital statistics much easier.

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

3. Expost the Quilibrium REST API:

   Edit your Quilibrium node config:
   ```bash
   nano /path/to/quilibrium/ceremonyclient/node/.config/config.yml
   ```

   Add to the bottom or edit an existing entry, and save:
   ```
   listenRESTMultiaddr: /ip4/127.0.0.1/tcp/8379
   ```

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

## Related Quilibrium community developments

   Another community member build a handy Quilibrium rust client:
   
   https://github.com/agostbiro/quilibrium-rs/tree/main/crates/quilclient


## Contributing

I love contributions! Feel free to open an issue or submit a PR!

## License

This project is licensed under the MIT License.
