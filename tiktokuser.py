"""
TikTok Username Checker - 4 Letter Username Availability Checker by 0Kxs
"""

import requests
import time
import random
import string
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Back, Style
import threading
from datetime import datetime

# Initialize colorama for colors
init(autoreset=True)

# Clear console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class TikTokUsernameChecker:
    def __init__(self, delay=0.5, threads=5, output_file="available_usernames.txt"):
        self.base_url = "https://www.tiktok.com/@"
        self.delay = delay
        self.threads = threads
        self.output_file = output_file
        self.session = requests.Session()
        self.found_count = 0
        self.checked_count = 0
        self.lock = threading.Lock()
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.tiktok.com/',
            'Origin': 'https://www.tiktok.com'
        }
    
    def print_banner(self):
        """Display colored banner"""
        banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════╗
║{Fore.CYAN}                                                    ║
║{Fore.YELLOW}   ████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗{Fore.CYAN}   ║
║{Fore.YELLOW}   ╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝{Fore.CYAN}   ║
║{Fore.YELLOW}      ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝{Fore.CYAN}    ║
║{Fore.YELLOW}      ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗{Fore.CYAN}    ║
║{Fore.YELLOW}      ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗{Fore.CYAN}   ║
║{Fore.YELLOW}      ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝{Fore.CYAN}   ║
║{Fore.CYAN}                                                    ║
╚════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)
    
    def print_stats(self):
        """Display statistics"""
        stats = f"""
{Fore.CYAN}┌─────────────────────────────────────────────────────────────────┐
│{Fore.WHITE}                      STATISTICS{Fore.CYAN}                                 │
├─────────────────────────────────────────────────────────────────┤
│ {Fore.GREEN}✓ Available found:{Fore.WHITE} {self.found_count:>8}{Fore.CYAN}                                     │
│ {Fore.RED}✗ Checked (taken):{Fore.WHITE} {self.checked_count - self.found_count:>8}{Fore.CYAN}                                     │
│ {Fore.YELLOW}⟳ Total checked:{Fore.WHITE} {self.checked_count:>8}{Fore.CYAN}                                       │
├─────────────────────────────────────────────────────────────────┤
│ {Fore.CYAN}⚙ Threads: {self.threads}  |  Delay: {self.delay}s{Fore.CYAN}                                    │
└─────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}
"""
        return stats
    
    def print_available_card(self, username):
        """Display card for available usernames"""
        card = f"""
{Fore.GREEN}╔══════════════════════════════════════════════════════════════════╗
║{Fore.GREEN}  🎉 NEW USERNAME AVAILABLE! 🎉{Fore.GREEN}                                 ║
╠══════════════════════════════════════════════════════════════════╣
║  {Fore.WHITE}@{username}{' ' * (55 - len(username))}{Fore.GREEN}║
║  {Fore.CYAN}🔗 https://tiktok.com/@{username}{' ' * (37 - len(username))}{Fore.GREEN}║
╠══════════════════════════════════════════════════════════════════╣
║  {Fore.YELLOW}📁 Saved to: {self.output_file}{' ' * (33 - len(self.output_file))}{Fore.GREEN}║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(card)
    
    def generate_all_usernames(self):
        """Generate all 4-letter combinations"""
        letters = string.ascii_lowercase
        all_usernames = []
        
        print(f"{Fore.CYAN}[*] Generating all 4-letter combinations...{Style.RESET_ALL}")
        
        # Loading animation
        chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        i = 0
        
        for a in letters:
            for b in letters:
                for c in letters:
                    for d in letters:
                        all_usernames.append(f"{a}{b}{c}{d}")
                        if len(all_usernames) % 10000 == 0:
                            print(f"\r{Fore.YELLOW}{chars[i % len(chars)]} Generating: {len(all_usernames)}/456,976 combinations{Style.RESET_ALL}", end="")
                            i += 1
        
        print(f"\r{Fore.GREEN}[+] {len(all_usernames)} combinations generated (26^4 = 456,976){Style.RESET_ALL}")
        return all_usernames
    
    def shuffle_usernames(self, usernames):
        """Randomly shuffle the list"""
        print(f"{Fore.CYAN}[*] Randomizing username order...{Style.RESET_ALL}")
        random.shuffle(usernames)
        print(f"{Fore.GREEN}[+] Random order applied{Style.RESET_ALL}")
        return usernames
    
    def check_username(self, username):
        """Check if username is available"""
        try:
            response = self.session.get(
                f"{self.base_url}{username}",
                headers=self.headers,
                timeout=10,
                allow_redirects=False
            )
            
            with self.lock:
                self.checked_count += 1
            
            if response.status_code == 404:
                with self.lock:
                    self.found_count += 1
                return (username, True, None)
            elif response.status_code == 200:
                return (username, False, None)
            elif response.status_code == 429:
                return (username, None, "Rate limit")
            else:
                return (username, False, f"HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            return (username, None, "Timeout")
        except requests.exceptions.ConnectionError:
            return (username, None, "Connection")
        except Exception as e:
            return (username, None, str(e)[:20])
    
    def save_username(self, username):
        """Save available username to file"""
        try:
            with open(self.output_file, 'a') as f:
                f.write(f"{username}\n")
        except:
            pass
    
    def load_checked_usernames(self):
        """Load already found usernames"""
        try:
            with open(self.output_file, 'r') as f:
                return set(line.strip() for line in f)
        except:
            return set()
    
    def check_batch(self, usernames, resume=False, total_usernames=None):
        """Check multiple usernames with real-time interface"""
        
        # Load already found
        already_found = set()
        if resume:
            already_found = self.load_checked_usernames()
            if already_found:
                print(f"{Fore.YELLOW}[!] Resume: {len(already_found)} usernames already found{Style.RESET_ALL}")
                self.found_count = len(already_found)
        
        # Filter out already found
        to_check = [u for u in usernames if u not in already_found]
        total_to_check = len(to_check)
        
        # Determine stats frequency based on total
        if total_usernames:
            total = total_usernames
        else:
            total = total_to_check
        
        if total < 1000:
            stats_frequency = 100
        else:
            stats_frequency = 200
        
        print(f"{Fore.CYAN}[*] Starting verification with {self.threads} threads...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Stats will be shown every {stats_frequency} usernames{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*50}{Style.RESET_ALL}\n")
        
        start_time = time.time()
        found_usernames = []
        last_stats_count = 0
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.check_username, username): username 
                      for username in to_check}
            
            for future in as_completed(futures):
                username = futures[future]
                
                try:
                    username, is_available, error = future.result()
                    
                    if is_available:
                        self.print_available_card(username)
                        found_usernames.append(username)
                        self.save_username(username)
                    elif is_available is False:
                        print(f"{Fore.RED}[✗] @{username} Taken{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}[?] @{username} - {error}{Style.RESET_ALL}")
                    
                    # Show stats periodically
                    if self.checked_count - last_stats_count >= stats_frequency:
                        print(self.print_stats())
                        last_stats_count = self.checked_count
                    
                except Exception as e:
                    print(f"{Fore.RED}[!] @{username} Error: {e}{Style.RESET_ALL}")
                
                # Respect delay
                time.sleep(self.delay)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Display final summary
        self.print_final_summary(duration, total_to_check, found_usernames)
        
        return found_usernames
    
    def print_progress_bar(self, current, total):
        """Display progress bar"""
        percent = (current / total) * 100 if total > 0 else 0
        bar_length = 50
        filled = int(bar_length * current // total) if total > 0 else 0
        bar = '█' * filled + '░' * (bar_length - filled)
        
        if percent < 30:
            color = Fore.RED
        elif percent < 70:
            color = Fore.YELLOW
        else:
            color = Fore.GREEN
        
        print(f"\r{color}{bar}{Style.RESET_ALL} {percent:.1f}% ({current}/{total})", end="")
    
    def print_final_summary(self, duration, total_checked, found):
        """Display final summary"""
        clear_screen()
        self.print_banner()
        
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.WHITE}{' '*20}FINAL SUMMARY")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}[+] Usernames found: {len(found)}")
        print(f"{Fore.RED}[-] Usernames taken: {total_checked - len(found)}")
        print(f"{Fore.CYAN}[*] Total checked: {total_checked}")
        print(f"{Fore.YELLOW}[*] Total time: {duration:.2f} seconds ({duration/3600:.2f} hours)")
        print(f"{Fore.CYAN}[*] Output file: {self.output_file}\n")
        
        if found:
            print(f"{Fore.GREEN}{'─'*60}")
            print(f"{Fore.WHITE}AVAILABLE USERNAMES:")
            print(f"{Fore.GREEN}{'─'*60}{Style.RESET_ALL}")
            
            # Display in columns
            found_sorted = sorted(found)
            col_width = 15
            cols = 4
            for i in range(0, len(found_sorted), cols):
                row = found_sorted[i:i+cols]
                print(f"{Fore.GREEN}  " + "  ".join([f"@{u:<{col_width}}" for u in row]))
            
            print(f"\n{Fore.GREEN}{'─'*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}[+] Scan completed!{Style.RESET_ALL}\n")
    
    def run_random_check(self, count=100):
        """Check random usernames"""
        letters = string.ascii_lowercase
        usernames = set()
        
        print(f"{Fore.CYAN}[*] Generating {count} random usernames...{Style.RESET_ALL}")
        
        while len(usernames) < count:
            username = ''.join(random.choices(letters, k=4))
            usernames.add(username)
        
        usernames = list(usernames)
        print(f"{Fore.GREEN}[+] {len(usernames)} random usernames generated{Style.RESET_ALL}")
        
        self.check_batch(usernames, total_usernames=count)
    
    def run_full_random(self, delay, threads, resume=False):
        """Check ALL usernames in random order"""
        self.delay = delay
        self.threads = threads
        
        clear_screen()
        self.print_banner()
        
        print(f"\n{Fore.CYAN}{'─'*60}")
        print(f"{Fore.WHITE}Configuration:")
        print(f"{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Threads: {Fore.YELLOW}{threads}")
        print(f"{Fore.WHITE}Delay: {Fore.YELLOW}{delay}s")
        print(f"{Fore.WHITE}Output file: {Fore.YELLOW}{self.output_file}")
        print(f"{Fore.WHITE}Resume mode: {Fore.YELLOW}{'Yes' if resume else 'No'}")
        print(f"{Fore.CYAN}{'─'*60}{Style.RESET_ALL}\n")
        
        # Generate all usernames
        all_usernames = self.generate_all_usernames()
        
        # Shuffle
        all_usernames = self.shuffle_usernames(all_usernames)
        
        # Check
        self.check_batch(all_usernames, resume=resume, total_usernames=len(all_usernames))


def main():
    clear_screen()
    checker = TikTokUsernameChecker()
    checker.print_banner()
    
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Fore.WHITE}                      CHOOSE MODE{Fore.CYAN}                                 ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠══════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Fore.CYAN} 1{Fore.WHITE} │ Check ALL usernames (456,976) - Random order{Fore.CYAN}                 ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Fore.CYAN} 2{Fore.WHITE} │ Check random sample{Fore.CYAN}                                          ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Fore.CYAN} 3{Fore.WHITE} │ Resume interrupted scan{Fore.CYAN}                                      ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    choice = input(f"\n{Fore.YELLOW}> Your choice (1/2/3): {Style.RESET_ALL}").strip()
    
    if choice == "1":
        print(f"\n{Fore.RED}{'!'*60}")
        print(f"{Fore.RED}WARNING: Full scan of 456,976 usernames")
        print(f"Estimated time: several hours depending on configuration")
        print(f"{Fore.RED}{'!'*60}{Style.RESET_ALL}\n")
        
        try:
            delay = float(input(f"{Fore.YELLOW}> Delay between requests (seconds, default 0.5): {Style.RESET_ALL}") or "0.5")
            threads = int(input(f"{Fore.YELLOW}> Number of threads (default 5, max recommended 10): {Style.RESET_ALL}") or "5")
            
            # Limit threads to avoid blocking
            if threads > 10:
                print(f"{Fore.YELLOW}[!] Reducing to 10 threads maximum{Style.RESET_ALL}")
                threads = 10
            
            confirm = input(f"\n{Fore.RED}> Start full scan? (yes/no): {Style.RESET_ALL}").strip().lower()
            
            if confirm == "yes":
                checker.run_full_random(delay, threads)
            else:
                print(f"{Fore.YELLOW}Cancelled.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid value{Style.RESET_ALL}")
            
    elif choice == "2":
        try:
            count = int(input(f"{Fore.YELLOW}> Number of usernames to check: {Style.RESET_ALL}") or "1000")
            delay = float(input(f"{Fore.YELLOW}> Delay between requests (default 0.3): {Style.RESET_ALL}") or "0.3")
            threads = int(input(f"{Fore.YELLOW}> Number of threads (default 5, max 10): {Style.RESET_ALL}") or "5")
            
            if threads > 10:
                threads = 10
            
            checker = TikTokUsernameChecker(delay=delay, threads=threads)
            checker.run_random_check(count)
            
        except ValueError:
            print(f"{Fore.RED}Invalid value{Style.RESET_ALL}")
            
    elif choice == "3":
        try:
            delay = float(input(f"{Fore.YELLOW}> Delay between requests (default 0.5): {Style.RESET_ALL}") or "0.5")
            threads = int(input(f"{Fore.YELLOW}> Number of threads (default 5): {Style.RESET_ALL}") or "5")
            
            if threads > 10:
                threads = 10
            
            checker = TikTokUsernameChecker(delay=delay, threads=threads)
            checker.run_full_random(delay, threads, resume=True)
            
        except ValueError:
            print(f"{Fore.RED}Invalid value{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Interrupted by user{Style.RESET_ALL}")
        sys.exit(0)