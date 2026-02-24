"""
Simple Classera Daily Report Downloader
Downloads the latest daily report from Classera with provided credentials
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import sys
import argparse

def download_daily_report(username, password, download_path="./downloads", quiet=False):
    """
    Download the latest daily report from Classera
    
    Args:
        username: Classera username
        password: Classera password  
        download_path: Where to save the downloaded file
        quiet: If True, suppress progress messages
    
    Returns:
        Path to downloaded file or None if failed
    """
    
    def log(msg):
        if not quiet:
            print(msg)
    
    # Create download directory
    download_dir = os.path.abspath(download_path)
    os.makedirs(download_dir, exist_ok=True)
    
    # Clean old files
    for f in os.listdir(download_dir):
        file_path = os.path.join(download_dir, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    log(f"📁 Download directory: {download_dir}")
    
    # Configure Chrome
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "safebrowsing.disable_download_protection": True,
        "profile.default_content_settings.popups": 0,
        "profile.default_content_setting_values.automatic_downloads": 1
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--silent")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    log("🌐 Starting browser...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Login
        log("🔐 Logging in to Classera...")
        driver.get("https://me.classera.com/#networkfirst")
        time.sleep(5)
        
        email_input = driver.find_element(By.NAME, "data[User][username]")
        email_input.send_keys(username)
        password_input = driver.find_element(By.NAME, "data[User][password]")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)
        
        # Navigate to document library
        log("📚 Navigating to document library...")
        driver.get("https://me.classera.com/student/courses/bdoc_list")
        time.sleep(5)
        
        # Find download links
        all_links = driver.find_elements(By.TAG_NAME, "a")
        download_links = []
        
        for i, link in enumerate(all_links):
            try:
                text = link.text.strip()
                href = link.get_attribute("href")
                if text and ("download" in text.lower() or "تحميل" in text):
                    download_links.append((i, text, href, link))
            except:
                continue
        
        if not download_links:
            log("❌ No download links found")
            return None
        
        log(f"📄 Found {len(download_links)} download link(s)")
        
        # Click first download link
        _, link_text, _, target_link = download_links[0]
        log(f"📥 Accessing: '{link_text}'")
        target_link.click()
        time.sleep(5)
        
        # Find download button
        download_button = None
        selectors = [
            "//a[contains(@href, '/attachments/download/') and contains(@class, 'btn')]",
            "//a[contains(@href, '/download/aid:')]",
            "//a[contains(text(), 'Download') and contains(@class, 'btn')]",
            "//a[contains(@class, 'btn-primary') and contains(text(), 'Download')]"
        ]
        
        for selector in selectors:
            try:
                download_button = driver.find_element(By.XPATH, selector)
                break
            except:
                continue
        
        if not download_button:
            log("❌ Could not find download button")
            return None
        
        # Download the file
        log("⬇️ Downloading file...")
        download_button.click()
        
        # Wait for download to complete
        timeout = 60
        start_time = time.time()
        downloaded_file = None
        
        while time.time() - start_time < timeout:
            files = [f for f in os.listdir(download_dir) 
                    if os.path.isfile(os.path.join(download_dir, f)) 
                    and not f.endswith('.crdownload') 
                    and not f.endswith('.tmp')]
            
            if files:
                downloaded_file = os.path.join(download_dir, files[0])
                break
            
            time.sleep(1)
        
        if downloaded_file:
            file_size = os.path.getsize(downloaded_file)
            log(f"✅ Downloaded: {os.path.basename(downloaded_file)} ({file_size:,} bytes)")
            return downloaded_file
        else:
            log("❌ Download timed out")
            return None
            
    except Exception as e:
        log(f"❌ Error: {e}")
        return None
        
    finally:
        driver.quit()
        log("🔒 Browser closed")


def main():
    parser = argparse.ArgumentParser(description='Download Classera Daily Report')
    parser.add_argument('--username', '-u', required=True, help='Classera username')
    parser.add_argument('--password', '-p', required=True, help='Classera password')
    parser.add_argument('--output', '-o', default='./downloads', help='Download directory (default: ./downloads)')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress progress messages')
    
    args = parser.parse_args()
    
    result = download_daily_report(
        username=args.username,
        password=args.password,
        download_path=args.output,
        quiet=args.quiet
    )
    
    if result:
        print(f"\n📄 Report saved to: {result}")
        sys.exit(0)
    else:
        print("\n❌ Failed to download report")
        sys.exit(1)


if __name__ == "__main__":
    main()
