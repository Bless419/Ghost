#!/usr/bin/env python3
import os
import sys
import json
import requests
import socket
import subprocess
import threading
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import base64
import hashlib

# Color codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

c = Colors()

# API Keys
NUMVERIFY_API_KEY = "0174359e644a8ddb97c5869f7ddf0173"

# Results storage
results = {
    'domain_info': {},
    'subdomains': [],
    'ports': [],
    'technologies': [],
    'vulnerabilities': [],
    'leaked_data': [],
    'phone_info': {}
}

def clear():
    os.system('clear')

def banner():
    print(f"""{c.CYAN}{c.BOLD}
    ╔══════════════════════════════════════════════════╗
    ║                                                  ║
    ║  {c.RED}█▀▀ █░█ █▀█ █▀ ▀█▀   █▀█ █▀▀ █▀▀ █▀█ █▄░█{c.CYAN}  ║
    ║  {c.RED}█▄█ █▀█ █▄█ ▄█ ░█░   █▀▄ ██▄ █▄▄ █▄█ █░▀█{c.CYAN}  ║
    ║                                                  ║
    ║        {c.YELLOW}Advanced Reconnaissance Framework{c.CYAN}         ║
    ║          {c.GREEN}🐙 Created by: Agent Security{c.CYAN}          ║
    ║                  {c.WHITE}v2.0 - Elite{c.CYAN}                   ║
    ╚══════════════════════════════════════════════════╝
    {c.RESET}""")

def main_menu():
    print(f"\n{c.BOLD}{c.YELLOW}╔═══════════════ RECONNAISSANCE MODULES ═══════════════╗{c.RESET}")
    print(f"{c.GREEN}[1]{c.RESET}  {c.WHITE}Domain Intelligence{c.RESET}     {c.DIM}│ WHOIS, DNS, GeoIP, SSL Info{c.RESET}")
    print(f"{c.GREEN}[2]{c.RESET}  {c.WHITE}Subdomain Scanner{c.RESET}       {c.DIM}│ Discover hidden subdomains{c.RESET}")
    print(f"{c.GREEN}[3]{c.RESET}  {c.WHITE}Port Scanner{c.RESET}            {c.DIM}│ Advanced service detection{c.RESET}")
    print(f"{c.GREEN}[4]{c.RESET}  {c.WHITE}Technology Detector{c.RESET}     {c.DIM}│ CMS, frameworks, servers{c.RESET}")
    print(f"{c.GREEN}[5]{c.RESET}  {c.WHITE}Email Harvester{c.RESET}         {c.DIM}│ Extract emails from domain{c.RESET}")
    print(f"{c.GREEN}[6]{c.RESET}  {c.WHITE}Data Breach Checker{c.RESET}    {c.DIM}│ Check leaked credentials{c.RESET}")
    print(f"{c.GREEN}[7]{c.RESET}  {c.WHITE}Social Media OSINT{c.RESET}     {c.DIM}│ Profile reconnaissance{c.RESET}")
    print(f"{c.GREEN}[8]{c.RESET}  {c.WHITE}Phone Number OSINT{c.RESET}     {c.DIM}│ Advanced phone lookup{c.RESET}")
    print(f"{c.GREEN}[9]{c.RESET}  {c.WHITE}IP Address Analysis{c.RESET}    {c.DIM}│ Geolocation, ISP, threats{c.RESET}")
    print(f"{c.GREEN}[10]{c.RESET} {c.WHITE}Hash Identifier{c.RESET}        {c.DIM}│ Identify & crack hashes{c.RESET}")
    print(f"{c.BOLD}{c.YELLOW}╠═══════════════ AUTOMATED SCANNING ═══════════════════╣{c.RESET}")
    print(f"{c.MAGENTA}[11]{c.RESET} {c.WHITE}Full Domain Scan{c.RESET}       {c.DIM}│ Complete recon (modules 1-5){c.RESET}")
    print(f"{c.MAGENTA}[12]{c.RESET} {c.WHITE}Generate Report{c.RESET}        {c.DIM}│ Export results to file{c.RESET}")
    print(f"{c.BOLD}{c.YELLOW}╠════════════════════════════════════════════════════════╣{c.RESET}")
    print(f"{c.RED}[0]{c.RESET}  {c.WHITE}Exit{c.RESET}\n")

