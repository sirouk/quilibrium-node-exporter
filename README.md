# Quilibrium Node Exporter

This Quilibrium metrics exporter is a tool that should simplify the task of exposing metrics from your Quilibrium network node for consumption by Prometheus. This is a basic start, but will eventually provide robust data to help you monitor node health, performance, and other vital statistics.

I will continue to add additional metrics as they become available.

Feel free to contribute!


## Features

- Designed to work out-of-the-box with the latest release of [Quilibrium node](https://github.com/quilibriumnetwork/ceremonyclient)
- Gathers detailed metrics from the Quilibrium node into a single call
- Suitable for monitoring an individual node

## Prerequisites

- Python 3.x
- Flask
- A running instance of Quilibrium network node with REST endpoint exposed (locally)
- Prometheus and Grafana

## Installation

1. Clone the repository:

   ```bash
   cd ~
   git clone https://github.com/sirouk/quilibrium-node-exporter
   
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
      exporter.log  grafana  Makefile  next_frame_number  quilibrium-node-exporter.py  README.md
      curl 127.0.0.1:8380/metrics
      Quilibrium_LatestFrame_truncatedClockFrames_frameNumber{filter="NAAb50MsLmZpraAnl4hoKrn2JnGxtTirmVBGlNmBy9M="} 20340
      Quilibrium_LatestFrame_truncatedClockFrames_timestamp{filter="NAAb50MsLmZpraAnl4hoKrn2JnGxtTirmVBGlNmBy9M="} 1697517372546
      Quilibrium_LatestFrame_truncatedClockFrames_difficulty{filter="NAAb50MsLmZpraAnl4hoKrn2JnGxtTirmVBGlNmBy9M="} 10000
      ...
      Quilibrium_NetworkInfo_peerScore{peerId="EiDBqssLUs550bRROG5rT7Gh2ZSUD3yJt1sG+cR+KfEJbw==",multiaddrs="['/ip4/23.139.82.67/udp/8336/quic']"} 0
      Quilibrium_NetworkInfo_peerScore{peerId="EiDDuejVIWjWB2EkgmzmTMXS0sWKWASp2xbiZ/w048hgLg==",multiaddrs="['/ip4/147.135.105.14/udp/8336/quic']"} 0
      Quilibrium_NetworkInfo_peerScore{peerId="EiDLg4I2+SAV7f0dUfT/qwDJWAstv1CAYmbhvJG3LxrgZw==",multiaddrs="['/ip4/65.109.17.13/udp/8336/quic']"} 0
      Quilibrium_NetworkInfo_peerScore{peerId="EiB+FoAYEbJ0RVI9L1rjxelLzUrbaHP1aOn/SQBbuVTFrA==",multiaddrs="['/ip4/65.109.17.24/udp/8336/quic']"} 0
      ...
      Quilibrium_PeerInfo_maxFrame{peerId="EiCgtRXQ+69xr3xSexZjmmBo9as5fmdXfeMAmee0LSRhHA==",multiaddrs="['']"} 0
      Quilibrium_PeerInfo_maxFrame{peerId="EiCtKApm4Z9at1keNK+D9G+qtcZjcmOYorFsIdgBP4jxMQ==",multiaddrs="['']"} 0
      Quilibrium_PeerInfo_maxFrame{peerId="EiAjhP9B5faB5+2IZI2cSm+FPfw9pfB7SL7AYDGlK4h4AQ==",multiaddrs="['/ip4/95.217.131.173/udp/8336/quic']"} 0
      Quilibrium_PeerInfo_maxFrame{peerId="EiDhS3+6Vc3SaMdJpYtrX5fnRS5ZRDEfF8vx+iOwWIO6Bw==",multiaddrs="['/ip4/167.235.142.205/udp/8336/quic']"} 224
      Quilibrium_PeerInfo_maxFrame{peerId="EiDZobodlnDZ/nNPhlDlw29XUQlevuKLopzM4rsMC7keCA==",multiaddrs="['/ip4/13.236.219.103/udp/8317/quic']"} 15487
      ...
      Quilibrium_PeerInfo_uncooperativePeerInfo_maxFrame{peerId="EiC3Kzc7YMFvjTQJNRzg3epEfqa2pf0HBUi7mO6/r4g0aw==",multiaddrs="['']"} 21950
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

   Configure Grafana and import the JSON located in this repo under `/grafana`

## Related Quilibrium community developments

   Another community member build a handy Quilibrium rust client:
   
   https://github.com/agostbiro/quilibrium-rs/tree/main/crates/quilclient


## Contributing

I love contributions! Feel free to open an issue or submit a PR!

## License

This project is licensed under the MIT License.
