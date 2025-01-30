import logging
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def menghapus_sumbangan():
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--headless")

    # Inisialisasi driver
    print("Inisialisasi driver...")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    # Akses URL
    driver.get("https://sit.siprusedu.com/login")
    print("Membuka halaman login")

    # Tunggu hingga elemen email dapat ditemukan
    wait = WebDriverWait(driver, 10)  # Tunggu hingga 10 detik
    email = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='email']")))
    print("Field email ditemukan")

    password = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.XPATH, "//*[@id='__next']/div[1]/main/div[1]/div/form/button")

    # Masukkan kredensial
    email.send_keys("admin.sekolah@gmail.com")
    password.send_keys("Test1234")
    print("Kredensial telah dimasukkan")

    # Klik tombol login
    login_button.click()
    print("Tombol login diklik")

    # Tunggu beberapa detik setelah login
    time.sleep(9)

    # Klik Menu Master Data
    master_data = wait.until(EC.element_to_be_clickable((By.XPATH, "(//*[@data-testid='sidebar-menu-master-data'])[2]")))

    master_data.click()
    print("Menu Master Data diklik")

    # Klik menu Sumbangan
    sumbangan = driver.find_element(By.XPATH, "(//*[@data-testid='sidebar-menu-sumbangan'])[2]")
    driver.execute_script("arguments[0].scrollIntoView(true);", sumbangan)
    time.sleep(1)  # Tunggu sejenak
    sumbangan.click()
    print("Menu Sumbangan diklik")
    time.sleep(5)

    # Hapus Sumbangan
    hapus_sumbangan = driver.find_element(By.XPATH,"(//button[contains(text(), 'Hapus')])[1]")
    hapus_sumbangan.click()
    print("Tombol Hapus diklik")
    time.sleep(5)

    # Klik Ya
    ya = driver.find_element(By.XPATH,"//div[text()='Ya']")
    ya.click()
    print("Tombol konfirmasi 'Ya' diklik")

    time.sleep(6)

    driver.quit()
    print("Driver dihentikan, skrip selesai")


if menghapus_sumbangan() == "_main_":
    menghapus_sumbangan()