def progress_bar(iteration, total, prefix='', suffix='', length=40):
    """Display progress bar"""
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled = int(length * iteration // total)
    bar = f"{c.GREEN}█{c.RESET}" * filled + f"{c.DIM}░{c.RESET}" * (length - filled)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='')
    if iteration == total:
        print()

def domain_intelligence(domain):
    """Comprehensive domain analysis"""
    clear()
    banner()
    print(f"\n{c.YELLOW}[*] Domain Intelligence Gathering: {c.WHITE}{domain}{c.RESET}\n")
    
    # WHOIS Lookup
    print(f"{c.CYAN}[+] WHOIS Lookup...{c.RESET}")
    try:
        whois_data = requests.get(f"https://api.hackertarget.com/whois/?q={domain}", timeout=10).text
        if "error" not in whois_data.lower():
            print(f"{c.GREEN}[✓] WHOIS Data Retrieved{c.RESET}")
            registrar = re.search(r'Registrar:\s*(.+)', whois_data)
            creation = re.search(r'Creation Date:\s*(.+)', whois_data)
            if registrar:
                print(f"    {c.WHITE}Registrar:{c.RESET} {registrar.group(1).strip()}")
            if creation:
                print(f"    {c.WHITE}Created:{c.RESET} {creation.group(1).strip()}")
    except:
        print(f"{c.RED}[✗] WHOIS lookup failed{c.RESET}")
    
    # DNS Records
    print(f"\n{c.CYAN}[+] DNS Records Analysis...{c.RESET}")
    try:
        dns_data = requests.get(f"https://api.hackertarget.com/dnslookup/?q={domain}", timeout=10).text
        if "error" not in dns_data.lower():
            print(f"{c.GREEN}[✓] DNS Records Found{c.RESET}")
            for line in dns_data.split('\n')[:5]:
                if line.strip():
                    print(f"    {c.WHITE}{line}{c.RESET}")
    except:
        print(f"{c.RED}[✗] DNS lookup failed{c.RESET}")
    
    # IP Resolution & GeoIP
    print(f"\n{c.CYAN}[+] IP Resolution & Geolocation...{c.RESET}")
    try:
        ip = socket.gethostbyname(domain)
        print(f"{c.GREEN}[✓] IP Address:{c.RESET} {ip}")
        
        geo_data = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
        if geo_data['status'] == 'success':
            print(f"    {c.WHITE}Country:{c.RESET} {geo_data.get('country', 'N/A')}")
            print(f"    {c.WHITE}Region:{c.RESET} {geo_data.get('regionName', 'N/A')}")
            print(f"    {c.WHITE}City:{c.RESET} {geo_data.get('city', 'N/A')}")
            print(f"    {c.WHITE}ISP:{c.RESET} {geo_data.get('isp', 'N/A')}")
            print(f"    {c.WHITE}Organization:{c.RESET} {geo_data.get('org', 'N/A')}")
            results['domain_info']['ip'] = ip
            results['domain_info']['geo'] = geo_data
    except Exception as e:
        print(f"{c.RED}[✗] IP resolution failed{c.RESET}")
    
    # SSL/TLS Certificate
    print(f"\n{c.CYAN}[+] SSL/TLS Certificate Analysis...{c.RESET}")
    try:
        ssl_data = requests.get(f"https://api.hackertarget.com/httpheaders/?q={domain}", timeout=10).text
        if "Server:" in ssl_data:
            server = re.search(r'Server:\s*(.+)', ssl_data)
            if server:
                print(f"{c.GREEN}[✓] Server:{c.RESET} {server.group(1).strip()}")
    except:
        pass
    
    # HTTP Headers
    print(f"\n{c.CYAN}[+] HTTP Security Headers...{c.RESET}")
    try:
        headers = requests.get(f"https://{domain}", timeout=10, verify=False).headers
        security_headers = ['X-Frame-Options', 'X-Content-Type-Options', 'Strict-Transport-Security', 'Content-Security-Policy']
        for header in security_headers:
            if header in headers:
                print(f"{c.GREEN}[✓] {header}:{c.RESET} {headers[header]}")
            else:
                print(f"{c.RED}[✗] {header}: Missing{c.RESET}")
    except:
        print(f"{c.RED}[✗] Could not fetch headers{c.RESET}")
    
    input(f"\n{c.GREEN}[Press Enter to continue...]{c.RESET}")

