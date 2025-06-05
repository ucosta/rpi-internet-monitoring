
# Raspberry Pi Internet Monitoring System - Installation Guide
This project monitors internet connectivity using two main scripts on a Raspberry Pi running Raspbian OS. It sends notifications via email and Telegram when internet connectivity is restored.

# Table of Contents
1. [Scripts Overview](#scripts-overview)
2. [Pre-reqs](#pre-reqs)
3. [Initial Setup](#initial-setup)
	1. [DuckDNS Configuration](#duckdns-configuration)
	2.  [Telegram Bot Setup](#telegram-bot-setup)
	3. [Gmail App Key Configuration](#gmail-app-key-configuration)
4. [Installation Guide](#installation-guide)
	1. [Script Configuration](#script-configuration)
		1. [duck.sh](#duck-sh)
		2. [monitor.py](#monitor-py)
		3. [server.py](#server-py)
	2. [Systemd Service Installation](#systemd-service-installation)
	3. [Validation](#validation)
5. [Troubleshooting](#troubleshooting)
# Scripts Overview <a name="scripts-overview"></a>

-   **monitor.py**: Checks internet connectivity and sends notifications via email and Telegram when the internet is restored.
-   **server.py**: Simulates an HTTP server that listens for connections and responds with **"It's Alive!"**.
-   **duck.sh**: Updates DuckDNS URL for dynamic DNS service.

# Pre-reqs <a name="pre-reqs"></a>

- Raspberry Pi running Raspberry Pi OS (32-bit or 64-bit)
- **Python 3**: Ensure Python 3 is installed on your Raspberry Pi.
- **Pip**: Make sure pip is installed (`sudo apt-get install python3-pip`).
- Active internet connection
- Terminal access (SSH or direct)

# Initial Setup <a name="initial-setup"></a>

1. Update system packages:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
2. Install required packages:
   ```bash
   sudo apt install -y python3-pip python3-venv curl
   ```
4. Install the necessary Python libraries:
    ```sh
    pip install requests
    ```     
4. Clone the git repository:
    ```bash
    git clone https://github.com/ucosta/rpi-internet-monitoring.git
    ```
5. Set up Python virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install requests
    ```
## DuckDNS Configuration <a name="duckdns-configuration"></a>
1. Sign up at www.duckdns.org
2. Create a subdomain (e.g., `myraspberry.duckdns.org`)
3. Note your API token from the DuckDNS page

## Telegram Bot Setup <a name="telegram-bot-setup"></a>
1. In Telegram, search for and start a chat with [@BotFather](https://telegram.me/BotFather)
2. Send `/newbot` and follow prompts to create your bot
3. Note the bot token (format: `123456789:ABCdefGHIjklMNopqRSTuvwxyz`)
4. Send `/setjoingroups <NAME OF YOUR GROUP>`
5. You'll be prompted to **Choose a bot to change group membership settings.** so you should send the bot name (in format `@<BOTNAME_bot>`)
6. The return message should be: **Current status is: ENABLED**
    ```log
    'Enable' - bot can be added to groups.
    'Disable' - block group invitations, the bot can't be added to groups.
    Current status is: ENABLED
    ```
8. Add your bot to a group chat
9. Get the group chat ID by:
    - Add [@RawDataBot](https://telegram.me/rawdatabot) to the group
    - It will display the chat ID (format: `-123456789`)

## Gmail App Key Configuration <a name="gmail-app-key-configuration"></a>
1. Create an App Password:
2. Go to your [Google Account](https://myaccount.google.com/) -> Security -> App passwords.
3. Generate an app password for "Mail".
4. Note the API secret (format: `ABCdefGHIjklMNopqRSTuvwxyz`)

# Installation Guide <a name="installation-guide"></a>
Follow these steps to set up the monitoring system.

## Script Configuration <a name="script-configuration"></a>

### duck.sh <a name="duck-sh"></a>
1. Edit the `duck.sh` with the following content and update <USER> and <TOKEN> with your DuckDNS credentials.
2. Save the changes.
4. Make the script executable:
    ```bash
    chmod +x duck.sh
    ```
5. Run the script:
    ```bash
    bash ~/internet-monitor/duck.sh
    ```
6. Check if the DNS has been updated:
    ```bash
    dig <USER>.duckdns.org
    ```
7. It should return your Raspberry Pi internet IP (to get your external IP run `curl https://ipv4.myip.wtf`)
    ```log 
    id 30053
    opcode QUERY
    rcode NOERROR
    flags QR RD RA
    ;QUESTION
    <USER>.duckdns.org. IN A
    ;ANSWER
    <USER>.duckdns.org. 60 IN A <YOUR IP>
    ;AUTHORITY
    ;ADDITIONAL
    ```
8. Create a cronjob to set up DuckDNS updates every 5 minutes, changing the `<PATH>` to the location where you cloned the Git Repo:
    ```bash  
    (crontab -l 2>/dev/null; echo "*/5 * * * * <PATH>/internet-monitor/duck.sh >> <PATH>/duckdns.log 2>&1") | crontab -
    ```
### monitor.py <a name="monitor-py"></a>

1. Edit the `monitor.py` with the following content (update credentials):
   - Update the Script: Replace `<TELEGRAM BOT_FATHER TOKEN>` and `<TELEGRAM GROUP ID>`.
   - Update the Script: Replace `<EMAIL>` and `<APP PASSWORD>` with your Gmail and app password.
      ```python
      # Email Configuration
      FROM_EMAIL = "<EMAIL>"
      PASSWORD = "<APP PASSWORD>"
      TO_EMAIL = "<EMAIL>"
      SMTP_SERVER = "smtp.gmail.com"
      SMTP_PORT = 587

      # Telegram Configuration
      TELEGRAM_TOKEN = '<TELEGRAM BOT_FATHER TOKEN>'
      GROUP_CHAT_ID = '<TELEGRAM GROUP ID>'

      # [Rest of the monitor.py content...]
      ```
3. Save the changes.
4. Make the script executable:
    ```bash
    chmod +x monitor.py
    ```

### server.py  <a name="server-py"></a>

1. Edit the `server.py` with the following content:
   - Update the Script: Replace `<PORT>` for the port number you want to be opened.
      ```python
      import socket

      # Server configuration
      HOST = '0.0.0.0'  # Listen on all available network interfaces
      PORT = <PORT>     # Port to listen on

      # [Rest of the server.py content...]
     ```
2. Save the changes.
3. Make the script executable:
   ```bash
    chmod +x server.py
    ```

## Systemd Service Installation  <a name="systemd-service-installation"></a>

1. Create service files:
- internet-monitor.service:
    ```ini
    [Unit]
    Description=RPI Internet Monitor
    After=network.target

    [Service]
    ExecStart=<PATH>/internet-monitor/venv/bin/python3 <PATH>/internet-monitor/monitor.py
    WorkingDirectory=<PATH>/internet-monitor
    Restart=always
    RestartSec=5s
    ```
- http-response.service
    ```ini
    [Unit]
    Description=HTTP Response Service
    After=network.target

    [Service]
    ExecStart=<PATH>/venv/bin/python3 <PATH>/internet-monitor/server.py
    WorkingDirectory=<PATH>/internet-monitor
    Restart=always
    RestartSec=5s
  
    [Install]
    WantedBy=multi-user.target
    ```
2. Copy the service files to `/etc/systemd/system/`
    ```bash  
    sudo cp *.service /etc/systemd/system/
    ```
3. Reload the systemctl daemon and start the services
    ```bash  
    sudo systemctl daemon-reload
    sudo systemctl enable internet-monitor.service http-response.service
    sudo systemctl start internet-monitor.service http-response.service
    ```

## Validation  <a name="validation"></a>

1. Check service status:
    ```bash  
    sudo systemctl status internet-monitor.service http-response.service
    ```
2. Test HTTP server:
    ```bash  
    curl http://localhost:5900
    # Should return "It's Alive!"
    ```
3. Check logs:
    ```bash  
    journalctl -u internet-monitor.service -f
    tail -f ~/internet_monitor.log
    ```
  
# Troubleshooting  <a name="troubleshooting"></a>

1. Email Notifications Not Working
    - Verify Gmail app password is correct
    - Check less secure apps access is enabled
    - Review logs: `journalctl -u internet-monitor.service`
2. Telegram Messages Not Arriving
    - Confirm bot token and chat ID are correct
    -  Ensure bot was added to the group
    -  Check bot privacy settings in [@BotFather](https://telegram.me/BotFather)
3. DuckDNS Not Updating
    -  Verify script has execute permissions
    -  Check cron is running: `systemctl status cron`
    -  Test script manually: `./duck.sh`
    - Check the duck.log
        ```bash
        cat duck.log
        ```
    - The the file will store the last attempt if was successful or not (OK or bad KO).
    - If it is KO check your Token and Domain are correct in the `duck.sh` script
4. Service Failing to Start
    -  Check paths in service files are correct
    -  Verify Python virtual environment is properly set up
    -  Examine logs: `journalctl -u service-name.service`
