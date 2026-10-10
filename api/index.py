
import os
from datetime import date, datetime
from decimal import Decimal

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(
    title="Sistem Pengelolaan Tugas",
    description="REST API untuk mengelola tugas mahasiswa",
    version="1.0.0",
)



def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg.connect(
            database_url,
            row_factory=dict_row,
            connect_timeout=10,
        )

    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5433")),
        dbname=os.getenv("DB_NAME", "sistem_pengelolaan_tugas"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        row_factory=dict_row,
        connect_timeout=5,
    )


class TugasCreate(BaseModel):
    id_mahasiswa: int = Field(gt=0)
    id_mata_kuliah: int = Field(gt=0)
    id_status: int = Field(gt=0)
    nama_tugas: str = Field(min_length=1, max_length=255)
    deskripsi: str | None = None
    tanggal_diberikan: date
    deadline: date


class TugasUpdate(BaseModel):
    id_mahasiswa: int | None = Field(default=None, gt=0)
    id_mata_kuliah: int | None = Field(default=None, gt=0)
    id_status: int | None = Field(default=None, gt=0)
    nama_tugas: str | None = Field(
        default=None, min_length=1, max_length=255
    )
    deskripsi: str | None = None
    tanggal_diberikan: date | None = None
    deadline: date | None = None


def fetch_all(query, params=()):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


def fetch_one(query, params=()):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()


@app.get("/")
def home():
    return {
        "message": "API Sistem Pengelolaan Tugas aktif",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    try:
        fetch_one("SELECT 1 AS status")
        return {"status": "ok", "database": "connected"}
    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="Database tidak dapat diakses",
        )


@app.get("/mahasiswa")
def list_mahasiswa():
    try:
        return fetch_all(
            "SELECT id_mahasiswa, nim, nama_mahasiswa, email "
            "FROM mahasiswa ORDER BY id_mahasiswa"
        )
    except psycopg.Error:
        raise HTTPException(500, "Gagal mengambil data mahasiswa")


@app.get("/mata-kuliah")
def list_mata_kuliah():
    try:
        return fetch_all(
            "SELECT id_mata_kuliah, kode_mata_kuliah, "
            "nama_mata_kuliah, sks FROM mata_kuliah "
            "ORDER BY id_mata_kuliah"
        )
    except psycopg.Error:
        raise HTTPException(500, "Gagal mengambil data mata kuliah")


@app.get("/status-tugas")
def list_status_tugas():
    try:
        return fetch_all(
            "SELECT id_status, nama_status FROM status_tugas "
            "ORDER BY id_status"
        )
    except psycopg.Error:
        raise HTTPException(500, "Gagal mengambil status tugas")


@app.get("/pengumpulan-tugas")
def list_pengumpulan_tugas():
    try:
        return fetch_all(
            "SELECT id_pengumpulan, id_tugas, tanggal_pengumpulan, "
            "link_file, catatan FROM pengumpulan_tugas "
            "ORDER BY id_pengumpulan"
        )
    except psycopg.Error:
        raise HTTPException(500, "Gagal mengambil data pengumpulan")


@app.get("/tugas")
def list_tugas():
    try:
        return fetch_all(
            """
            SELECT t.*, m.nama_mahasiswa,
                   mk.nama_mata_kuliah, s.nama_status
            FROM tugas t
            JOIN mahasiswa m ON m.id_mahasiswa = t.id_mahasiswa
            JOIN mata_kuliah mk
                ON mk.id_mata_kuliah = t.id_mata_kuliah
            JOIN status_tugas s ON s.id_status = t.id_status
            ORDER BY t.id_tugas
            """
        )
    except psycopg.Error:
        raise HTTPException(500, "Gagal mengambil data tugas")


@app.get("/tugas/{id_tugas}")
def detail_tugas(id_tugas: int):
    try:
        tugas = fetch_one(
            "SELECT * FROM tugas WHERE id_tugas = %s",
            (id_tugas,),
        )
        if tugas is None:
            raise HTTPException(404, "Tugas tidak ditemukan")
        return tugas
    except HTTPException:
        raise
    except psycopg.Error:
        raise HTTPException(500, "Gagal mengambil detail tugas")