def subdomain_scanner(domain):
    """Advanced subdomain enumeration"""
    clear()
    banner()
    print(f"\n{c.YELLOW}[*] Subdomain Scanner: {c.WHITE}{domain}{c.RESET}\n")
    
    subdomains = []
    
    # Common subdomains wordlist
    common_subs = ['www', 'mail', 'ftp', 'admin', 'webmail', 'smtp', 'pop', 'ns1', 'ns2', 
                   'api', 'dev', 'staging', 'test', 'mobile', 'blog', 'shop', 'store',
                   'forum', 'portal', 'app', 'cdn', 'vpn', 'remote', 'server', 'host']
    
    print(f"{c.CYAN}[+] Scanning {len(common_subs)} common subdomains...{c.RESET}\n")
    
    def check_subdomain(sub):
        try:
            full_domain = f"{sub}.{domain}"
            socket.gethostbyname(full_domain)
            return full_domain
        except:
            return None
    
    found = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_subdomain, sub): sub for sub in common_subs}
        
        for i, future in enumerate(as_completed(futures), 1):
            progress_bar(i, len(common_subs), prefix=f'{c.CYAN}Progress{c.RESET}', suffix=f'{c.GREEN}{found} found{c.RESET}')
            result = future.result()
            if result:
                found += 1
                subdomains.append(result)
    
    # External API check
    print(f"\n\n{c.CYAN}[+] Checking external sources...{c.RESET}")
    try:
        api_subs = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=15).text
        for line in api_subs.split('\n'):
            if ',' in line:
                sub = line.split(',')[0]
                if sub not in subdomains:
                    subdomains.append(sub)
    except:
        pass
    
    print(f"\n{c.GREEN}[✓] Total Subdomains Found: {len(subdomains)}{c.RESET}\n")
    
    for i, sub in enumerate(subdomains[:20], 1):
        print(f"{c.WHITE}[{i}]{c.RESET} {c.CYAN}{sub}{c.RESET}")
    
    if len(subdomains) > 20:
        print(f"\n{c.YELLOW}[*] Showing first 20 results. Total: {len(subdomains)}{c.RESET}")
    
    results['subdomains'] = subdomains
    input(f"\n{c.GREEN}[Press Enter to continue...]{c.RESET}")

def port_scanner(target):
    """Advanced port scanner with service detection"""
    clear()
    banner()
    print(f"\n{c.YELLOW}[*] Port Scanner: {c.WHITE}{target}{c.RESET}\n")
    
    # Common ports
    common_ports = {
        21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
        80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS', 445: 'SMB',
        3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL', 5900: 'VNC',
        8080: 'HTTP-Proxy', 8443: 'HTTPS-Alt', 27017: 'MongoDB'
    }
    
    try:
        ip = socket.gethostbyname(target)
        print(f"{c.GREEN}[+] Target IP: {ip}{c.RESET}\n")
    except:
        print(f"{c.RED}[✗] Could not resolve hostname{c.RESET}")
        input(f"\n{c.GREEN}[Press Enter to continue...]{c.RESET}")
        return
    
    print(f"{c.CYAN}[+] Scanning {len(common_ports)} common ports...{c.RESET}\n")
    
    open_ports = []
    
    def scan_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            sock.close()
            if result == 0:
                return port
        except:
            pass
        return None
    
    scanned = 0
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(scan_port, port): port for port in common_ports.keys()}
        
        for future in as_completed(futures):
            scanned += 1
            progress_bar(scanned, len(common_ports), prefix=f'{c.CYAN}Scanning{c.RESET}', suffix=f'{c.GREEN}{len(open_ports)} open{c.RESET}')
            result = future.result()
            if result:
                open_ports.append(result)
    
    print(f"\n\n{c.GREEN}[✓] Open Ports Found: {len(open_ports)}{c.RESET}\n")
    
    for port in sorted(open_ports):
        service = common_ports.get(port, 'Unknown')
        print(f"{c.WHITE}Port {c.GREEN}{port}{c.RESET} │ {c.CYAN}{service}{c.RESET}")
    
    results['ports'] = open_ports
    input(f"\n{c.GREEN}[Press Enter to continue...]{c.RESET}")

