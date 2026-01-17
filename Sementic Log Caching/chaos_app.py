import requests
import random
import time
from datetime import datetime
from colorama import Fore, Style, init

init() # Colors for terminal

SERVER_URL = "http://localhost:8000/v1/ingest"

# Mock messages that look different but mean the same thing semantically
LOG_TEMPLATES = [
    # Cluster 1: Database Connection Issues
    "Connection to DB failed for user {uid} at IP {ip}. Retrying...",
    "DB_ERR: Connection timed out. User_ID: {uid}. Source: {ip}",
    "Unable to reach database shard 4. Request from {ip} dropped.",
    
    # Cluster 2: Payment Gateway Failures
    "Payment declined for txn_{txn}. Gateway timeout.",
    "User {uid} tried to pay but gateway was unresponsive.",
    "Error 503: Payment Service Unavailable. Txn ID: {txn}",
    
    # Cluster 3: Successful Logins (Noise)
    "User {uid} logged in successfully from {ip}.",
    "Auth Success: {uid} entered the system.",
]

def generate_noise():
    """Generates random IPs, IDs, and timestamps."""
    ip = f"{random.randint(10,192)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
    uid = random.randint(1000, 9999)
    txn = f"TX{random.randint(10000,99999)}"
    return ip, uid, txn
    

def run_simulation(n_logs=50):
    print(f"{Fore.CYAN}--- STARTING CHAOS SIMULATION ({n_logs} logs) ---{Style.RESET_ALL}")
    
    for i in range(n_logs):
        # Selecting random template and fill it with noise
        template = random.choice(LOG_TEMPLATES)
        ip, uid, txn = generate_noise()
        message = template.format(uid=uid, ip=ip, txn=txn)
        
        # Creating payload
        payload = {
            "service_name": "ecommerce-frontend",
            "timestamp": datetime.now().isoformat(),
            "message": message
        }
        
        # Sending to SemLog
        try:
            resp = requests.post(SERVER_URL, json=payload)
            data = resp.json()
            
            if data['action'] == "COMPRESSED":
                print(f"{Fore.GREEN}[COMPRESSED]{Style.RESET_ALL} {message[:50]}...")
            else:
                print(f"{Fore.RED}[NEW PATTERN]{Style.RESET_ALL} {message[:50]}...")
                
        except Exception as e:
            print(f"Server error: {e}")
            
        time.sleep(0.05)
        

if __name__ == "__main__":
    run_simulation(100) # Sending 100 logs