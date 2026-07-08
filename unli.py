import re
import requests
import os
import sys
import time

# ======================== COLOR CODES ========================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    BLACK = '\033[30m'
    WHITE = '\033[97m'
    BG_BLACK = '\033[40m'
    BG_BLUE = '\033[44m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'

# ======================== BANNER ========================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                                   ║
║   {Colors.RED}██████╗ ███████╗██╗  ██╗ ██████╗ ██╗  ██╗ █████╗ {Colors.CYAN}   ║
║   {Colors.RED}██╔══██╗██╔════╝██║  ██║██╔═══██╗██║ ██╔╝██╔══██╗{Colors.CYAN}   ║
║   {Colors.RED}██████╔╝███████╗███████║██║   ██║█████╔╝ ███████║{Colors.CYAN}   ║
║   {Colors.RED}██╔══██╗╚════██║██╔══██║██║   ██║██╔═██╗ ██╔══██║{Colors.CYAN}   ║
║   {Colors.RED}██║  ██║███████║██║  ██║╚██████╔╝██║  ██╗██║  ██║{Colors.CYAN}   ║
║   {Colors.RED}╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝{Colors.CYAN}   ║
║                                                                   ║
║   {Colors.YELLOW}       RUIJIE UNLIMITED AUTHENTICATOR v3.0             {Colors.CYAN}   ║
║   {Colors.GREEN}     === Network Freedom Tool for Ruijie Portal ===      {Colors.CYAN}   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.BOLD}{Colors.WHITE}  ╔══════════════════════════════════════════════════════════════╗
  ║ {Colors.CYAN}Developer: {Colors.GREEN}@Nain663                      {Colors.WHITE}║
  ║ {Colors.CYAN}Version:  {Colors.GREEN}3.0                         {Colors.WHITE}║
  ╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
