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
   listenGrpcMultiaddr: /ip4/127.0.0.1/tcp/8378
   listenRESTMultiaddr: /ip4/127.0.0.1/tcp/8379
   ```

   Note: You must open the gRPC if you want REST to work!
   

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
      Quilibrium_LatestFrame_truncatedClockFrames_frameNumber{filter="NAAb50MsLmZpraAnl4hoKrn2JnGxtTirmVBGlNmBy9M="} 37414
      Quilibrium_LatestFrame_truncatedClockFrames_timestamp{filter="NAAb50MsLmZpraAnl4hoKrn2JnGxtTirmVBGlNmBy9M="} 1697364469374
      Quilibrium_LatestFrame_truncatedClockFrames_difficulty{filter="NAAb50MsLmZpraAnl4hoKrn2JnGxtTirmVBGlNmBy9M="} 10000
      ...
      Quilibrium_NetworkInfo_peerScore{peerId="QmdYYNKRvZYThJ7tP2A3RHfed3xrazNBiSLUrDnqNr83EZ",multiaddrs="['/ip4/198.98.109.189/udp/8336/quic']"} 100
      ...
      Quilibrium_PeerInfo_maxFrame{peerId="QmZfPwUNk3hFSVRvMtijqxBYkxmrPix2Zd7gbZdZQe65Dp",multiaddrs="['/ip4/147.135.62.9/udp/8336/quic']"} 209
      Quilibrium_PeerInfo_timestamp{peerId="QmZfPwUNk3hFSVRvMtijqxBYkxmrPix2Zd7gbZdZQe65Dp",multiaddrs="['/ip4/147.135.62.9/udp/8336/quic']"} 1699245754932
      ...
      Quilibrium_PeerInfo_uncooperativePeerInfo_maxFrame{peerId="QmaffYBcwMgMNz5KhkhpJuWg6kChX7TmdZ8hexz8de8TWA",multiaddrs="['/ip4/70.187.187.239/udp/8336/quic']"} 53799
      ...
      Quilibrium_TokenInfo_confirmedTokenSupply 90585200000000000
      Quilibrium_TokenInfo_unconfirmedTokenSupply 90585200000000000
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

   Configure Grafana with a Prometheus datasource URL of `http://localhost:9090` and import the JSON located in this repo under `/grafana` for a copy of the Quilibrium Network Dashboard.


## Setting up Grafana on a Subdomain (optional)

- Modify your domain DNS to include an A record with the name you prefer and the IP of your server.
- Uncomment `domain = ` in `grafana.ini` and set it to your full subdomain:

   ```bash
   sudo nano /etc/grafana/grafana.ini
   ```
   
   Example:
   ```
   somesubdomain.yourdomain.tld
   ```
   

- Set up the reverse proxy using Nginx:

   Install Nginx and create a site:
   ```bash
   sudo apt update
   sudo apt install nginx
   
   ```
   
  Add the server block:
  ```bash
  sudo nano /etc/nginx/sites-available/somesubdomain.yourdomain.tld
  ```

  Contents of server block (80  for now, but will be updated by certbot)
  ```
   server {
       listen 80;
       server_name somesubdomain.yourdomain.tld;
   
       location / {
           proxy_pass http://localhost:3000; # Forward requests to Grafana
           proxy_set_header Host $host; # Pass the host header - important for virtual hosting
           proxy_set_header X-Real-IP $remote_addr; # Pass the real client IP to Grafana
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; # Manage the forwarded-for header
           proxy_set_header X-Forwarded-Proto $scheme; # Manage the forwarded-proto header
       }
   }
  ```

   Enable the site for nginx to serve:
   ```bash
   sudo ln -s /etc/nginx/sites-available/somesubdomain.yourdomain.tld /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   sudo systemctl enable nginx
   ```

- Allow the site through the firewall for HTTP (DCV) and HTTPS traffic:

   ```bash
   sudo ufw allow 80
   sudo ufw allow 443
   ```

- Set up SSL with Let's Encrypt:

   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d somesubdomain.yourdomain.tld
   ```


## Related Quilibrium community developments

   Another community member build a handy Quilibrium rust client:
   
   https://github.com/agostbiro/quilibrium-rs/tree/main/crates/quilclient


## Contributing

I love contributions! Feel free to open an issue or submit a PR!

## License

This project is licensed under the MIT License.
