import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Fungsi untuk membuat direktori baru jika belum ada
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# URL halaman web
url = "https://peraturan.go.id/uu"

# Direktori tempat menyimpan file PDF
directory = "UU_scrap"

# Membuat direktori baru jika belum ada
create_directory(directory)

# Mendapatkan konten HTML dari halaman web
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Mendapatkan semua tag <a> dengan href berisi file PDF
pdf_links = soup.find_all("a", href=lambda href: (href and href.endswith(".pdf")))

# Mendownload dan menyimpan setiap file PDF
for link in pdf_links:
    pdf_url = urljoin(url, link["href"])
    pdf_name = link["href"].split("/")[-1]  # Nama file PDF
    pdf_path = os.path.join(directory, pdf_name)  # Path lengkap file PDF

    # Mendownload file PDF
    with open(pdf_path, "wb") as pdf_file:
        response = requests.get(pdf_url)
        pdf_file.write(response.content)
        print(f"File {pdf_name} berhasil diunduh dan disimpan di {pdf_path}")