""")

def line():
    terminal_width = os.get_terminal_size()[0]
    print(f"{Colors.BOLD}{Colors.WHITE}{'-' * terminal_width}{Colors.RESET}")

# ======================== CORE FUNCTIONS ========================
def get_session_id(session_url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'referer': session_url,
        'sec-ch-ua': '"Chromium";v="148", "Microsoft Edge";v="148", "Not/A)Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0',
        'cookie':'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219e0ddbd9f2152-0df941f2efc6b08-4c657b58-1327104-19e0ddbd9f3a60%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fgemini.google.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTllMGRkYmQ5ZjIxNTItMGRmOTQxZjJlZmM2YjA4LTRjNjU3YjU4LTEzMjcxMDQtMTllMGRkYmQ5ZjNhNjAifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219e0ddbd9f2152-0df941f2efc6b08-4c657b58-1327104-19e0ddbd9f3a60%22%7D'
    }
    
    try:
        response = requests.get(session_url, headers=headers)
        session_id = re.search(r"[?&]sessionId=([a-zA-Z0-9]+)", response.url).group(1)
        return session_id
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}❌ Connection error occurred. Please check your internet connection and try again.{Colors.RESET}")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f"{Colors.RED}❌ The request timed out. Please check your internet connection and try again.{Colors.RESET}")
        sys.exit(1)
    except AttributeError:
        print(f"{Colors.RED}❌ Failed to extract session ID from the URL. Please check the session URL and try again.{Colors.RESET}")
        line()
        print(f"{Colors.YELLOW}📝 Response: {response.text}{Colors.RESET}")
        sys.exit(1)

def login_voucher(session_id, voucher):
    data = {
        "accessCode": voucher,
        "sessionId": session_id,
        "apiVersion": 2
    }
    post_url = "https://portal-as.ruijienetworks.com/api/auth/voucher/?lang=en_US"
    headers = {
        "authority": "portal-as.ruijienetworks.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://portal-as.ruijienetworks.com",
        "referer": f"https://portal-as.ruijienetworks.com/download/static/maccauth/src/index.html?RES=./../expand/res/mrlev58jlgslg49ervu&IS_EG=0&sessionId={session_id}",
        "sec-ch-ua": '"Chromium";v="139", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": f'Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    try:
        with requests.post(post_url, json=data, headers=headers) as response:
            response_text = response.text
            if "Authentication failed" in response_text or "expired" in response_text or "Expired" in response_text:
                print(f"{Colors.YELLOW}⚠️  Voucher code {voucher} incorrect or expired{Colors.RESET}")
                sys.exit(1)
            else:
                print(f"{Colors.GREEN}✅ Voucher authenticated successfully{Colors.RESET}")
                return re.search('token=(.*?)&', response_text).group(1)
    except AttributeError:
        print(f"{Colors.RED}❌ Failed to retrieve token. Please check the voucher code and session ID.{Colors.RESET}")
        line()
        print(f"{Colors.YELLOW}📝 Response: {response_text}{Colors.RESET}")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}❌ Connection error occurred. Please check your internet connection and try again.{Colors.RESET}")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f"{Colors.RED}❌ The request timed out. Please check your internet connection and try again.{Colors.RESET}")
        sys.exit(1)

def OneClick(token):
    headers = {
        'authority': 'portal-as.ruijienetworks.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,my;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://portal-as.ruijienetworks.com',
        'referer': 'https://portal-as.ruijienetworks.com/download/static/maccauth/src/index.html?RES=./../expand/res/mrlev58jlgslg49ervu&IS_EG=0&sessionId=7182e9a18cd04a1eb47868d3f7b69b44',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    params = {
        'lang': 'en_US',
    }
    json_data = {
        'phoneNumber':'',
        'sessionId': token,
    }
    try:
        response = requests.post(
            'https://portal-as.ruijienetworks.com/api/auth/direct/',
            params=params,
            headers=headers,
            json=json_data,
        )
        response_text = response.text
        token_match = re.search('token=(.*?)&', response_text)
        if token_match:
            print(f"{Colors.GREEN}✅ OneClick authentication successful{Colors.RESET}")
            return token_match.group(1)
        else:
            print(f"{Colors.YELLOW}⚠️  OneClick authentication failed, trying again...{Colors.RESET}")
            return None
    except AttributeError:
        return None
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}❌ Connection error occurred. Please check your internet connection and try again.{Colors.RESET}")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f"{Colors.RED}❌ The request timed out. Please check your internet connection and try again.{Colors.RESET}")
        sys.exit(1)

def auth(voucher=None, ip=None, token=None, session_url=None, final=False):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,my;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    params = {
        'token': token,
        'phoneNumber': '',
    }
    try:
        response = requests.get(f'http://{ip}:2060/wifidog/auth', params=params, headers=headers).url
        if "success" in response or 'www.baidu.com' in response or "www.ruijie.com/en-global" in response:
            print(f"{Colors.GREEN}✅ Successfully Authenticated{Colors.RESET}")
            line()
            if not final:
                Auth_as_Unlimited(voucher, ip, session_url)
            else:
                print(f"{Colors.GREEN}🎉 Successfully changed to unlimited mode!{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ Failed to Authenticate: {response}{Colors.RESET}")
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}❌ Connection error. Make sure you're connected to the network.{Colors.RESET}")
        sys.exit(1)

def Auth_as_Unlimited(voucher, ip, session_url):
    for i in range(3):
        print(f"\n{Colors.CYAN}🔄 Attempt {i+1}/3{Colors.RESET}")
        session_id = get_session_id(session_url)
        print(f"{Colors.GREEN}📌 Final Inactive Session Id: {session_id}{Colors.RESET}")
        line()
        token = login_voucher(session_id, voucher)
        if token:
            print(f"{Colors.WHITE}📌 Final Active Session Id: {Colors.GREEN}{token}{Colors.RESET}")
            line()
            token = OneClick(token)
            if token:
                auth(ip=ip, token=token, final=True)
                print(f"{Colors.GREEN}🎉 Successful to change into unlimited{Colors.RESET}")
                return True
            else:
                print(f"{Colors.RED}❌ Attempt {i+1} failed{Colors.RESET}")
                line()
        else:
            print(f"{Colors.RED}❌ Failed to Authenticate. Please check the voucher code and session ID.{Colors.RESET}")
    print(f"{Colors.RED}❌ All 3 attempts failed. Please try again later.{Colors.RESET}")
    return False

def get_default_gateway():
    try:
        if os.name == 'nt':
            result = os.popen('ipconfig | findstr "Default Gateway"').read()
            lines = result.strip().split('\n')
            if lines:
                for line in lines:
                    if line.strip():
                        ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                        if ip_match:
                            return ip_match.group(1)
        else:
            result = os.popen('ip route | grep default').read()
            ip_match = re.search(r'default via (\d+\.\d+\.\d+\.\d+)', result)
            if ip_match:
                return ip_match.group(1)
    except:
        pass
    return None

def get_session_url_from_router(ip):
    try:
        response = requests.get(f'http://{ip}/', timeout=5)
        if 'sessionId' in response.text:
            session_id = re.search(r'sessionId=([a-zA-Z0-9]+)', response.text)
            if session_id:
                return f"http://{ip}/?sessionId={session_id.group(1)}"
    except:
        pass
    return None

# ======================== MENU FUNCTIONS ========================
def menu():
    print(f"""
{Colors.BOLD}{Colors.YELLOW}╔══════════════════════════════════════════════════════════════╗
║                      {Colors.GREEN}MAIN MENU{Colors.YELLOW}                       ║
╠══════════════════════════════════════════════════════════════╣
║  {Colors.CYAN}[1]{Colors.WHITE} 🚀  Unlimited Mode                          {Colors.YELLOW}║
║  {Colors.CYAN}[2]{Colors.WHITE} 📊  Check Voucher Status                    {Colors.YELLOW}║
║  {Colors.CYAN}[3]{Colors.WHITE} ℹ️   About / Help                          {Colors.YELLOW}║
║  {Colors.CYAN}[4]{Colors.WHITE} 🚪  Exit                                   {Colors.YELLOW}║
╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
""")

def unlimited_mode():
    clear_screen()
    banner()
    print(f"\n{Colors.BOLD}{Colors.GREEN}🚀 UNLIMITED MODE{Colors.RESET}\n")
    
    ip = get_default_gateway()
    if ip:
        print(f"{Colors.GREEN}✅ Detected Gateway IP: {ip}{Colors.RESET}")
    else:
        ip = input(f"{Colors.YELLOW}⚠️  Could not detect gateway. Enter your WiFi Gateway IP: {Colors.BLUE}")
    
    line()
    
    session_url = get_session_url_from_router(ip)
    if session_url:
        print(f"{Colors.GREEN}✅ Detected Session URL: {session_url}{Colors.RESET}")
        use_detected = input(f"{Colors.CYAN}Use this session URL? (y/n, default y): {Colors.WHITE}").strip().lower()
        if use_detected == 'n':
            session_url = input(f"{Colors.YELLOW}Enter Session URL manually: {Colors.BLUE}")
    else:
        print(f"{Colors.YELLOW}⚠️  Could not auto-detect session URL.{Colors.RESET}")
        session_url = input(f"{Colors.YELLOW}Enter Session URL from browser: {Colors.BLUE}")
    
    line()
    
    voucher = input(f"{Colors.WHITE}Enter Voucher Code: {Colors.GREEN}")
    line()
    
    print(f"{Colors.CYAN}🔄 Starting unlimited mode authentication...{Colors.RESET}")
    line()
    
    session_id = get_session_id(session_url)
    print(f"{Colors.GREEN}📌 Session ID: {session_id}{Colors.RESET}")
    line()
    
    token = login_voucher(session_id, voucher)
    if token:
        print(f"{Colors.GREEN}✅ Token obtained: {token}{Colors.RESET}")
        line()
        Auth_as_Unlimited(voucher, ip, session_url)
    else:
        print(f"{Colors.RED}❌ Authentication failed.{Colors.RESET}")
    
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

def check_voucher_status():
    clear_screen()
    banner()
    print(f"\n{Colors.BOLD}{Colors.GREEN}📊 CHECK VOUCHER STATUS{Colors.RESET}\n")
    
    ip = get_default_gateway()
    if not ip:
        ip = input(f"{Colors.YELLOW}Enter Gateway IP: {Colors.BLUE}")
        line()
    
    session_url = get_session_url_from_router(ip)
    if not session_url:
        session_url = input(f"{Colors.YELLOW}Enter Session URL: {Colors.BLUE}")
        line()
    
    voucher = input(f"{Colors.WHITE}Enter Voucher Code to check: {Colors.GREEN}")
    line()
    
    print(f"{Colors.CYAN}🔄 Checking voucher status...{Colors.RESET}")
    line()
    
    session_id = get_session_id(session_url)
    print(f"{Colors.GREEN}📌 Session ID: {session_id}{Colors.RESET}")
    line()
    
    token = login_voucher(session_id, voucher)
    
    if token:
        print(f"{Colors.GREEN}✅ Voucher is valid and active!{Colors.RESET}")
        print(f"{Colors.WHITE}📌 Token: {Colors.GREEN}{token}{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ Voucher is invalid or expired.{Colors.RESET}")
    
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

def about():
    clear_screen()
    banner()
    print(f"""
{Colors.BOLD}{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                         {Colors.GREEN}ABOUT{Colors.CYAN}                            ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  {Colors.WHITE}📌 {Colors.GREEN}Tool       {Colors.WHITE}: Ruijie Unlimited Authenticator     ║
║  {Colors.WHITE}📌 {Colors.GREEN}Developer  {Colors.WHITE}: RSHOKA                        ║
║  {Colors.WHITE}📌 {Colors.GREEN}Purpose    {Colors.WHITE}: Bypass Ruijie Portal Limit     ║
║  {Colors.WHITE}📌 {Colors.GREEN}Version    {Colors.WHITE}: 3.0                            ║
║                                                               ║
║  {Colors.YELLOW}⚠️  {Colors.RED}DISCLAIMER{Colors.YELLOW}: Use at your own risk!             ║
║     This tool is for educational purposes only.              ║
║     Please respect network policies and local laws.          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
""")
    input(f"\n{Colors.CYAN}Press Enter to return to menu...{Colors.RESET}")

# ======================== MAIN ========================
def main():
    while True:
        clear_screen()
        banner()
        menu()
        
        choice = input(f"\n{Colors.BOLD}{Colors.CYAN}👉  Select option [1-4]: {Colors.WHITE}")
        
        if choice == '1':
            unlimited_mode()
        elif choice == '2':
            check_voucher_status()
        elif choice == '3':
            about()
        elif choice == '4':
            print(f"\n{Colors.GREEN}👋 Goodbye! Thanks for using RSHOKA Tool{Colors.RESET}\n")
            sys.exit(0)
        else:
            print(f"{Colors.RED}❌ Invalid option. Please try again.{Colors.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Interrupted by user. Exiting...{Colors.RESET}")
        sys.exit(0)