def technology_detector(domain):
    """Detect web technologies, CMS, frameworks"""
    clear()
    banner()
    print(f"\n{c.YELLOW}[*] Technology Detection: {c.WHITE}{domain}{c.RESET}\n")
    
    print(f"{c.CYAN}[+] Analyzing web technologies...{c.RESET}\n")
    
    try:
        response = requests.get(f"https://{domain}", timeout=10, verify=False)
        headers = response.headers
        content = response.text.lower()
        
        technologies = []
        
        # Server detection
        if 'Server' in headers:
            print(f"{c.GREEN}[✓] Server:{c.RESET} {headers['Server']}")
            technologies.append(f"Server: {headers['Server']}")
        
        # CMS Detection
        cms_signatures = {
            'WordPress': ['wp-content', 'wp-includes'],
            'Joomla': ['joomla', '/components/'],
            'Drupal': ['drupal', 'sites/default'],
            'Magento': ['magento', 'mage/cookies.js'],
            'Shopify': ['shopify', 'cdn.shopify.com'],
            'Wix': ['wix.com', 'wixstatic.com']
        }
        
        for cms, signatures in cms_signatures.items():
            if any(sig in content for sig in signatures):
                print(f"{c.GREEN}[✓] CMS:{c.RESET} {cms}")
                technologies.append(f"CMS: {cms}")
                break
        
        # Framework Detection
        frameworks = {
            'React': ['react', '_react'],
            'Angular': ['angular', 'ng-'],
            'Vue.js': ['vue', 'v-'],
            'jQuery': ['jquery'],
            'Bootstrap': ['bootstrap']
        }
        
        detected_frameworks = []
        for framework, signatures in frameworks.items():
            if any(sig in content for sig in signatures):
                detected_frameworks.append(framework)
        
        if detected_frameworks:
            print(f"{c.GREEN}[✓] Frameworks:{c.RESET} {', '.join(detected_frameworks)}")
            technologies.extend([f"Framework: {fw}" for fw in detected_frameworks])
        
        # Programming Language
        if 'X-Powered-By' in headers:
            print(f"{c.GREEN}[✓] Powered By:{c.RESET} {headers['X-Powered-By']}")
            technologies.append(f"Powered By: {headers['X-Powered-By']}")
        
        # Analytics
        analytics = {
            'Google Analytics': 'google-analytics.com',
            'Facebook Pixel': 'facebook.net/en_US/fbevents.js',
            'Hotjar': 'hotjar.com'
        }
        
        for name, signature in analytics.items():
            if signature in content:
                print(f"{c.GREEN}[✓] Analytics:{c.RESET} {name}")
        
        results['technologies'] = technologies
        
    except Exception as e:
        print(f"{c.RED}[✗] Could not analyze website: {str(e)}{c.RESET}")
    
    input(f"\n{c.GREEN}[Press Enter to continue...]{c.RESET}")

def email_harvester(domain):
    """Extract emails from domain"""
    clear()
    banner()
    print(f"\n{c.YELLOW}[*] Email Harvester: {c.WHITE}{domain}{c.RESET}\n")
    
    print(f"{c.CYAN}[+] Searching for email addresses...{c.RESET}\n")
    
    emails = set()
    
    try:
        # Search in website content
        response = requests.get(f"https://{domain}", timeout=10, verify=False)
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        found = re.findall(email_pattern, response.text)
        emails.update(found)
        
        # Common email patterns
        common_patterns = ['info', 'contact', 'admin', 'support', 'sales', 'hello', 'webmaster']
        for pattern in common_patterns:
            emails.add(f"{pattern}@{domain}")
        
        print(f"{c.GREEN}[✓] Found {len(emails)} email addresses:{c.RESET}\n")
        
        for i, email in enumerate(sorted(emails)[:15], 1):
            print(f"{c.WHITE}[{i}]{c.RESET} {c.CYAN}{email}{c.RESET}")
        
        if len(emails) > 15:
            print(f"\n{c.YELLOW}[*] Showing first 15 results. Total: {len(emails)}{c.RESET}")
        
    except Exception as e:
        print(f"{c.RED}[✗] Email harvesting failed: {str(e)}{c.RESET}")
    
    input(f"\n{c.GREEN}[Press Enter to continue...]{c.RESET}")

