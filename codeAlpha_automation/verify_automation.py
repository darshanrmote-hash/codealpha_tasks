import os
import shutil
import re
import requests
from datetime import datetime

# Import functions from task_automation
import task_automation

def setup_test_environment():
    print("[*] Setting up test environment...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_assets_dir = os.path.join(base_dir, "test_assets")
    src_images_dir = os.path.join(test_assets_dir, "src_images")
    dest_images_dir = os.path.join(test_assets_dir, "dest_images")
    
    # Clean and recreate directories
    for d in [src_images_dir, dest_images_dir]:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
        
    # Create mock images and other files
    open(os.path.join(src_images_dir, "image1.jpg"), "w").close()
    open(os.path.join(src_images_dir, "image2.JPEG"), "w").close()
    open(os.path.join(src_images_dir, "document.pdf"), "w").close()
    open(os.path.join(src_images_dir, "readme.txt"), "w").close()
    
    print(f"  - Created mock source images folder at: {src_images_dir}")
    print(f"  - Created empty target destination folder at: {dest_images_dir}")
    
    return src_images_dir, dest_images_dir

def run_tests():
    src_img, dest_img = setup_test_environment()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_assets_dir = os.path.join(base_dir, "test_assets")
    
    print("\n" + "=" * 50)
    print("TEST 1: File Organizer (.jpg/.jpeg)")
    print("=" * 50)
    # We will simulate the function logic programmatically since it asks for inputs
    # Let's inspect the files in src before
    print(f"Files in source before organizing: {os.listdir(src_img)}")
    
    # We can invoke shutil/os logic directly as in task_automation.py, or we can mock/simulate input.
    # To run the exact code, we can temporarily patch input or just call the core logic.
    # Since we want to test task_automation.py, let's mock builtins.input.
    import builtins
    original_input = builtins.input
    
    # Mocking input for Feature 1 (File Organizer)
    inputs_1 = [src_img, dest_img]
    def mock_input_1(prompt):
        val = inputs_1.pop(0)
        print(f"{prompt}{val}")
        return val
        
    builtins.input = mock_input_1
    try:
        task_automation.organize_jpg_files()
    except Exception as e:
        print(f"Test 1 failed with error: {e}")
    finally:
        builtins.input = original_input
        
    print(f"Files left in source: {os.listdir(src_img)}")
    print(f"Files moved to destination: {os.listdir(dest_img)}")
    
    # Assertions
    assert "image1.jpg" in os.listdir(dest_img)
    assert "image2.JPEG" in os.listdir(dest_img)
    assert "document.pdf" in os.listdir(src_img)
    assert "readme.txt" in os.listdir(src_img)
    print("[✓] Test 1 passed: Only .jpg and .jpeg files were moved!")
    
    print("\n" + "=" * 50)
    print("TEST 2: Email Extractor")
    print("=" * 50)
    
    test_emails_file = os.path.join(test_assets_dir, "test_emails.txt")
    output_emails_file = os.path.join(test_assets_dir, "extracted_emails.txt")
    
    if os.path.exists(output_emails_file):
        os.remove(output_emails_file)
        
    # Mock input for Feature 2
    inputs_2 = [test_emails_file, output_emails_file]
    def mock_input_2(prompt):
        val = inputs_2.pop(0)
        print(f"{prompt}{val}")
        return val
        
    builtins.input = mock_input_2
    try:
        task_automation.extract_email_addresses()
    except Exception as e:
        print(f"Test 2 failed with error: {e}")
    finally:
        builtins.input = original_input
        
    # Verify emails
    assert os.path.exists(output_emails_file)
    with open(output_emails_file, "r") as f:
        extracted = f.read().splitlines()
        
    print(f"Extracted unique emails: {extracted}")
    expected_emails = ["admin@example.com", "info@domain.org", "sales@example.com", "support@example.com"]
    for email in expected_emails:
        assert email in extracted
    assert len(extracted) == 4
    print("[✓] Test 2 passed: All unique valid emails extracted successfully!")
    
    print("\n" + "=" * 50)
    print("TEST 3: Webpage Title Scraper")
    print("=" * 50)
    
    # We will scrape a highly stable page (like https://python.org or https://www.google.com)
    # Let's clean the log file first if it exists
    log_file = "scraped_titles.txt"
    if os.path.exists(log_file):
        os.remove(log_file)
        
    inputs_3 = ["https://python.org"]
    def mock_input_3(prompt):
        val = inputs_3.pop(0)
        print(f"{prompt}{val}")
        return val
        
    builtins.input = mock_input_3
    try:
        task_automation.scrape_webpage_title()
    except Exception as e:
        print(f"Test 3 failed with error: {e}")
    finally:
        builtins.input = original_input
        
    assert os.path.exists(log_file)
    with open(log_file, "r", encoding="utf-8") as f:
        log_content = f.read()
    print(f"Log content:\n{log_content}")
    assert "python" in log_content.lower()
    print("[✓] Test 3 passed: Page title scraped and logged successfully!")

if __name__ == "__main__":
    run_tests()
