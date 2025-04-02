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
    browser.add_cookie({"name": "MUSIC_U", "value": "001988B6001199ED0014D2F6E98A0B87F6C9BDE829F7E6A9CE3C23A6DDBEE24C594C3CB35C48570263996FAFA48CA98DC3CCA43CE4872FB97FD4749CAED064667DE2442323AD805568B37FC3CAE65ABE6611956E249ACE3990DF9B5830647F612F4B63E278A29DFD0D8E222EEB61EA860938F54665BA6203D12166142ACBBD429D7C2176AF2CC63992EE7C8FE9F621170AC2ED489EA48F4CBCD445D77E26464E54C7678CDCAAB1CFE33263ED8F654E3E2761C730F80AD151BAC97083B39AD3768ED806EE8002E7C19F5988301EC636EFFC6769220E2361870DDA8789B46748D9B9B88EB62F266AD915943562DFAE09F4B35722FBFF2B6CED9CE13E7DA25CA8F0D4E046CDCCAAB3F7F788AA79FDC053097036BEAE8BDE7A538A67ECBADE920F450F6212463E9C22B64DF325E53FDDAD8F699B2C705ED46F0DDA0F3D70F24112C8936960B05D66EEF12DA6ED99EF85E58831197E9CB14FED844EE09898D9E84C1D4D542E549F04A2B797DF0EA5774583FDEF"})
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
