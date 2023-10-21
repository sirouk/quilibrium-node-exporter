# Quilibrium Node Exporter

This Quilibrium metrics exporter is a tool that should simplify the task of exposing metrics from your Quilibrium network node for consumption by Prometheus. This is a basic start, but will eventually provide robust data to help you monitor node health, performance, and other vital statistics.

I will continue to add additional metrics as they become available. Eventually, I will add a Grafana template. 

Feel free to contribute!


## Features

- Designed to work out-of-the-box with the latest release of [Quilibrium node](https://github.com/quilibriumnetwork/ceremonyclient)
- Gathers detailed metrics from the Quilibrium node into a single call
- Suitable for monitoring an individual node

## Prerequisites

- Python 3.x
- Flask
- A running instance of Quilibrium network node with REST endpoint exposed (locally)
- Prometheus (Grafana details will be added later for consuming Prometheus and providing visualization)

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
