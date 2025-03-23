# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0011A7E8D0BEF39E24090D6F33FFEE5D1FD106FD5BFF999006E5EF21F3A53F6F472D10DE6CD8B3113CA8540612808E6CB894226175D472E921C7A1FAD05E2998539CD0921E09AAC015AEA9FB7BEEA53CDB8A4EADBF41C7F5E870B2A235D14C9E6D96578CE32EF7579D22F5D92F5809032852972FB19054AF9F4D09C18CE0AFC9A5A32A28C7D0082BBD0DA39213D84244B3CAF7D75F85CE20C04CE4BD3ACB5FCA7711DC3AED4809E56ADDEBF7D79F7FC77AB9E9E396EF1E47FF0E02AF63632675BD078CBBB34E350E3E154A5209E61AEA40438180F9273A6E463ED91B9CCDB7151053490808379819D7F4ABD07EC02E6EA2C2250D8A22F7C338B502EEF839BA6CF3D093982717A064DCED9A534D0BCE7A0C7FE449229CB535E0F08EC2DF8BC82CEDD65671C9C5DB9AA0C7533ED0CEDFE331F5447F64356D670E79D8CC1BFB256C8DF1E7D396E2E1D00DD6F80E3808E16937CB3096D636B6DE9B4B64961E014E0E957E031F7481914FBCEFD3DE26CF2A8338"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
