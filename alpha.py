import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading
from requests.exceptions import ConnectTimeout, ConnectionError

# Fungsi untuk membuat direktori baru jika belum ada
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Fungsi untuk mengunduh file PDF dari URL
def download_pdf(pdf_url, directory):
    try:
        response = requests.get(pdf_url, timeout=10)
        if response.status_code == 200:
            # Ekstrak nama file dari URL dan tentukan path file lokal
            file_name = pdf_url.split("/")[-1]
            file_path = os.path.join(directory, file_name)
            # Simpan konten respons ke dalam file PDF
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {file_name}")
    except ConnectTimeout as e:
        print("Timeout saat melakukan koneksi:", e)
    except ConnectionError as e:
        print("Gagal melakukan koneksi:", e)
    except Exception as e:
        print("Error lain:", e)

# Fungsi untuk mengunduh dan menyimpan file PDF dari halaman web
def download_pdf_files(url, directory):
    # Mendapatkan konten HTML dari halaman web
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Mendapatkan semua tag <a> dengan href berisi file PDF
    pdf_links = soup.find_all("a", href=lambda href: (href and href.endswith(".pdf")))

    # Mendownload dan menyimpan setiap file PDF dalam thread terpisah
    for link in pdf_links:
        pdf_url = urljoin(url, link["href"])
        # Memulai unduhan dalam thread terpisah
        thread = threading.Thread(target=download_pdf, args=(pdf_url, directory))
        thread.start()

    # Cek apakah ada halaman berikutnya
    next_page_link = soup.find("li", class_="next").find("a")["href"] if soup.find("li", class_="next") else None

    if next_page_link:
        next_page_url = urljoin(url, next_page_link)
        print(f"Mengunjungi halaman berikutnya: {next_page_url}")
        download_pdf_files(next_page_url, directory)
    else:
        print("Tidak ada halaman berikutnya.")

if __name__ == "__main__":
    # URL awal halaman web
    base_url = "https://peraturan.go.id/uu?page=1"
    # Direktori tempat menyimpan file PDF
    directory = "UU_scrap_threading"
    # Membuat direktori baru jika belum ada
    create_directory(directory)
    # Memulai proses mengunduh file PDF dari halaman web
    download_pdf_files(base_url, directory)
