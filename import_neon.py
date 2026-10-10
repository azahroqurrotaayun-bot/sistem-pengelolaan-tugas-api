
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise SystemExit("DATABASE_URL tidak ditemukan di file .env")

sql_file = os.path.join(
    os.path.expanduser("~"),
    "Documents",
    "sistem_pengelolaan_tugas_neon.sql",
)

if not os.path.isfile(sql_file):
    raise SystemExit(f"File SQL tidak ditemukan: {sql_file}")

print("Memulai impor database ke Neon...")


result = subprocess.run(
    [
        r"C:\Program Files\PostgreSQL\15\bin\psql.exe",
        "-X",
        "-v",
        "ON_ERROR_STOP=1",
        "-f",
        sql_file,
        database_url,
    ],
    check=False,
)

if result.returncode == 0:
    print("Impor selesai!")
else:
    print("Impor gagal. Periksa pesan kesalahan di atas.")
    raise SystemExit(result.returncode)
