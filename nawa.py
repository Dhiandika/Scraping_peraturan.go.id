import requests
import os
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading

# Fungsi untuk membuat direktori baru jika belum ada
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Fungsi untuk mendownload file PDF
def download_pdf(pdf_url, pdf_path):
    response = requests.get(pdf_url)
    with open(pdf_path, "wb") as pdf_file:
        pdf_file.write(response.content)
        print(f"File {pdf_path} berhasil diunduh")

# Fungsi untuk scraping informasi undang-undang
def scrape_uu(page_num, base_url, url, directory, writer):
    # Mendapatkan konten HTML dari halaman web
    response = requests.get(url + str(page_num))
    soup = BeautifulSoup(response.content, "html.parser")

    # Mendapatkan semua tag <div> dengan class "col-md-12" yang berisi informasi undang-undang
    uu_divs = soup.find_all("div", class_="strip grid")

    for uu_div in uu_divs:
        # Mendapatkan informasi undang-undang
        uu_title = uu_div.find("p", style="padding-top: -2;").text.strip()
        pdf_link = uu_div.find("a", href=lambda href: (href and href.endswith(".pdf")))
        pdf_url = urljoin(base_url, pdf_link["href"])
        pdf_name = pdf_link["href"].split("/")[-1]
        pdf_path = os.path.join(directory, pdf_name)

        # Mendapatkan kementerian yang terkait dengan undang-undang
        ministry = uu_div.find("span", class_="loc_open").text.strip()

        # Mendapatkan konteks undang-undang
        context = uu_div.find("p").find_next_sibling("p").text.strip()

        # Menulis informasi undang-undang ke dalam file CSV
        writer.writerow({'Judul': uu_title, 'Kementerian': ministry, 'Konteks': context, 'Link Download': pdf_url})

        # Mendownload file PDF menggunakan threading
        threading.Thread(target=download_pdf, args=(pdf_url, pdf_path)).start()

# URL halaman web
base_url = "https://peraturan.go.id/permen"
url = base_url + "?page="

# Direktori tempat menyimpan file PDF
directory = "UU_scrap"

# Membuat direktori baru jika belum ada
create_directory(directory)

# Membuka file CSV untuk menyimpan data undang-undang
csv_file_path = "undang_undang.csv"
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Judul', 'Kementerian', 'Konteks', 'Link Download']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Mendapatkan jumlah halaman total
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")
    pagination = soup.find("div", class_="pagination__wrapper")
    total_pages = int(pagination.find_all("a")[-2].text)

    # Membuat array untuk menyimpan thread
    threads = []

    # Scraping informasi undang-undang menggunakan threading
    for page_num in range(1, min(total_pages, 11)):  # Scraping hingga halaman 10 atau hingga halaman terakhir jika kurang dari 10 halaman
        thread = threading.Thread(target=scrape_uu, args=(page_num, base_url, url, directory, writer))
        threads.append(thread)
        thread.start()

    # Menunggu hingga semua thread selesai
    for thread in threads:
        thread.join()

print("Proses scraping selesai. Data undang-undang tersimpan dalam file CSV.")
