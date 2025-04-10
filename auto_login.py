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
    browser.add_cookie({"name": "MUSIC_U", "value": "001E23209E756B28CB750F8623DE421574F8A1103FF5BBDDF51E3591305D5111BA1551FC46400C70D8604EFC055B3363D78664CC8CAA0EF58669DB9F795B8C02C185F50FFCE55B95E201F13D21A703A8ED4A0C6DECA75390D63482F0558AAA5CE021E9518E8FF7F5CF18B6200222BF3C6E7FE24B00343DB49217D7F467A368EF94E6AA5A54ED1C651BC09019FAC6451BAD5EDF7176928A85DF299DE4A5A8D00E8BFFA49491C3CDA10A1583A44EFB59CB0136AF9B300E30E8EBC3FF14AAD32164824CC6704921D9E3DD051A7F35C81D8FC92E80BB7DB6EF3CDA46B3EB6FA69C6409F4C79B28E28FF7795CBA4E321645E33EFAF650DA3CE6DA7F99276D011A3B3E074B7564102C61623FE990B7E4622521C461CF4621E36F9A4384CCF07ECDE4C3AD1D4DCFD6B66B315373CAA764D873BA49F1C2748F421D8124B3CA00122BE2820EAFE9207953A08DAB953EFE1AB3D6BDBC77FBEDDDA1CAD124976B4239136B7B011CFD3DBF3C5152CE637741749EB56472"})
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
