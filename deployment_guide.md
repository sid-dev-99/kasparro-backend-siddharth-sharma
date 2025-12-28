# Deployment Guide

This guide will help you deploy the Crypto ETL Backend to a cloud provider like **Railway**, **AWS EC2**, or **DigitalOcean**.

## Option 1: Railway (Recommended for Ease of Use)

Railway is a PaaS that makes deployment extremely simple.

### 1. Prerequisites
- A GitHub account with this repository pushed.
- A [Railway](https://railway.app/) account.

### 2. Deploy the Web Service
1.  Log in to Railway and click **New Project**.
2.  Select **Deploy from GitHub repo**.
3.  Choose your repository (`kasparro-backend`).
4.  Railway will automatically detect the `Procfile` and start building.
5.  Once deployed, go to **Settings** -> **Variables** and add your environment variables:
    - `API_KEY`: Your secret API key.
    - `COINPAPRIKA_API_KEY`: (Optional)
    - `COINGECKO_API_KEY`: (Optional)
6.  Go to **Settings** -> **Networking** to see your public URL (e.g., `https://kasparro-backend-production.up.railway.app`).

### 3. Schedule ETL (Cron Job)
1.  In your Railway project, click **New** -> **Service**.
2.  Select **GitHub Repo** again and choose the same repository.
3.  Click on the new service to open its settings.
4.  Go to **Settings** -> **General** -> **Build Command**. Leave it empty or default.
5.  Go to **Settings** -> **General** -> **Start Command**. Change it to:
    ```bash
    python -m app.ingestion.runner
    ```
6.  Go to **Settings** -> **Cron Schedule**.
    - Enable Cron.
    - Set the schedule (e.g., `0 * * * *` for every hour).
    - This service will now wake up, run the ETL script, and shut down.

### 4. Viewing Logs
- Click on either service (Web or Cron) in the Railway dashboard.
- Click **Logs** to see real-time output.

---

## Option 2: AWS EC2 (Ubuntu)

### 1. Launch an Instance
1.  Log in to AWS Console and go to **EC2**.
2.  Click **Launch Instance**.
3.  **Name**: `CryptoBackend`.
4.  **OS Image**: Choose **Ubuntu Server 22.04 LTS**.
5.  **Instance Type**: `t2.micro` (Free tier eligible) or `t3.small`.
6.  **Key Pair**: Create a new key pair (e.g., `crypto-key.pem`) and download it.
7.  **Network Settings**:
    -   Check **Allow SSH traffic from** (My IP).
    -   Check **Allow HTTP traffic from the internet**.
    -   Check **Allow HTTPS traffic from the internet**.
    -   **IMPORTANT**: You must also open port **8000**.
        -   Click "Edit" in Network Settings.
        -   Add Security Group Rule: Custom TCP, Port `8000`, Source `0.0.0.0/0` (Anywhere).
8.  Click **Launch Instance**.

### 2. Connect to the Instance
Open your terminal where you downloaded the key pair (`crypto-key.pem`).

```bash
# Set permissions for the key
chmod 400 crypto-key.pem

# Connect via SSH (replace 1.2.3.4 with your Instance Public IP)
ssh -i "crypto-key.pem" ubuntu@1.2.3.4
```

### 3. Upload Code
You have two options to get your code onto the server:

**Option A: Git Clone (Recommended)**
If your code is on GitHub (and public, or you have keys set up):
```bash
# On the server
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git app
```

**Option B: SCP (Copy from Local)**
If your code is only on your laptop:
```bash
# Run this from your LOCAL project folder
# Replace 1.2.3.4 with your Instance Public IP
scp -i "path/to/crypto-key.pem" -r . ubuntu@1.2.3.4:~/app
```

### 4. Install & Run (On the Server)
Go back to your **SSH terminal** (connected to the server).

```bash
# Go to the app folder
cd ~/app

# Make the setup script executable
chmod +x setup_cloud_vm.sh

# Run the setup script (Installs Docker & Starts App)
sudo ./setup_cloud_vm.sh
```

### 5. Verify
Once the script finishes, your app is live!

-   **Health Check**:
    ```bash
    curl -H "X-API-Key: test-key" http://1.2.3.4:8000/health
    ```
-   **Browser**: Visit `http://1.2.3.4:8000/docs` (You might need to authorize with the button using `test-key` if I added auth to docs, otherwise just use curl).

---

## Scheduling ETL (Cron) on EC2

Since the app is running, you want to trigger the ETL process every hour.

1.  On the server, open crontab:
    ```bash
    crontab -e
    ```
2.  Add this line to run every hour:
    ```bash
    0 * * * * curl -X POST -H "X-API-Key: test-key" http://localhost:8000/etl/run >> /home/ubuntu/etl.log 2>&1
    ```

## Viewing Logs on EC2

To see what's happening:
```bash
# View app logs
sudo docker-compose logs -f app
```
