from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

def get_direct_link(url):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path="geckodriver")

    try:
        driver.get(url)
        time.sleep(5)  # espera a que cargue el botón de descarga
        button = driver.find_element(By.ID, "downloadButton")
        direct_link = button.get_attribute("href")
        return direct_link
    finally:
        driver.quit()
