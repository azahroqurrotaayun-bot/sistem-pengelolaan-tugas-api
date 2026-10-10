\# Sistem Pengelolaan Tugas API



\## 1. Deskripsi Proyek



Sistem Pengelolaan Tugas API adalah aplikasi REST API yang digunakan untuk mengelola data mahasiswa, mata kuliah, status tugas, tugas, dan pengumpulan tugas. Aplikasi dibuat menggunakan Python dengan framework FastAPI dan database PostgreSQL.



Proyek ini menerapkan operasi CRUD (Create, Read, Update, Delete) dan di-deploy menggunakan Vercel agar dapat diakses secara online.



\## 2. Teknologi yang Digunakan



\- Python

\- FastAPI

\- PostgreSQL

\- Neon sebagai hosting database

\- Vercel sebagai platform deployment

\- Git dan GitHub

\- Swagger UI untuk pengujian API



\## 3. Struktur Database



Database terdiri dari lima tabel:



1\. \*\*mahasiswa\*\*: menyimpan ID mahasiswa, NIM, nama mahasiswa, dan email.

2\. \*\*mata\_kuliah\*\*: menyimpan ID mata kuliah, kode mata kuliah, nama mata kuliah, dan SKS.

3\. \*\*status\_tugas\*\*: menyimpan daftar status tugas.

4\. \*\*tugas\*\*: menyimpan informasi tugas, mahasiswa, mata kuliah, status, tanggal diberikan, dan deadline.

5\. \*\*pengumpulan\_tugas\*\*: menyimpan tanggal pengumpulan, tautan file, dan catatan pengumpulan tugas.



\### Relasi Antar Tabel



\- `mahasiswa` berelasi dengan `tugas` melalui `id\_mahasiswa`.

\- `mata\_kuliah` berelasi dengan `tugas` melalui `id\_mata\_kuliah`.

\- `status\_tugas` berelasi dengan `tugas` melalui `id\_status`.

\- `tugas` berelasi dengan `pengumpulan\_tugas` melalui `id\_tugas`.



\## 4. Daftar Endpoint API



| Metode | Endpoint | Fungsi |

|---|---|---|

| GET | `/` | Menampilkan informasi API |

| GET | `/health` | Memeriksa status API |

| GET | `/mahasiswa` | Menampilkan data mahasiswa |

| GET | `/mata-kuliah` | Menampilkan data mata kuliah |

| GET | `/status-tugas` | Menampilkan daftar status tugas |

| GET | `/tugas` | Menampilkan daftar tugas |

| GET | `/tugas/{id\_tugas}` | Menampilkan detail tugas |

| POST | `/tugas` | Menambahkan tugas |

| PUT | `/tugas/{id\_tugas}` | Memperbarui seluruh data tugas |

| PATCH | `/tugas/{id\_tugas}` | Memperbarui sebagian data tugas |

| DELETE | `/tugas/{id\_tugas}` | Menghapus tugas |

| GET | `/pengumpulan-tugas` | Menampilkan data pengumpulan tugas |



\## 5. URL Proyek



\- \*\*GitHub Repository:\*\* https://github.com/azahroqurrotaayun-bot/sistem-pengelolaan-tugas-api

\- \*\*Deployment URL:\*\* https://sistem-pengelolaan-tugas-api.vercel.app

\- \*\*Dokumentasi API:\*\* https://sistem-pengelolaan-tugas-api.vercel.app/docs



\## 6. Cara Menjalankan API Secara Lokal



\### Persyaratan



\- Python

\- Git

\- Database PostgreSQL yang dapat diakses



\### Langkah Menjalankan



1\. Clone repositori GitHub:



&#x20;  ```bash

&#x20;  git clone https://github.com/azahroqurrotaayun-bot/sistem-pengelolaan-tugas-api.git

&#x20;  ```



2\. Masuk ke folder proyek:



&#x20;  ```bash

&#x20;  cd sistem-pengelolaan-tugas-api

&#x20;  ```



3\. Buat virtual environment:



&#x20;  ```bash

&#x20;  python -m venv .venv

&#x20;  ```



4\. Aktifkan virtual environment di Windows:



&#x20;  ```bash

&#x20;  .venv\\Scripts\\activate

&#x20;  ```



5\. Instal dependensi:



&#x20;  ```bash

&#x20;  pip install -r requirements.txt

&#x20;  ```



6\. Buat file `.env` di folder utama dan isi variabel `DATABASE\_URL` dengan connection string PostgreSQL milik sendiri. Jangan mengunggah file `.env` ke GitHub.



7\. Jalankan API:



&#x20;  ```bash

&#x20;  uvicorn api.index:app --reload

&#x20;  ```



8\. Buka dokumentasi API:



&#x20;  `http://127.0.0.1:8000/docs`



\## 7. Hasil Pengujian



Pengujian dilakukan menggunakan Swagger UI pada deployment Vercel.



Hasil pengujian yang dilaporkan:



\- GET berhasil dengan respons `200 OK`.

\- POST `/tugas` berhasil dengan respons `201 Created`.

\- GET detail tugas berhasil dengan respons `200 OK`.

\- PUT `/tugas/{id\_tugas}` berhasil dengan respons `200 OK`.

\- PATCH `/tugas/{id\_tugas}` berhasil dengan respons `200 OK`.

\- DELETE `/tugas/{id\_tugas}` berhasil dengan respons `200 OK`.



\## 8. Kesimpulan



Sistem Pengelolaan Tugas API telah dibuat menggunakan FastAPI dan PostgreSQL dengan lima tabel yang saling berelasi. API telah di-deploy ke Vercel dan pengujian endpoint dilakukan melalui Swagger UI. Operasi CRUD pada endpoint tugas berhasil diuji.





