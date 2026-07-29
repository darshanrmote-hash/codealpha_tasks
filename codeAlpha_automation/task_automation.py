import os
import shutil
import re
import requests
from datetime import datetime

def clear_screen():
    """Clears the terminal screen for a cleaner interface."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Prints a styled header for the sections."""
    print("=" * 60)
    print(f"{title.center(60)}")
    print("=" * 60)

def press_enter_to_continue():
    """Helper to pause execution and wait for user acknowledgment."""
    print("\n" + "-" * 60)
    input("  Press Enter to return to the main menu...")

# =====================================================================
# FEATURE 1: File Organizer (.jpg/.jpeg files)
# =====================================================================
def organize_jpg_files():
    clear_screen()
    print_header("FILE ORGANIZER: MOVE JPG/JPEG FILES")
    
    print("  This tool moves all .jpg and .jpeg files from a source")
    print("  directory to a destination directory of your choice.\n")
    
    # Get and validate source directory
    source_dir = input("  Enter path of the source folder (or press Enter for current folder): ").strip()
    if not source_dir:
        source_dir = "."
        
    if not os.path.exists(source_dir):
        print(f"\n  [!] Error: Source directory '{source_dir}' does not exist.")
        press_enter_to_continue()
        return
        
    if not os.path.isdir(source_dir):
        print(f"\n  [!] Error: '{source_dir}' is not a directory.")
        press_enter_to_continue()
        return
        
    # Get destination directory
    dest_dir = input("  Enter path of the destination folder: ").strip()
    if not dest_dir:
        print("\n  [!] Error: Destination directory cannot be empty.")
        press_enter_to_continue()
        return
        
    # Standardize paths
    source_path = os.path.abspath(source_dir)
    dest_path = os.path.abspath(dest_dir)
    
    if source_path == dest_path:
        print("\n  [!] Source and destination directories are the same. No files to move.")
        press_enter_to_continue()
        return
        
    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_path):
        try:
            os.makedirs(dest_path)
            print(f"  [+] Created destination folder: {dest_path}")
        except Exception as e:
            print(f"\n  [!] Error creating destination directory: {e}")
            press_enter_to_continue()
            return
            
    # Move files
    moved_count = 0
    errors_count = 0
    
    try:
        files = os.listdir(source_path)
    except Exception as e:
        print(f"\n  [!] Error reading source directory: {e}")
        press_enter_to_continue()
        return
        
    print("\n  Scanning and moving files...")
    print("  " + "-" * 56)
    
    for filename in files:
        # Check for .jpg or .jpeg extension (case-insensitive)
        if filename.lower().endswith(('.jpg', '.jpeg')):
            src_file_path = os.path.join(source_path, filename)
            
            # Skip directories that happen to end with .jpg/.jpeg (rare but possible)
            if os.path.isdir(src_file_path):
                continue
                
            dest_file_path = os.path.join(dest_path, filename)
            
            # Handle filename collisions in destination folder
            if os.path.exists(dest_file_path):
                name, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(dest_file_path):
                    new_filename = f"{name}_{counter}{ext}"
                    dest_file_path = os.path.join(dest_path, new_filename)
                    counter += 1
                final_name = os.path.basename(dest_file_path)
            else:
                final_name = filename
                
            try:
                shutil.move(src_file_path, dest_file_path)
                print(f"  [✓] Moved: {filename} -> {final_name}")
                moved_count += 1
            except Exception as e:
                print(f"  [✗] Failed to move {filename}: {e}")
                errors_count += 1
                
    print("  " + "-" * 56)
    print(f"  Successfully moved {moved_count} file(s).")
    if errors_count > 0:
        print(f"  Failed to move {errors_count} file(s).")
        
    press_enter_to_continue()

