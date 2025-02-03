import pytest
import random
import os
import time
from selenium import webdriver
from selenium.common import (
    ElementClickInterceptedException,
    NoSuchElementException,
    WebDriverException,
)
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import allure

# Setup Direktori Screenshot
screenshot_dir = "TrySeleniumTestCase/NewRegression/screenshots"
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()


def capture_screenshot(driver, request, step_name, attempt):
    test_name = request.node.name
    iteration_screenshot_dir = os.path.join(screenshot_dir, f"attempt_{attempt}")
    if not os.path.exists(iteration_screenshot_dir):
        os.makedirs(iteration_screenshot_dir)
    screenshot_path = os.path.join(
        iteration_screenshot_dir, f"{test_name}_{step_name}.png"
    )
    driver.save_screenshot(screenshot_path)
    allure.attach.file(
        screenshot_path,
        name=f"{step_name} (Attempt {attempt})",
        attachment_type=allure.attachment_type.PNG,
    )
    print(f"Screenshot saved: {screenshot_path}")


@pytest.mark.order(1)
@allure.feature("Add Bank Account")
def test_tambah_bank(driver, request):
    for attempt in range(1):
        try:
            print(f"Iteration {attempt + 1} started")
            driver.get("https://sit.siprusedu.com/login")
            capture_screenshot(driver, request, "01_login_page", attempt + 1)

            with allure.step("Fill login form"):
                wait = WebDriverWait(driver, 10)
                # Login
                email = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//input[@name='email']"))
                )
                password = driver.find_element(By.NAME, "password")
                login_button = driver.find_element(
                    By.XPATH, "//*[@id='__next']/div[1]/main/div[1]/div/form/button"
                )
                email.send_keys("admin.sekolah@gmail.com")
                password.send_keys("Test1234")
                capture_screenshot(driver, request, "02_filled_login_form", attempt + 1)
                login_button.click()
                time.sleep(9)
                capture_screenshot(driver, request, "03_after_login", attempt + 1)

            with allure.step("Navigate to Master Data"):
                # Navigasi ke Master Data
                master_data = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "(//*[@data-testid='sidebar-menu-master-data'])[2]")
                    )
                )
                master_data.click()
                time.sleep(6)
                capture_screenshot(driver, request, "04_master_data_page", attempt + 1)

            with allure.step("Navigate to Akun Bank"):
                # Navigasi ke Akun Bank
                akun_bank = driver.find_element(
                    By.XPATH, "(//*[@data-testid='sidebar-menu-akun-bank'])[2]"
                )
                akun_bank.click()
                time.sleep(6)
                capture_screenshot(driver, request, "05_akun_bank_page", attempt + 1)

            with allure.step("Add new Bank Account"):
                # Klik Tambah Akun Bank
                btn_tambah = driver.find_element(
                    By.XPATH, "//*[@data-testid='btn-add-bank']"
                )
                btn_tambah.click()
                time.sleep(6)
                capture_screenshot(driver, request, "06_tambah_akun_bank_page", attempt + 1)

            with allure.step("Select Bank and Fill Account Info"):
                # Pilih Nama Bank
                dropdown_bank = driver.find_element(
                    By.XPATH, "//*[@data-testid='selected-value']"
                )
                dropdown_bank.click()
                value_bank = driver.find_element(
                    By.XPATH,
                    "//*[@data-testid='option-PT. BANK CIMB NIAGA UNIT USAHA SYARIAH - (CIMB SYARIAH)']",
                )
                value_bank.click()
                time.sleep(3)
                capture_screenshot(driver, request, "07_selected_bank", attempt + 1)

                # Input Nama Rekening
                nasabah = driver.find_element(
                    By.XPATH, "//*[@data-testid='field-bank-name']"
                )
                nasabah.click()
                nasabah_list = [
                    "Toni", "Jono", "Budi Handoko", "Kim Jong Un", "Tony Stark",
                    "Tony Hawk", "Dani Aditya", "Oda Nobunaga", "Itachi Uchiha",
                ]
                random_nasabah = random.choice(nasabah_list)
                nasabah.send_keys(random_nasabah)
                time.sleep(7)
                capture_screenshot(driver, request, "08_filled_nasabah_name", attempt + 1)

                # Input Nomor Rekening
                norek = driver.find_element(
                    By.XPATH, "//*[@data-testid='field-bank-number']"
                )
                norek.click()
                random_number = random.randint(10000, 99999)
                norek.send_keys(random_number)
                time.sleep(5)
                capture_screenshot(driver, request, "09_filled_norek", attempt + 1)

            with allure.step("Select Ownership and Submit"):
                # Pilih Kepemilikan
                kepemilikan = driver.find_element(
                    By.XPATH, "(//*[@data-testid='selected-value'])[2]"
                )
                kepemilikan.click()
                value_kepemilikan = driver.find_element(
                    By.XPATH, "(//*[@data-testid='paragraph'])[1]"
                )
                value_kepemilikan.click()
                capture_screenshot(driver, request, "10_selected_kepemilikan", attempt + 1)

                # Klik Tambahkan
                button_tambahData = driver.find_element(
                    By.XPATH,
                    "//button[contains(@class, 'rounded-[6px]') and .//div[text()='Tambahkan']]",
                )
                button_tambahData.click()
                time.sleep(6)
                capture_screenshot(driver, request, "11_submission_completed", attempt + 1)

            print(f"Iteration {attempt + 1} completed")
        except Exception as e:
            print(f"❌ Error occurred in iteration {attempt + 1}: {e}")
            capture_screenshot(
                driver, request, f"error_iteration_{attempt + 1}", attempt + 1
            )
        finally:
            # Bersihkan state sebelum iterasi berikutnya
            driver.delete_all_cookies()
            driver.refresh()
            time.sleep(3)

# You can similarly apply `allure.step` to other tests (`test_edit_bank`, `test_tambah_kelas`) following the same structure.
