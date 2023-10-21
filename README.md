# Quilibrium Node Exporter

Quilibrium Metrics Exporter for Prometheus provides insights into the Quilibrium Blockchain node by exposing essential metrics to Prometheus. This enables administrators, developers, and other stakeholders to monitor node health, performance, and other vital statistics.

## Features

- **Easy Integration**: Designed to work out-of-the-box with Prometheus and Grafana.
- **Rich Metrics**: Gathers detailed metrics from the Quilibrium node, including peer information, network status, and more.
- **Scalable**: Suitable for monitoring individual nodes or a network of nodes.

## Prerequisites

- Python 3.x
- Flask
- A running instance of Quilibrium Blockchain node
- Prometheus & Grafana (for visualization)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/YourUsername/quilibrium-node-exporter.git
   cd quilibrium-node-exporter
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the exporter:

   ```bash
   python app.py
   ```

   By default, the exporter will run on port 8380.

2. Configure Prometheus to scrape from the exporter. Add the following to your `prometheus.yml`:

   ```yaml
   scrape_configs:
     - job_name: 'quilibrium_node_exporter'
       static_configs:
       - targets: ['localhost:8380']
   ```

3. Visualize the metrics in Grafana by connecting it to your Prometheus data source and creating custom dashboards.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more details.
