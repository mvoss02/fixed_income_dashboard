# Bond Analytics Dashboard

A streamlined dashboard for analyzing fixed income securities, featuring U.S. Treasury yield curves, corporate bond comparisons, and portfolio analytics.

![Bond Analytics Dashboard](https://github.com/yourusername/bond-analytics-dashboard/raw/main/docs/images/dashboard-preview.png)

## 🌟 Features

- **Interactive Yield Curves**: View Treasury yield curves for any date in the past year
- **ESG Proxy Analysis**: Compare high-quality (AAA) and lower-grade (BAA) corporate bonds against Treasury benchmarks
- **Historical Trend Visualization**: Track key metrics like 10-year Treasury yields and the 10Y-2Y spread over time
- **Portfolio Summary**: Analyze weighted yields and performance of a sample bond portfolio
- **Comprehensive Bond Data**: Access data for multiple Treasury and corporate bond series

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone git@github.com:mvoss02/fixed_income_dashboard.git
cd fixed_income_dashboard

# Build and run the Docker container
make run-docker

# Access the dashboard
# Open your browser and navigate to http://localhost:8501
```

### Manual Setup

```bash
# Clone the repository
git clone git@github.com:mvoss02/fixed_income_dashboard.git
cd fixed_income_dashboard

# Install dependencies using uv
uv sync

# Fetch the latest bond data
make ingest-data

# Run the dashboard locally
make run

# Build and run docker container
make run-docker
```

## 📊 Data Sources

The dashboard uses the following bond data series from the Federal Reserve Economic Data (FRED):

| Series         | Description                                    | Category  |
| -------------- | ---------------------------------------------- | --------- |
| DGS1MO - DGS30 | Treasury Constant Maturity Rates (1mo to 30yr) | Treasury  |
| AAA            | Moody's Seasoned Aaa Corporate Bond Yield      | Corporate |
| BAA            | Moody's Seasoned Baa Corporate Bond Yield      | Corporate |
| T10Y2Y         | 10-Year minus 2-Year Treasury Yield Spread     | Trend     |

## 🛠️ Project Structure

```
fixed_income_dashboard/
├── data/                      # Parquet files for bond data
├── services/
│   ├── data_ingestion/        # Scripts for fetching and processing bond data
├── Dockerfile                 # Container configuration
├── pyproject.toml            # Project dependencies
├── run.py                    # Main Streamlit application
├── Makefile                  # Automation commands
└── README.md                 # Project documentation
```

## 🖥️ Deployment

### Hosting on a Virtual Machine

1. **Provision a VM** (AWS EC2, Google Cloud Compute, DigitalOcean Droplet, etc.)
   Note: Allow http and SSH connections!

2. **SSH into your VM (For Azure)**:
   After saving the .pem file in a desired directory, connect to the VM:

   ```bash
   chmod 400 ~/.ssh/<your-private-key> # Allows only to read ssh key
   ssh -i ~/.ssh/FILE_NAME.pem USERNAME@IP-Address
   ```

3. **Install Docker** on your VM:

   ```bash
   # For Ubuntu/Debian
   sudo apt update && sudo apt install -y python3-pip nginx
   sudo apt update && sudo apt install docker.io  docker-buildx
   sudo systemctl enable --now docker

   # Add your user to docker group (optional)
   sudo usermod -aG docker $USER
   # Log out and back in for changes to take effect
   ```

4. **Setup nginx**

```bash
sudo vim /etc/nginx/site-enabled/streamlit_nginx
```

Nginx config for easy routing and websocket support (required for streamlit):

```
server {
    listen 80;
    server_name YOUR_PUBLIC_IP_OR_DOMAIN_NAME;

    location / {
        proxy_pass http://IP_ADDRESS:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

5. **Clone and deploy**:

   ```bash
   git clone https://github.com/mvoss02/fixed_income_dashboard.git
   cd fixed_income_dashboard
   make run-docker
   ```

6. **Configure Firewall** to allow access to port 8501 (or your chosen port)

7. **Access your dashboard** at `http://your-vm-ip/`

### Setting up Automatic Updates

Create a simple cron job to periodically fetch new data:

```bash
# Open crontab editor
crontab -e

# Add a daily update job (runs at 1:00 AM)
0 1 * * * cd /path/to/bond-analytics-dashboard && make ingest-data && make stop-docker && make run-docker
```

## 📝 Makefile Commands

- `make run` - Run the Streamlit app locally
- `make run-docker` - Build and run the Docker container
- `make stop-docker` - Stop any running Docker containers
- `make ingest-data` - Fetch the latest bond data

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