# =====================================================================
# FEATURE 2: Email Extractor
# =====================================================================
def extract_email_addresses():
    clear_screen()
    print_header("EMAIL EXTRACTOR")
    
    print("  This tool extracts all unique email addresses from a text")
    print("  file and saves them to an output file of your choice.\n")
    
    # Get and validate source file
    source_file = input("  Enter path to the source text file: ").strip()
    if not source_file:
        print("\n  [!] Error: Source file path cannot be empty.")
        press_enter_to_continue()
        return
        
    if not os.path.exists(source_file):
        print(f"\n  [!] Error: Source file '{source_file}' does not exist.")
        press_enter_to_continue()
        return
        
    if not os.path.isfile(source_file):
        print(f"\n  [!] Error: '{source_file}' is not a valid file.")
        press_enter_to_continue()
        return
        
    # Get destination file
    dest_file = input("  Enter path to the output text file (e.g., emails.txt): ").strip()
    if not dest_file:
        print("\n  [!] Error: Output file path cannot be empty.")
        press_enter_to_continue()
        return
        
    # Regex pattern for matching email addresses
    # Complies with standard email formats
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    
    try:
        with open(source_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"\n  [!] Error reading source file: {e}")
        press_enter_to_continue()
        return
        
    # Find all emails and make them unique (casing preserved, but deduplicated case-insensitively)
    found_emails = email_pattern.findall(content)
    
    if not found_emails:
        print("\n  [i] No email addresses were found in the source file.")
        press_enter_to_continue()
        return
        
    # Deduplicate while maintaining case variations if desired, or standardize to lower
    unique_emails = sorted(list(set(email.lower() for email in found_emails)))
    
    try:
        # Ensure parent folder for dest_file exists
        dest_dir = os.path.dirname(os.path.abspath(dest_file))
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            
        with open(dest_file, 'w', encoding='utf-8') as f:
            for email in unique_emails:
                f.write(email + '\n')
                
        print("\n  Extraction Complete!")
        print("  " + "-" * 56)
        print(f"  Total emails found: {len(found_emails)}")
        print(f"  Unique emails saved: {len(unique_emails)}")
        print(f"  Results saved to: {os.path.abspath(dest_file)}")
        print("  " + "-" * 56)
    except Exception as e:
        print(f"\n  [!] Error writing to output file: {e}")
        
    press_enter_to_continue()

# =====================================================================
# FEATURE 3: Web Title Scraper
# =====================================================================
def scrape_webpage_title():
    clear_screen()
    print_header("WEBPAGE TITLE SCRAPER")
    
    print("  This tool scrapes the HTML title of any webpage using a URL")
    print("  and appends it to a local log file ('scraped_titles.txt').\n")
    
    url = input("  Enter website URL (e.g., https://python.org): ").strip()
    if not url:
        print("\n  [!] Error: URL cannot be empty.")
        press_enter_to_continue()
        return
        
    # Simple URL prefix check & fix
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'https://' + url
        print(f"  [i] Auto-prefixed protocol. Using URL: {url}")
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print("\n  Connecting to webpage and fetching title...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"\n  [!] Error fetching webpage: {e}")
        press_enter_to_continue()
        return
        
    html_content = response.text
    
    # Extract title using regular expression
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
    
    if not title_match:
        print("\n  [!] Error: Could not locate a <title> tag in the HTML source.")
        press_enter_to_continue()
        return
        
    # Clean the title (remove leading/trailing whitespace, resolve simple HTML entities if any)
    title = title_match.group(1).strip()
    # Simple HTML entity decoding for common characters
    title = title.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
    
    print("\n  Webpage Scraped Successfully!")
    print("  " + "-" * 56)
    print(f"  URL:   {url}")
    print(f"  Title: {title}")
    print("  " + "-" * 56)
    
    # Save the scraped result
    log_filename = "scraped_titles.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open(log_filename, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] URL: {url} | TITLE: {title}\n")
        print(f"  [✓] Logged entry in '{os.path.abspath(log_filename)}'")
    except Exception as e:
        print(f"  [!] Failed to save log entry: {e}")
        
    press_enter_to_continue()

# =====================================================================
# MAIN LOOP
# =====================================================================
def main():
    while True:
        clear_screen()
        print("=" * 60)
        print("                TASK AUTOMATION PYTHON TOOL             ")
        print("=" * 60)
        print("  1. File Organizer (Move .jpg/.jpeg files)")
        print("  2. Email Address Extractor (from .txt file)")
        print("  3. Webpage Title Scraper (save title of website)")
        print("  4. Exit")
        print("=" * 60)
        
        choice = input("  Select an option (1-4): ").strip()
        
        if choice == '1':
            organize_jpg_files()
        elif choice == '2':
            extract_email_addresses()
        elif choice == '3':
            scrape_webpage_title()
        elif choice == '4':
            clear_screen()
            print("\n  Thank you for using the Task Automation Tool! Goodbye.\n")
            break
        else:
            print("\n  [!] Invalid choice. Please enter a number from 1 to 4.")
            import time
            time.sleep(1.5)

if __name__ == "__main__":
    main()