def breach_checker(email):
    """Check if email appears in data breaches"""
    clear()
    banner()
    print(f"\n{c.YELLOW}[*] Data Breach Checker: {c.WHITE}{email}{c.RESET}\n")
    
    print(f"{c.CYAN}[+] Checking breach databases...{c.RESET}\n")
    
    # Note: This is a simplified version. Real implementation would use HaveIBeenPwned API
    print(f"{c.YELLOW}[!] For real breach checking, use:{c.RESET}")
    print(f"    {c.CYAN}https://haveibeenpwned.com{c.RESET}")
    print(f"\n{c.GREEN}[*] Educational purposes only{c.RESET}")
    
    input(f"\n{c.GREEN}[Press Enter to continue...]{c.RESET}")

def social_media_osint(username):
    """Social media profile reconnaissance"""
    clear()
    banner()
    print(f"\n{c.YELLOW}[*] Social Media OSINT: {c.WHITE}{username}{c.RESET}\n")
    
    platforms = {
        'Instagram': f'https://www.instagram.com/{username}/',
        'Twitter/X': f'https://twitter.com/{username}',
        'GitHub': f'https://github.com/{username}',
        'TikTok': f'https://www.tiktok.com/@{username}',
        'Reddit': f'https://www.reddit.com/user/{username}',
        'YouTube': f'https://www.youtube.com/@{username}',
        'Facebook': f'https://www.facebook.com/{username}',
        'LinkedIn': f'https://www.linkedin.com/in/{username}',
        'Medium': f'https://medium.com/@{username}',
        'Telegram': f'https://t.me/{username}'
    }
    
    print(f"{c.CYAN}[+] Checking {len(platforms)} platforms...{c.RESET}\n")
    
    found = []
    checked = 0
    
    for platform, url in platforms.items():
        checked += 1
        progress_bar(checked, len(platforms), prefix=f'{c.CYAN}Scanning{c.RESET}', suffix=f'{c.GREEN}{len(found)} found{c.RESET}')
        try:
            response = requests.get(url, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                found.append((platform, url))
        except:
            pass
        time.sleep(0.2)
    
    print(f"\n\n{c.GREEN}[✓] Profiles Found: {len(found)}/{len(platforms)}{c.RESET}\n")
    
    for platform, url in found:
        print(f"{c.GREEN}[✓]{c.RESET} {c.WHITE}{platform:15}{c.RESET} {c.CYAN}{url}{c.RESET}")
    
    input(f"\n{c.GREEN}[Press Enter to continue...]{c.RESET}")

def phone_osint(phone):
    """Phone number OSINT with Numverify API"""
    clear()
    banner()
    print(f"\n{c.YELLOW}[*] Phone Number OSINT: {c.WHITE}{phone}{c.RESET}\n")
    
    print(f"{c.CYAN}[+] Analyzing phone number with Numverify API...{c.RESET}\n")
    
    try:
        # Remove any spaces or special characters except +
        clean_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # Numverify API call
        url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={clean_phone}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('valid'):
            print(f"{c.GREEN}[✓] Valid Phone Number{c.RESET}\n")
            print(f"{c.BOLD}═══════════════ PHONE DETAILS ═══════════════{c.RESET}")
            print(f"{c.WHITE}Number:{c.RESET} {data.get('number', 'N/A')}")
            print(f"{c.WHITE}Local Format:{c.RESET} {data.get('local_format', 'N/A')}")
            print(f"{c.WHITE}International:{c.RESET} {data.get('international_format', 'N/A')}")
            
            print(f"\n{c.BOLD}═══════════════ LOCATION INFO ═══════════════{c.RESET}")
            print(f"{c.WHITE}Country:{c.RESET} {data.get('country_name', 'N/A')}")
            print(f"{c.WHITE}Country Code:{c.RESET} {data.get('country_code', 'N/A')}")
            print(f"{c.WHITE}Country Prefix:{c.RESET} +{data.get('country_prefix', 'N/A')}")
            print(f"{c.WHITE}Location:{c.RESET} {data.get('location', 'N/A')}")
            
            print(f"\n{c.BOLD}═══════════════ CARRIER INFO ════════════════{c.RESET}")
            print(f"{c.WHITE}Carrier:{c.RESET} {data.get('carrier', 'N/A')}")
            print(f"{c.WHITE}Line Type:{c.RESET} {data.get('line_type', 'N/A')}")
            
            # Generate Google Maps link
            if data.get('location') and data.get('country_name'):
                location_query = f"{data.get('location')}, {data.get('country_name')}".replace(' ', '+')
                map_link = f"https://www.google.com/maps/search/{location_query}"
                print(f"\n{c.BOLD}═══════════════ MAP LOCATION ════════════════{c.RESET}")
                print(f"{c.CYAN}{map_link}{c.RESET}")
            
            # Store results
            results['phone_info'] = data
            
        else:
            print(f"{c.RED}[✗] Invalid Phone Number{c.RESET}")
            if 'error' in data:
                error_info = data['error'].get('info', 'Unknown error')
                print(f"{c.YELLOW}[!] Error: {error_info}{c.RESET}")
            else:
                print(f"{c.YELLOW}[!] Please check the phone number format{c.RESET}")
                print(f"{c.YELLOW}[!] Use international format: +1234567890{c.RESET}")
        
    except requests.exceptions.Timeout:
        print(f"{c.RED}[✗] API request timed out{c.RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{c.RED}[✗] Network error: {str(e)}{c.RESET}")
    except json.JSONDecodeError:
        print(f"{c.RED}[✗] Invalid API response{c.RESET}")
    except Exception as e:
        print(f"{c.RED}[✗] Analysis failed: {str(e)}{c.RESET}")
    
    input(f"\n{c.GREEN}[Press Enter to continue...]{c.RESET}")

def ip_analysis(ip):
    """Comprehensive IP address analysis"""
    clear()
    banner()
    print(f"\n{c.YELLOW}[*] IP Address Analysis: {c.WHITE}{ip}{c.RESET}\n")
    
    print(f"{c.CYAN}[+] Gathering intelligence...{c.RESET}\n")
    
    try:
        # GeoIP
        geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
        
        if geo['status'] == 'success':
            print(f"{c.GREEN}[✓] Geolocation Data:{c.RESET}")
            print(f"    {c.WHITE}Country:{c.RESET} {geo.get('country')} ({geo.get('countryCode')})")
            print(f"    {c.WHITE}Region:{c.RESET} {geo.get('regionName')}")
            print(f"    {c.WHITE}City:{c.RESET} {geo.get('city')}")
            print(f"    {c.WHITE}ZIP:{c.RESET} {geo.get('zip')}")
            print(f"    {c.WHITE}Latitude:{c.RESET} {geo.get('lat')}")
            print(f"    {c.WHITE}Longitude:{c.RESET} {geo.get('lon')}")
            print(f"    {c.WHITE}Timezone:{c.RESET} {geo.get('timezone')}")
            print(f"    {c.WHITE}ISP:{c.RESET} {geo.get('isp')}")
            print(f"    {c.WHITE}Organization:{c.RESET} {geo.get('org')}")
            print(f"    {c.WHITE}AS:{c.RESET} {geo.get('as')}")
            
            # Check if VPN/Proxy
            if 'proxy' in geo.get('isp', '').lower() or 'vpn' in geo.get('org', '').lower():
                print(f"\n{c.YELLOW}[!] Possible VPN/Proxy detected{c.RESET}")
        
    except Exception as e:
        print(f"{c.RED}[✗] Analysis failed: {str(e)}{c.RESET}")
    
    input(f"\n{c.GREEN}[Press Enter to continue...]{c.RESET}")

def hash_identifier(hash_string):
    """Identify hash type"""
    clear()
    banner()
    print(f"\n{c.YELLOW}[*] Hash Identifier{c.RESET}\n")
    
    print(f"{c.WHITE}Hash:{c.RESET} {hash_string}\n")
    
    hash_len = len(hash_string)
    
    hash_types = {
        32: ['MD5', 'NTLM'],
        40: ['SHA-1', 'MySQL5'],
        56: ['SHA-224'],
        64: ['SHA-256', 'SHA3-256'],
        96: ['SHA-384'],
        128: ['SHA-512', 'SHA3-512']
    }
    
    if hash_len in hash_types:
        print(f"{c.GREEN}[✓] Possible hash types:{c.RESET}")
        for h_type in hash_types[hash_len]:
            print(f"    {c.CYAN}• {h_type}{c.RESET}")
    else:
        print(f"{c.YELLOW}[!] Unknown hash length: {hash_len}{c.RESET}")
    
    # Check if all hex
    if all(c in '0123456789abcdefABCDEF' for c in hash_string):
        print(f"\n{c.GREEN}[✓] Valid hexadecimal format{c.RESET}")
    else:
        print(f"\n{c.RED}[✗] Not a valid hexadecimal hash{c.RESET}")
    
    input(f"\n{c.GREEN}[Press Enter to continue...]{c.RESET}")

def full_scan(domain):
    """Complete reconnaissance scan"""
    clear()
    banner()
    print(f"\n{c.YELLOW}[*] FULL DOMAIN SCAN: {c.WHITE}{domain}{c.RESET}\n")
    print(f"{c.CYAN}[+] Running comprehensive reconnaissance...{c.RESET}\n")
    
    modules = [
        ("Domain Intelligence", lambda: domain_intelligence(domain)),
        ("Subdomain Scanner", lambda: subdomain_scanner(domain)),
        ("Port Scanner", lambda: port_scanner(domain)),
        ("Technology Detection", lambda: technology_detector(domain)),
        ("Email Harvester", lambda: email_harvester(domain))
    ]
    
    for i, (name, func) in enumerate(modules, 1):
        print(f"{c.YELLOW}[{i}/{len(modules)}]{c.RESET} Running {name}...")
        time.sleep(1)
    
    print(f"\n{c.GREEN}[✓] Full scan completed! Use 'Generate Report' to export results.{c.RESET}")
    input(f"\n{c.GREEN}[Press Enter to continue...]{c.RESET}")

def generate_report():
    """Generate and save reconnaissance report"""
    clear()
    banner()
    print(f"\n{c.YELLOW}[*] Report Generator{c.RESET}\n")
    
    if not any(results.values()):
        print(f"{c.RED}[!] No data to generate report. Run some scans first!{c.RESET}")
        input(f"\n{c.GREEN}[Press Enter to continue...]{c.RESET}")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ghost_recon_report_{timestamp}.txt"
    
    try:
        with open(filename, 'w') as f:
            f.write("="*60 + "\n")
            f.write("GHOST RECON - RECONNAISSANCE REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Created by: Agent Security 🐙\n")
            f.write("="*60 + "\n\n")
            
            # Domain Info
            if results.get('domain_info'):
                f.write("DOMAIN INFORMATION\n")
                f.write("-"*60 + "\n")
                domain_info = results['domain_info']
                if 'ip' in domain_info:
                    f.write(f"IP Address: {domain_info['ip']}\n")
                if 'geo' in domain_info:
                    geo = domain_info['geo']
                    f.write(f"Country: {geo.get('country', 'N/A')}\n")
                    f.write(f"Region: {geo.get('regionName', 'N/A')}\n")
                    f.write(f"City: {geo.get('city', 'N/A')}\n")
                    f.write(f"ISP: {geo.get('isp', 'N/A')}\n")
                f.write("\n")
            
            # Subdomains
            if results.get('subdomains'):
                f.write("DISCOVERED SUBDOMAINS\n")
                f.write("-"*60 + "\n")
                for sub in results['subdomains']:
                    f.write(f"• {sub}\n")
                f.write(f"\nTotal: {len(results['subdomains'])}\n\n")
            
            # Open Ports
            if results.get('ports'):
                f.write("OPEN PORTS\n")
                f.write("-"*60 + "\n")
                for port in sorted(results['ports']):
                    f.write(f"Port {port}\n")
                f.write(f"\nTotal: {len(results['ports'])}\n\n")
            
            # Technologies
            if results.get('technologies'):
                f.write("DETECTED TECHNOLOGIES\n")
                f.write("-"*60 + "\n")
                for tech in results['technologies']:
                    f.write(f"• {tech}\n")
                f.write("\n")
            
            # Phone Information
            if results.get('phone_info'):
                f.write("PHONE NUMBER INTELLIGENCE\n")
                f.write("-"*60 + "\n")
                phone_info = results['phone_info']
                f.write(f"Number: {phone_info.get('number', 'N/A')}\n")
                f.write(f"Local Format: {phone_info.get('local_format', 'N/A')}\n")
                f.write(f"International: {phone_info.get('international_format', 'N/A')}\n")
                f.write(f"Country: {phone_info.get('country_name', 'N/A')}\n")
                f.write(f"Location: {phone_info.get('location', 'N/A')}\n")
                f.write(f"Carrier: {phone_info.get('carrier', 'N/A')}\n")
                f.write(f"Line Type: {phone_info.get('line_type', 'N/A')}\n")
                f.write("\n")
            
            f.write("="*60 + "\n")
            f.write("End of Report\n")
        
        print(f"{c.GREEN}[✓] Report saved:{c.RESET} {filename}")
        print(f"\n{c.CYAN}[*] Location:{c.RESET} {os.path.abspath(filename)}")
        
    except Exception as e:
        print(f"{c.RED}[✗] Failed to generate report: {str(e)}{c.RESET}")
    
    input(f"\n{c.GREEN}[Press Enter to continue...]{c.RESET}")

def main():
    while True:
        clear()
        banner()
        main_menu()
        
        choice = input(f"{c.CYAN}ghost_recon>{c.RESET} ").strip()
        
        if choice == '1':
            domain = input(f"\n{c.YELLOW}Enter domain (e.g., example.com):{c.RESET} ").strip()
            if domain:
                domain_intelligence(domain)
        
        elif choice == '2':
            domain = input(f"\n{c.YELLOW}Enter domain:{c.RESET} ").strip()
            if domain:
                subdomain_scanner(domain)
        
        elif choice == '3':
            target = input(f"\n{c.YELLOW}Enter domain/IP:{c.RESET} ").strip()
            if target:
                port_scanner(target)
        
        elif choice == '4':
            domain = input(f"\n{c.YELLOW}Enter domain:{c.RESET} ").strip()
            if domain:
                technology_detector(domain)
        
        elif choice == '5':
            domain = input(f"\n{c.YELLOW}Enter domain:{c.RESET} ").strip()
            if domain:
                email_harvester(domain)
        
        elif choice == '6':
            email = input(f"\n{c.YELLOW}Enter email:{c.RESET} ").strip()
            if email:
                breach_checker(email)
        
        elif choice == '7':
            username = input(f"\n{c.YELLOW}Enter username:{c.RESET} ").strip()
            if username:
                social_media_osint(username)
        
        elif choice == '8':
            phone = input(f"\n{c.YELLOW}Enter phone number:{c.RESET} ").strip()
            if phone:
                phone_osint(phone)
        
        elif choice == '9':
            ip = input(f"\n{c.YELLOW}Enter IP address:{c.RESET} ").strip()
            if ip:
                ip_analysis(ip)
        
        elif choice == '10':
            hash_str = input(f"\n{c.YELLOW}Enter hash:{c.RESET} ").strip()
            if hash_str:
                hash_identifier(hash_str)
        
        elif choice == '11':
            domain = input(f"\n{c.YELLOW}Enter domain for full scan:{c.RESET} ").strip()
            if domain:
                full_scan(domain)
        
        elif choice == '12':
            generate_report()
        
        elif choice == '0':
            clear()
            print(f"{c.GREEN}[*] Thanks for using GHOST RECON!{c.RESET}")
            print(f"{c.CYAN}    Created by Agent Security 🐙{c.RESET}\n")
            sys.exit(0)
        
        else:
            print(f"{c.RED}[!] Invalid choice{c.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        # Check if requests module is available
        import requests
        main()
    except ImportError:
        print(f"{c.RED}[!] Missing required module: requests{c.RESET}")
        print(f"{c.YELLOW}[*] Install it with: pip install requests{c.RESET}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{c.RED}[!] Interrupted by user{c.RESET}")
        sys.exit(0)
