import os
import random
import json
import requests
import threading
import time
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ANSI Formatting
BANNER = os.getenv('BANNER') or "IP-SCANNER"
BEFORE = f"\033[93m[{BANNER}\033[0m] "
AFTER = "\033[0m"
BEFORE_GREEN = "\033[92m["
AFTER_GREEN = "\033[0m"
WHITE = "\033[1;37m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

INPUT = "[?]"
IP_VALID = "[+] IP Reachable!"
IP_INVALID = "[!] IP Unreachable!"
white = WHITE
green = GREEN
red = RED
reset = RESET

# CONFIG VALUES (embedded directly)
THREADS_NUMBER = 10
COLOR_WEBHOOK = 65280
USERNAME_WEBHOOK = "IP Scanner Bot"
AVATAR_WEBHOOK = "https://i.imgur.com/CzGEcPL.png"

# Helper Functions
def current_time_hour():
    return time.strftime("%H:%M:%S")

def ErrorModule(error):
    print(f"{BEFORE}{RED}Error!{RESET} {error}")

def ErrorNumber():
    print(f"{BEFORE}{RED}Error!{RESET} The number of threads should be an integer.")
    input("Press Enter to exit...")
    exit()

def CheckWebhook(webhook_url):
    try:
        requests.post(webhook_url)
    except Exception as e:
        ErrorModule(e)
        print(f"{BEFORE + current_time_hour() + AFTER}{RED} Invalid or Missing Webhook URL{RESET}")
        webhook_url = input(f"{BEFORE + current_time_hour() + AFTER}> Webhook URL -> {RESET}")
        CheckWebhook(webhook_url)

def send_ip_notification(ip):
    payload = {
        'embeds': [ {
            'title': 'Reachable IP Found!',
            'description': f"**IP:** `{ip}`",
            'color': COLOR_WEBHOOK,
            'footer': {
                "text": USERNAME_WEBHOOK,
                "icon_url": AVATAR_WEBHOOK,
            }
        }],
        'username': USERNAME_WEBHOOK,
        'avatar_url': AVATAR_WEBHOOK
    }

    headers = {'Content-Type': 'application/json'}

    try:
        requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    except Exception as e:
        ErrorModule(e)

# Replaces pinging with a simulated random result
def simulate_ip_check(ip):
    return random.choice([True, False])

def scan_ip():
    while True:
        ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
        if simulate_ip_check(ip):
            print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {IP_VALID} {white}{ip}{reset}")
            if webhook_url:
                send_ip_notification(ip)
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {IP_INVALID} {white}{ip}{reset}")
        time.sleep(0.25)

def request():
    threads = []
    try:
        for _ in range(THREADS_NUMBER):
            t = threading.Thread(target=scan_ip)
            t.start()
            threads.append(t)
    except:
        ErrorNumber()

    for t in threads:
        t.join()

# Main
if __name__ == '__main__':
    try:
        webhook_choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook? (y/n) -> {reset}")
        if webhook_choice.lower() in ['y', 'yes']:
            webhook_url = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook URL -> {reset}")
            CheckWebhook(webhook_url)
        else:
            webhook_url = None

        request()  # Run once instead of infinite loop

        # After scanning ends
        input("\nPress Enter to return to menu...")

    except Exception as e:
        ErrorModule(e)
        input("\nSomething went wrong. Press Enter to exit...")
