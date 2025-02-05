import json
import os
import shutil
import subprocess
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

# Path konfigurasi
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Direktori skrip ini
ALLURE_RESULTS = os.path.join(BASE_DIR, "allure-results")
ALLURE_REPORT = os.path.join(BASE_DIR, "allure-report")
ALLURE_REPORT_DATA = os.path.join(ALLURE_REPORT, "data/test-cases")
ATTACHMENTS_PATH = os.path.join(ALLURE_REPORT, "data/attachments")
OUTPUT_PDF = "allure_steps_report1.pdf"
ZIP_FILE = "regression_report1.zip"


def run_tests():
    """ Menjalankan pytest dan generate report allure """
    print("Menjalankan pytest...")
    subprocess.run(["pytest", f"--alluredir={ALLURE_RESULTS}"], check=True)

    print("Menghasilkan laporan Allure...")
    allure_executable = shutil.which("allure")
    if not allure_executable:
        print("Allure executable not found. Please install Allure CLI.")
        return  # Exit early if Allure is not found

    try:
        subprocess.run([allure_executable, "generate", ALLURE_RESULTS, "-o", ALLURE_REPORT, "--clean"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during Allure report generation: {e}")
        return  # Exit early if Allure report generation fails


def extract_steps_and_screenshots():
    """ Ekstrak langkah dan screenshot dari laporan Allure """
    test_cases = []

    if not os.path.exists(ALLURE_REPORT_DATA):
        print(f"Error: Folder tidak ditemukan: {ALLURE_REPORT_DATA}")
        return test_cases

    for filename in os.listdir(ALLURE_REPORT_DATA):
        if filename.endswith(".json"):
            with open(os.path.join(ALLURE_REPORT_DATA, filename), "r", encoding="utf-8") as file:
                data = json.load(file)
                print(f"Membaca file: {filename}")  # Debug

                test_name = data.get("name", "Unknown Test")
                steps = []

                stages = data.get("beforeStages", []) + [data.get("testStage", {})] + data.get("afterStages", [])

                for stage in stages:
                    for step in stage.get("steps", []):
                        step_name = step.get("name", "Unknown Step")
                        status = step.get("status", "Unknown Status")
                        attachments = step.get("attachments", [])

                        screenshots = []
                        for attachment in attachments:
                            if attachment["name"] == "Screenshot" or attachment["type"] == "image/png":
                                screenshot_path = os.path.join(ATTACHMENTS_PATH, attachment["source"])
                                if os.path.exists(screenshot_path):
                                    screenshots.append(screenshot_path)
                                    print(f"Screenshot ditemukan: {screenshot_path}")
                                else:
                                    print(f"Screenshot tidak ditemukan: {screenshot_path}")

                        steps.append({"name": step_name, "status": status, "screenshots": screenshots})

                test_cases.append({"name": test_name, "steps": steps})

    return test_cases


def create_pdf(test_cases):
    """ Buat PDF dari data langkah dan screenshot menggunakan ReportLab """
    c = canvas.Canvas(OUTPUT_PDF, pagesize=letter)
    width, height = letter
    y_position = height - 40  # Mulai dari bagian atas halaman

    for test in test_cases:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y_position, f"Test: {test['name']}")
        y_position -= 20

        if not test["steps"]:
            c.drawString(60, y_position, "Tidak ada langkah ditemukan!")
            y_position -= 20

        for step in test["steps"]:
            c.setFont("Helvetica", 10)
            c.drawString(60, y_position, f"Step: {step['name']} - Status: {step['status']}")
            y_position -= 30  # Memberikan lebih banyak ruang antar langkah

            # Menyisipkan screenshot
            if step["screenshots"]:
                for screenshot in step["screenshots"]:
                    if os.path.exists(screenshot):
                        try:
                            img = ImageReader(screenshot)
                            img_width, img_height = img.getSize()
                            aspect_ratio = img_width / img_height

                            # Menyesuaikan ukuran gambar
                            max_width = 300
                            max_height = 200
                            if img_width > max_width or img_height > max_height:
                                if img_width > img_height:
                                    img_width = max_width
                                    img_height = img_width / aspect_ratio
                                else:
                                    img_height = max_height
                                    img_width = img_height * aspect_ratio

                            # Cek jika gambar terlalu besar untuk halaman
                            if img_height > (y_position - 40):  # Sisakan ruang untuk margin bawah
                                c.showPage()  # Buat halaman baru
                                y_position = height - 40  # Reset posisi Y

                            c.drawImage(img, 80, y_position - img_height, width=img_width, height=img_height)
                            y_position -= img_height + 20  # Geser posisi Y ke bawah
                        except Exception as e:
                            print(f"Error saat menyisipkan gambar {screenshot}: {e}")
                            c.drawString(60, y_position, f"Gambar gagal ditampilkan: {e}")
                            y_position -= 20
                    else:
                        print(f"Screenshot tidak ditemukan: {screenshot}")
                        c.drawString(60, y_position, "Screenshot tidak ditemukan!")
                        y_position -= 20
            else:
                c.drawString(60, y_position, "Tidak ada screenshot untuk langkah ini.")
                y_position -= 20

            y_position -= 10  # Pemisah antar langkah

        y_position -= 20  # Pemisah antar test case
        if y_position < 100:  # Jika ruang hampir habis, mulai halaman baru
            c.showPage()  # Memulai halaman baru
            y_position = height - 80  # Reset posisi Y di halaman baru

    c.save()


def create_zip():
    """ Membuat file ZIP dari hasil eksekusi """
    with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Tambahkan file PDF
        if os.path.exists(OUTPUT_PDF):
            zipf.write(OUTPUT_PDF, os.path.basename(OUTPUT_PDF))

        # Tambahkan laporan Allure
        for root, dirs, files in os.walk(ALLURE_REPORT):  # Pastikan seluruh folder Allure dimasukkan
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, ALLURE_REPORT)  # Mempertahankan struktur folder
                zipf.write(file_path, arcname)

    print(f"File ZIP berhasil dibuat: {ZIP_FILE}")


def main():
    """ Menjalankan keseluruhan proses """
    run_tests()  # Jalankan tes
    test_cases = extract_steps_and_screenshots()  # Ekstrak data langkah dan screenshot
    create_pdf(test_cases)  # Buat PDF dari data tes
    create_zip()  # Buat file ZIP dari hasil eksekusi


if __name__ == "__main__":
    main()
