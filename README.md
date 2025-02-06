# **CryptoTrendPredictor**
Predicting temporal tendencies of cryptocurrencies using ML

## **Proyect structure**
``` markdown
/CRYPTOTRENDPREDICTOR/
|-- /data/
    |-- /raw/
        |-- crypto_data.db  <-- Here, SQL db is saved 
|-- /scr/
    │-- database.py <-- Script to inilize, create, and save bd
    │-- fetch_data.py <-- Script to get data from API and save them in the bd
    │-- config.py <-- Script to configure bd parameters
```


## **Automating ```main.py``` Execution**
To ensure that ```main.py``` runs automatically at regular intervals without manual intervention, follow the appropriate setup based on your operating system.

### **Windows: Task Scheduler**
Windows provides the **Task Scheduler**, which allows you to automate script execution.

Steps to schedule ```main.py``` in Windows:
**CMD**
1. **Open Task Scheduler:**
    Press ```Win + R```, type ```taskschd.msc```, and press ```Enter```.

2. **Create a new task:**
    Click **"Create Basic Task"** on the right panel.

3. **Set task name and description:**
    - Name it something like ```Crypto Data Fetcher```.
    - Add a short description: *Runs main.py to fetch cryptocurrency data*.

4. **Choose the frequency:**
    Select  ```Daily ``` or  ```Hourly ```, depending on how often you want the script to run.

5. **Set the start time:**
    Choose the time and interval for execution.

6. **Select the action → Start a program:**
    - Under "Program/script", enter:

        ```sh
        C:\Windows\System32\cmd.exe
        ```
    - Under **"Add arguments"**, enter the path to ```main.py```:
        ```sh
        /c "C:\path\to\your\project\venv\Scripts\activate && python C:\path\to\your\project\main.py"
        ```
    - Under **"Start in"**, enter the folder where ```main.py``` is located.
    ```sh
    C:\path\to\your\project
    ```

7. **Finish and save:**
    Confirm and test the scheduled task.

The Task Scheduler will now run ```main.py``` at the specified intervals.

**WSL**
1. **Open WSL Terminal:**

2. **Edit the crontab file:**
    ```sh
    crontab -e
    ```

3. **Add the following cron job to run main.py every hour:**
    ```Hourly```
    ```sh
    0 * * * * source /mnt/c/Users/YOUR_USER/path/to/venv/Scripts/activate && python /mnt/c/Users/YOUR_USER/path/to/main.py
    ```

    ```Daily``` <!-- Runs at 03:00 AM -->
    ```sh
    0 3 * * * source /mnt/c/Users/YOUR_USER/path/to/venv/Scripts/activate && python /mnt/c/Users/YOUR_USER/path/to/main.py
    ```
    (Replace ```YOUR_USER``` with your username and update the script path accordingly.)

4. **Save and exit:**
    In nano, press ```Ctrl + X```, then ```Y```, and ```Enter```.

5. **Check scheduled jobs:**
    ```sh
    crontab -l
    ```

Possibily, WSL does not execute ```cron``` automatically, but you can configure:
1. **Open WSL configuration file:**
    ```sh
    sudo nano /etc/wsl.conf
    ```

2. **Add at the end of the file:**
    ```markdown
    [boot]
    command="service cron start"
    ```

3. **Save and restart the terminal:**
    ```sh
    wsl --shutdown
    ```

- To check if ```cron``` is running:
    ```sh
    sudo service cron status
    ```

- To iniziate ```cron```:
    ```sh
    sudo service cron start
    ```

- To check if ```cron jobs``` are been executed:
    ```sh
    grep cron /var/log/syslog
    ```



### **Mac: Using ```launchd``` (LaunchAgents)**
On macOS, you can automate tasks using ```launchd``` by creating a **LaunchAgent**.

Steps to automate main.py in macOS:
1. **Open Terminal:**
    Press ```Cmd + Space```, type ```Terminal```, and press ```Enter```.

2. **Create a new LaunchAgent configuration file:**
    ```sh
    nano ~/Library/LaunchAgents/com.crypto.fetch.plist
    ```

3. **Add the following configuration:**
    ```Hourly ```
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>com.crypto.fetch</string>
            <key>ProgramArguments</key>
            <array>
                <string>/usr/bin/python3</string>
                <string>/Users/YOUR_USER/path/to/project/main.py</string>
            </array>
            <key>StartInterval</key>
            <integer>3600</integer> <!-- Runs every 3600 seconds (1 hour) -->
            <key>RunAtLoad</key>
            <true/>
        </dict>
    </plist>
    ```

    ```Daily ```
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>com.crypto.fetch</string>
            <key>ProgramArguments</key>
            <array>
                <string>/usr/bin/python3</string>
                <string>/Users/YOUR_USER/path/to/project/main.py</string>
            </array>
            <key>StartCalendarInterval</key>
            <dict>
                <key>Hour</key>
                <integer>3</integer> <!-- Runs at 03:00 AM -->
                <key>Minute</key>
                <integer>0</integer>
            </dict>
            <key>RunAtLoad</key>
            <true/>
        </dict>
    </plist>
    ```

    (Replace ```YOUR_USER``` with your actual username and update the ```main.py``` path accordingly.)

4. **Load the task into ```launchd```:**
    ```sh
    launchctl load ~/Library/LaunchAgents/com.crypto.fetch.plist
    ```
    ```launchd``` will now automatically run ```main.py``` every hour.

    To verify if it is running:
    ```sh
    launchctl list | grep com.crypto.fetch
    ```



### **Linux: Using ```cron``` Jobs:**
In Linux, we can use ```cron```, a built-in task scheduler.

Steps to automate ```main.py``` in Linux:
1. **Open Terminal:**
    Press ```Ctrl + Alt + T```.

2. **Edit the crontab file:**
    ```sh
    crontab -e
    ```

3. **Add the following cron job to run main.py every hour:**
    ```Hourly```
    ```sh
    0 * * * * /bin/bash -c 'source /home/YOUR_USER/path/to/project/venv/bin/activate && python /home/YOUR_USER/path/to/project/main.py'
    ```

    ```Daily``` <!-- Runs at 03:00 AM -->
    ```sh
    0 3 * * * /bin/bash -c 'source /home/YOUR_USER/path/to/project/venv/bin/activate && python /home/YOUR_USER/path/to/project/main.py'
    ```
    (Replace ```YOUR_USER``` with your username and update the script path accordingly.)

4. **Save and exit:**
    In nano, press ```Ctrl + X```, then ```Y```, and ```Enter```.

5. **Check scheduled jobs:**
    ```sh
    crontab -l
    ```

Now, ```cron``` will automatically run main.py every hour.




