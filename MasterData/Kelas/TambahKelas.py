from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, WebDriverException
import random
import time

from webdriver_manager.chrome import ChromeDriverManager


def tambah_kelas():
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

    # Klik Menu Master Data
    print("Klik menu Master Data...")
    master_data = wait.until(EC.element_to_be_clickable((By.XPATH, "(//*[@data-testid='sidebar-menu-master-data'])[2]")))
    master_data.click()

    # Klik Sidebar Menu Kelas
    print("Klik menu Kelas...")
    sidebar_menu_kelas = wait.until(EC.element_to_be_clickable((By.XPATH, "(//*[@data-testid='sidebar-menu-kelas'])[2]")))
    sidebar_menu_kelas.click()

    time.sleep(5)

    # Tambah Kelas
    print("Klik tombol Tambah Kelas...")
    button_tambah = driver.find_element(By.XPATH, "//*[@data-testid='btn-add-class']")
    button_tambah.click()
    time.sleep(3)

    # Dropdown Unit
    print("Memilih unit dari dropdown...")
    dropdown = driver.find_element(By.XPATH, "//*[@data-testid='selected-value']")
    dropdown.click()
    value_dropdown = driver.find_element(By.XPATH, "//*[@data-testid='paragraph']")
    value_dropdown.click()

    # Prefix
    print("Memilih prefix...")
    option_list = ["option-83", "option-73", "option-67", "option-66"]

    try:
        # Klik element1 untuk membuka dropdown
        element1 = driver.find_element(By.XPATH, "(//*[@data-testid='selected-value'])[2]")
        element1.click()

        # Pilih salah satu option secara random
        selected_option = random.choice(option_list)

        try:
            # Cari elemen berdasarkan data-testid yang dipilih secara random
            value_element1 = driver.find_element(By.XPATH, f"//*[@data-testid='{selected_option}']")
            value_element1.click()
            print(f"Berhasil memilih: {selected_option}")
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            print(f"Gagal memilih option {selected_option}: {e}")

    except (NoSuchElementException, ElementClickInterceptedException) as e:
        print(f"Gagal membuka dropdown: {e}")

    # Pilih Jurusan
    print("Memilih jurusan...")
    opsi_jurusan = ["option-53", "option-52", "option-48", "option-50", "option-35"]

    try:
        # Klik dropdown untuk membuka pilihan jurusan
        jurusan = driver.find_element(By.XPATH, "(//*[@data-testid='selected-value'])[3]")
        jurusan.click()
        time.sleep(2)  # Tunggu sebentar agar opsi muncul


        selected_jurusan = random.choice(opsi_jurusan)

        try:
            jurusan_option = driver.find_element(By.XPATH, f"//*[@data-testid='{selected_jurusan}']")
            jurusan_option.click()
            print(f"Berhasil memilih jurusan: {selected_jurusan}")
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            print(f"Gagal memilih jurusan {selected_jurusan}: {e}")

    except (NoSuchElementException, ElementClickInterceptedException) as e:
        print(f"Gagal membuka dropdown jurusan: {e}")

    # Suffix
    suffix_list = ["sesat", "jalan", "random", "acak", "test", "example"]

    # Memilih suffix secara acak
    random_suffix = random.choice(suffix_list)

    print("Mengisi suffix...")

    try:
        suffix = driver.find_element(By.NAME, "suffix")
        suffix.click()
        suffix.send_keys(random_suffix)

        print(f"Suffix '{random_suffix}' berhasil diisi.")
    except WebDriverException as e:
        print(f"Error: Terjadi kesalahan saat mengakses WebDriver. Pesan error: {e}")

    # Terapkan
    try:
        print("Menunggu tombol Tambahkan dapat diklik...")
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'flex items-center text-center') and text()='Tambahkan']")
            )
        )
        element.click()
        print("Tombol Tambahkan berhasil diklik!")
    except Exception as e:
        print(f"Error saat mengklik tombol Tambahkan: {e}")
    time.sleep(6)

    # Menutup browser
    print("Menutup browser...")
    driver.quit()

if tambah_kelas() == "_main_":
    tambah_kelas()