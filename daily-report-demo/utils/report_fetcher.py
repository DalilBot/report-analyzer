"""
Classera Daily Report Fetcher
Downloads the latest daily report PDF from Classera using Selenium
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


def download_daily_report(username, password, download_path="./downloads", on_status=None):
    """
    Download the latest daily report from Classera.

    Args:
        username: Classera username
        password: Classera password
        download_path: Where to save the downloaded file
        on_status: Optional callback(message) for progress updates

    Returns:
        Path to downloaded file or None if failed
    """
    def log(msg):
        if on_status:
            on_status(msg)

    download_dir = os.path.abspath(download_path)
    os.makedirs(download_dir, exist_ok=True)

    # Clean old files
    for f in os.listdir(download_dir):
        file_path = os.path.join(download_dir, f)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Configure Chrome headless
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

    log("Starting browser...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        log("Logging in to Classera...")
        driver.get("https://me.classera.com/#networkfirst")
        time.sleep(5)

        email_input = driver.find_element(By.NAME, "data[User][username]")
        email_input.send_keys(username)
        password_input = driver.find_element(By.NAME, "data[User][password]")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        log("Navigating to document library...")
        driver.get("https://me.classera.com/student/courses/bdoc_list")
        time.sleep(5)

        # Find download links
        all_links = driver.find_elements(By.TAG_NAME, "a")
        download_links = []

        for link in all_links:
            try:
                text = link.text.strip()
                if text and ("download" in text.lower() or "تحميل" in text):
                    download_links.append(link)
            except Exception:
                continue

        if not download_links:
            log("No download links found")
            return None

        log(f"Found {len(download_links)} download link(s)")

        download_links[0].click()
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
            except Exception:
                continue

        if not download_button:
            log("Could not find download button")
            return None

        log("Downloading file...")
        download_button.click()

        # Wait for download
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
            size = os.path.getsize(downloaded_file)
            log(f"Downloaded: {os.path.basename(downloaded_file)} ({size:,} bytes)")
            return downloaded_file
        else:
            log("Download timed out")
            return None

    except Exception as e:
        log(f"Error: {e}")
        return None

    finally:
        driver.quit()
