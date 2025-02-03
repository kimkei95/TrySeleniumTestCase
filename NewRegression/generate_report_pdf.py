

import os
import json
import shutil
import subprocess
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Path konfigurasi
ALLURE_RESULTS = "allure-results"
ALLURE_REPORT = "allure-report"
ALLURE_REPORT_DATA = os.path.join(ALLURE_REPORT, "data/test-cases")
ATTACHMENTS_PATH = os.path.join(ALLURE_REPORT, "data/attachments")
OUTPUT_PDF = "allure_steps_report.pdf"
ZIP_FILE = "regression_report.zip"

def run_tests():
    """ Menjalankan pytest dan generate report allure """
    print("Menjalankan pytest...")
    subprocess.run(["pytest", f"--alluredir={ALLURE_RESULTS}"], check=True)

    print("Menghasilkan laporan Allure...")
    allure_executable = "allure"

    if not shutil.which(allure_executable):
        allure_executable =r"C:\Users\akmal\scoop\apps\allure\2.32.0\bin"

        subprocess.run([allure_executable, "generate", ALLURE_RESULTS, "-o", ALLURE_REPORT, "--clean"], check=True)



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
                test_name = data.get("name", "Unknown Test")
                steps = []

                if "steps" in data:
                    for step in data["steps"]:
                        step_name = step.get("name", "Unknown Step")
                        status = step.get("status", "Unknown Status")
                        attachments = step.get("attachments", [])

                        screenshots = []
                        for attachment in attachments:
                            if attachment["name"] == "Screenshot":
                                screenshots.append(os.path.join(ATTACHMENTS_PATH, attachment["source"]))

                        steps.append({"name": step_name, "status": status, "screenshots": screenshots})

                test_cases.append({"name": test_name, "steps": steps})

    return test_cases

def create_pdf(test_cases):
    """ Buat PDF dari data langkah dan screenshot """
    c = canvas.Canvas(OUTPUT_PDF, pagesize=letter)
    width, height = letter
    y_position = height - 40

    for test in test_cases:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y_position, f"Test: {test['name']}")
        y_position -= 20

        for step in test["steps"]:
            c.setFont("Helvetica", 10)
            c.drawString(60, y_position, f"Step: {step['name']} - Status: {step['status']}")
            y_position -= 20

            for screenshot in step["screenshots"]:
                if os.path.exists(screenshot):
                    img = ImageReader(screenshot)
                    img_width = 300
                    img_height = 200
                    c.drawImage(img, 80, y_position - img_height, width=img_width, height=img_height)
                    y_position -= img_height + 20

            y_position -= 10

        y_position -= 20
        if y_position < 100:
            c.showPage()
            y_position = height - 40

    c.save()

def create_zip():
    """ Membuat file ZIP dari hasil eksekusi """
    with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Tambahkan file PDF
        if os.path.exists(OUTPUT_PDF):
            zipf.write(OUTPUT_PDF, os.path.basename(OUTPUT_PDF))

        # Tambahkan laporan Allure
        for root, dirs, files in os.walk(ALLURE_REPORT):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), ALLURE_REPORT))

        # Tambahkan hasil tes lainnya jika ada (misalnya file logs)
        # zipf.write('path/to/other/files', 'other/file/filename')

    print(f"File ZIP berhasil dibuat: {ZIP_FILE}")

def main():
    """ Menjalankan keseluruhan proses """
    run_tests()  # Jalankan tes
    test_cases = extract_steps_and_screenshots()  # Ekstrak data langkah dan screenshot
    create_pdf(test_cases)  # Buat PDF dari data tes
    create_zip()  # Buat file ZIP dari hasil eksekusi


if __name__ =="__main__":
    main()


