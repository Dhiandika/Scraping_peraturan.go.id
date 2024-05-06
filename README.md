# Scraping_peraturan.go.id
 ini merupakan repository untuk melakukan scraping pada web peraturan.go.id

## Gunakan kode di bawah untuk mengerun kode yang ada

```
  python file.py
```

| file | Description                |
| :-------- | :------------------------- |
| `alpha.py` | Melakukan scraping dengan menggunakan threading sampai batas page yang di tentukan |
| `scrap.py` | Melakukan scraping hanya 1 page |
| `uuscrap.py` | Melakukan scraping secara otomatis dan perlahan hingga page berikutnya sampai habis |
| `nazo.py` | Melakukan scraping secara otomatis dan perlahan hingga page yang di tentukan dan membuat folder csv file yang di download dengan kolom `Judul`,`kementrian`,`link downlad`, berikutnya sampai habis |
| `nawa.py` | Melakukan scraping secara otomatis dan perlahan hingga page yang di tentukan dan membuat folder csv file yang di download dengan kolom `Judul`,`kementrian`,`konteks`,`link downlad`, berikutnya sampai habis |


### Contoh output Csv 
| Judul                             | Kementerian      | Konteks                               | Link Download                                 |
|-----------------------------------|------------------|---------------------------------------|-----------------------------------------------|
| Undang-Undang Nomor 16 Tahun 2022 | Pemerintah Pusat | Pembentukan Provinsi Papua Pegunungan | https://peraturan.go.id/files/UU_Nomor_16.pdf |
| Undang-Undang Nomor 6 Tahun 2017  | Pemerintah Pusat | Arsitek                               | https://peraturan.go.id/files/uu6-2017bt.pdf  |
| Undang-Undang Nomor 8 Tahun 2016  | Pemerintah Pusat | Penyandang Disabilitas                | https://peraturan.go.id/files/uu8-2016bt.pdf  |
| Undang-Undang Nomor 7 Tahun 2017  | Pemerintah Pusat | Pemilihan Umum                        | https://peraturan.go.id/files/uu7-2017bt.pdf  |