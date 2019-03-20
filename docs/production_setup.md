Circus
======
[Docs](https://circus.readthedocs.io/en/latest/)  
[Installation Docs](https://circus.readthedocs.io/en/latest/tutorial/step-by-step/)  

systemd
=======
[Circus and systemd](https://circus.readthedocs.io/en/latest/for-ops/deployment/)  

Production Environment Setup
============================
1. Install Circus
    ```bash
    sudo apt install libzmq-dev libevent-dev python-dev python-virtualenv
    sudo -H pip3 install circus
    sudo -H pip3 install circus-web
    ```
2. Install SQSurvey
    ```bash
    sudo apt install python3-venv
    python3 -m venv path/to/project/
    source path/to/project/bin/activate
    cd path/to/project/
    git clone https://github.com/reputage/SQSurvey.git
    pip install -e SQSurvey/
    ```
3. Create a circus.ini File
    ```bash
    mkdir /etc/circus/
    vim /etc/circus/circus.ini
    ```
    Paste the contents below into the circus.ini file. Make sure 
    that if you are running multiple instances of Didery that you 
    change the port values for each.
    ```
    [watcher:didery]
    cmd = /path/to/project/bin/sqsurveyd -P 8000
    numprocesses = 1
    ```
    Save and quit.
4. Create a systemd service file
    ```bash
    vim /etc/systemd/system/circus.service
    ```
    Paste the contents below into the circus.service file.
    ```
    [Unit]
    Description=Circus process manager
    After=syslog.target network.target nss-lookup.target
    
    [Service]
    Type=simple
    ExecReload=/usr/local/bin/circusctl reload
    ExecStart=/usr/local/bin/circusd /etc/circus/circus.ini
    Restart=always
    RestartSec=5
    
    [Install]
    WantedBy=default.target
    ```
    Save and quit.
5. Enable the service to startup on boot
    ```bash
    systemctl enable circus
    ```
6. Start the service
    Restart the systemd Daemon
    ```bash
    systemctl --system daemon-reload
    ```
    Or You can restart Ubuntu
    ```bash
    sudo reboot
    ```

Installing Updates
==================
currently SQSurvey is not on pip so everything is done through git.

1. cd to project directory
    on 178.128.0.208 the survey server repo is at:
    ```bash
    cd reputation/projects/sqsurvey/SQSurvey/
    ```

2. Pull latest changes from master
    ```bash
    git pull
    ```

3. Restart the server
    ```bash
    sudo reboot
    ```

Cleaning Out The Database
=========================
Use these steps for cleaning up test servers or clearing out data so the next survey can be run.

1. Find where the db is located.
    Default paths:
    ```bash
    ls /var/sqsurvey/db
    ls ~/.consensys/sqsurvey/db
    ```
    It's also possible that a custom path was entered. There is no way to find out where this is except to ask whoever set it up.

2. Remove database
    ```bash
    rm -rf /path/to/db
    ```

3. Restart the server
    The server won't notice the db has been removed till you restart the survey.
    ```bash
    sudo reboot
    ```
