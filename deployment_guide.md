# Deployment Guide (Simplified)

This guide will help you deploy the Crypto ETL Backend to a cloud provider like **AWS EC2** or **DigitalOcean**.

## Prerequisites
-   A Cloud Account (AWS, Google Cloud, or DigitalOcean).
-   Terminal access on your local machine.
-   (Optional) A GitHub repository for your code.

---

## Quickstart: AWS EC2 (Ubuntu)

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

## Scheduling ETL (Cron)

Since the app is running, you want to trigger the ETL process every hour.

1.  On the server, open crontab:
    ```bash
    crontab -e
    ```
2.  Add this line to run every hour:
    ```bash
    0 * * * * curl -X POST -H "X-API-Key: test-key" http://localhost:8000/etl/run >> /home/ubuntu/etl.log 2>&1
    ```

## Viewing Logs

To see what's happening:
```bash
# View app logs
sudo docker-compose logs -f app
```