@app.post("/tugas", status_code=201)
def create_tugas(data: TugasCreate):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO tugas (
                        id_mahasiswa, id_mata_kuliah, id_status,
                        nama_tugas, deskripsi,
                        tanggal_diberikan, deadline
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING *
                    """,
                    (
                        data.id_mahasiswa,
                        data.id_mata_kuliah,
                        data.id_status,
                        data.nama_tugas,
                        data.deskripsi,
                        data.tanggal_diberikan,
                        data.deadline,
                    ),
                )
                tugas = cur.fetchone()
        return {"message": "Tugas berhasil ditambahkan", "data": tugas}
    except psycopg.errors.ForeignKeyViolation:
        raise HTTPException(
            400, "ID mahasiswa, mata kuliah, atau status tidak valid"
        )
    except psycopg.Error:
        raise HTTPException(500, "Gagal menambahkan tugas")


@app.put("/tugas/{id_tugas}")
def replace_tugas(id_tugas: int, data: TugasCreate):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE tugas
                    SET id_mahasiswa = %s,
                        id_mata_kuliah = %s,
                        id_status = %s,
                        nama_tugas = %s,
                        deskripsi = %s,
                        tanggal_diberikan = %s,
                        deadline = %s
                    WHERE id_tugas = %s
                    RETURNING *
                    """,
                    (
                        data.id_mahasiswa,
                        data.id_mata_kuliah,
                        data.id_status,
                        data.nama_tugas,
                        data.deskripsi,
                        data.tanggal_diberikan,
                        data.deadline,
                        id_tugas,
                    ),
                )
                tugas = cur.fetchone()
        if tugas is None:
            raise HTTPException(404, "Tugas tidak ditemukan")
        return {"message": "Tugas berhasil diperbarui", "data": tugas}
    except HTTPException:
        raise
    except psycopg.errors.ForeignKeyViolation:
        raise HTTPException(400, "Referensi data tidak valid")
    except psycopg.Error:
        raise HTTPException(500, "Gagal memperbarui tugas")


@app.patch("/tugas/{id_tugas}")
def patch_tugas(id_tugas: int, data: TugasUpdate):
    perubahan = data.model_dump(exclude_unset=True)
    if not perubahan:
        raise HTTPException(400, "Tidak ada data yang diubah")

    kolom_diizinkan = {
        "id_mahasiswa", "id_mata_kuliah", "id_status",
        "nama_tugas", "deskripsi",
        "tanggal_diberikan", "deadline",
    }
    if not set(perubahan).issubset(kolom_diizinkan):
        raise HTTPException(400, "Kolom tidak diizinkan")

    set_clause = ", ".join(f"{kolom} = %s" for kolom in perubahan)
    values = list(perubahan.values()) + [id_tugas]

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"UPDATE tugas SET {set_clause} "
                    "WHERE id_tugas = %s RETURNING *",
                    values,
                )
                tugas = cur.fetchone()
        if tugas is None:
            raise HTTPException(404, "Tugas tidak ditemukan")
        return {"message": "Tugas berhasil diperbarui", "data": tugas}
    except HTTPException:
        raise
    except psycopg.errors.ForeignKeyViolation:
        raise HTTPException(400, "Referensi data tidak valid")
    except psycopg.Error:
        raise HTTPException(500, "Gagal memperbarui tugas")


@app.delete("/tugas/{id_tugas}")
def delete_tugas(id_tugas: int):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM tugas WHERE id_tugas = %s RETURNING id_tugas",
                    (id_tugas,),
                )
                tugas = cur.fetchone()
        if tugas is None:
            raise HTTPException(404, "Tugas tidak ditemukan")
        return {"message": "Tugas berhasil dihapus"}
    except HTTPException:
        raise
    except psycopg.errors.ForeignKeyViolation:
        raise HTTPException(
            409,
            "Tugas masih memiliki data pengumpulan dan tidak dapat dihapus",
        )
    except psycopg.Error:
        raise HTTPException(500, "Gagal menghapus tugas")
