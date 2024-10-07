import requests
import time
from datetime import datetime

# Configuration
url = 'http://rail-service-solent.unicard-uk.com:8080/RailApiWebTest/'  # Replace with the website you want to monitor
check_interval = 300  # Time between checks in seconds

# Variables to track uptime and downtime
start_time = None
last_status = None
total_uptime = 0

def check_website():
    try:
        # Make a GET request to the website
        response = requests.get(url, timeout=10)
        # Return True if the website is up (status code 200)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        # Handle connection errors or timeouts
        print(f"Error connecting to {url}: {e}")
        return False

def log_status(is_up):
    global start_time, last_status, total_uptime

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if is_up:
        if last_status is False or start_time is None:  # Site was down, now up
            print(f"[{current_time}] Website is UP.")
            start_time = datetime.now()
        else:
            # Update uptime duration
            uptime_duration = (datetime.now() - start_time).total_seconds()
            total_uptime = uptime_duration
            print(f"[{current_time}] Website has been up for {uptime_duration:.2f} seconds.")
    else:
        if last_status is True:  # Site was up, now down
            if start_time:
                uptime_duration = (datetime.now() - start_time).total_seconds()
                print(f"[{current_time}] Website went DOWN. Uptime before failure: {uptime_duration:.2f} seconds.")
            start_time = None
        else:
            print(f"[{current_time}] Website is still DOWN.")

    last_status = is_up

def main():
    print(f"Monitoring {url} every {check_interval} seconds.")
    while True:
        is_up = check_website()
        log_status(is_up)
        time.sleep(check_interval)

if __name__ == "__main__":
    main()
