import random

import pyautogui
from selenium import webdriver
from selenium.common import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def filter_user():
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--headless")

        # Inisialisasi driver
    print("Inisialisasi driver...")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

            # Akses URL
    print("Mengakses URL...")
    driver.get("https://sit.siprusedu.com/login")

            # Tunggu hingga elemen email dapat ditemukan
    print("Menunggu elemen login...")
    wait = WebDriverWait(driver, 10)
    email = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='email']")))
    password = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.XPATH, "//*[@id='__next']/div[1]/main/div[1]/div/form/button")

            # Masukkan kredensial
    print("Mengisi kredensial login...")
    email.send_keys("admin.sekolah@gmail.com")
    password.send_keys("Test1234")

            # Klik tombol login
    print("Klik tombol login...")
    login_button.click()

            # Tunggu beberapa detik setelah login
    time.sleep(9)


        #Klik Menu User Management

    menu_userManagement = driver.find_element(By.XPATH,"(//*[@data-testid='sidebar-menu-user-management'])[2]")
    menu_userManagement.click()
    time.sleep(4)


        # Filter

    try:
        filterByRole = driver.find_element(By.XPATH, "(//*[@data-testid='selected-value'][1])")
        filterByRole.click()

        valueRole = ["option-2", "option-3", "option-4", "option-5"]
        selected_role = random.choice(valueRole)

        # Cari dan klik opsi yang dipilih secara acak
        try:
            role_option = driver.find_element(By.XPATH,"//*[@data-testid='dropdown-menu']")  # Asumsi elemen memiliki ID sesuai dengan array
            role_option.click()
            time.sleep(5)
            print(f"Berhasil memilih role: {selected_role}")
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            print(f"Gagal memilih role {selected_role}: {e}")
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        print(f"Gagal membuka filter role: {e}")

    driver.quit()

if filter_user() =="_main_":
    filter_user()