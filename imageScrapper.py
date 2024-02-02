import base64
import os

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


class ImageScrapper:

    base64_urls = []  # Required to download the first images since those are represented as base64 jpeg data
    encrypted_urls = []  # Remaining urls follow the https protocol
    headless: bool

    def __init__(self, headless: bool):
        try:
            options = Options()
            if headless:
                options.add_argument('--headless')
            driver = webdriver.Chrome(chrome_options=options)
            driver.set_window_size(1400, 1050)
            driver.get("https://www.google.com")
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "W0wltc"))).click()
        except Exception as e:
            exit(f"An error occured during the scrapper initialization : {e}")
        self.driver = driver
        self.headless = headless

    def find_urls(self, search_key, image_count):
        print(f"[INFO] : Searching for images using the keyword : {search_key}")
        search_url = f"https://www.google.com/search?q={search_key}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947"
        indx_1 = 0
        indx_2 = 0
        search_string = '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'
        alt_search_string = '//*[@id="islrg"]/div[1]/div[%s]/div[%s]/a[1]/div[1]/img'
        count = 0
        img_url = None

        self.driver.get(search_url)
        time.sleep(3)
        while count < image_count:
            if indx_2 > 0:
                try:
                    img_url = self.driver.find_element(By.XPATH, search_string % (indx_1, indx_2 + 1))
                    img_url.click()
                    indx_2 = indx_2 + 1
                except Exception:
                    try:
                        img_url = self.driver.find_element(By.XPATH, search_string % (indx_1 + 1, 1))
                        img_url.click()
                        indx_2 = 1
                        indx_1 = indx_1 + 1
                    except Exception:
                        indx_2 = indx_2 + 1
            else:
                try:
                    img_url = self.driver.find_element(By.XPATH, search_string % (indx_1 + 1))
                    img_url.click()

                    indx_1 = indx_1 + 1
                except Exception:
                    try:
                        img_url = self.driver.find_element(By.XPATH, alt_search_string % (indx_1, indx_2 + 1))
                        img_url.click()

                        indx_2 = indx_2 + 1
                        search_string = alt_search_string
                    except Exception:
                        indx_1 = indx_1 + 1
            if img_url is not None:
                print("Image url : ", img_url.get_attribute("src"))
                img_src = img_url.get_attribute("src")
                if "data:image/jpeg;base64," in img_src and img_src not in self.base64_urls:

                    self.base64_urls.append(img_src)
                    count += 1
                elif "encrypted" in img_src and img_src not in self.encrypted_urls:
                    self.encrypted_urls.append(img_src)
                    count += 1
            try:
                if count % 3 == 0:
                    self.driver.execute_script(f"window.scrollTo(0, {str(indx_1 * 60)});")
                element = self.driver.find_element(By.CLASS_NAME, "mye4qd")
                element.click()
                print("[INFO] Loading next page")
                time.sleep(3)
            except Exception:
                time.sleep(1)
        print("[INFO] : Urls scrapped successfully")

    def download_images(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        image_count = 0
        for base64string in self.base64_urls:
            image_data = base64.b64decode(base64string.replace("data:image/jpeg;base64,", ""))

            with open (path + f"/image{image_count}.jpg", 'wb') as file:
                file.write(image_data)
            image_count += 1
        for encryptedstring in self.encrypted_urls:
            response = requests.get(encryptedstring, stream=True)
            if response.status_code == 200:
                with open (path + f"/image{image_count}.jpg", 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                image_count += 1

    def connect(self):
        try:
            options = Options()
            if self.headless:
                options.add_argument('--headless')
            driver = webdriver.Chrome(chrome_options=options)
            driver.set_window_size(1400, 1050)
            driver.get("https://www.google.com")
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "W0wltc"))).click()
        except Exception as e:
            exit(f"An error occured during the scrapper initialization : {e}")
        self.driver = driver

    def destroy(self):
        self.driver.quit()
        print("[INFO] : Driver destroyed")

