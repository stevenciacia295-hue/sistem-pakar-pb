"""Koneksi dan inisialisasi database SQLite."""

import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = str(Path("data") / "pbexpert.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS cheat (
    kode      TEXT PRIMARY KEY,
    nama      TEXT NOT NULL,
    deskripsi TEXT NOT NULL DEFAULT '',
    saran     TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS gejala (
    kode      TEXT PRIMARY KEY,
    deskripsi TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS aturan (
    kode              TEXT PRIMARY KEY,
    kode_cheat        TEXT NOT NULL REFERENCES cheat(kode) ON DELETE CASCADE,
    kode_gejala       TEXT NOT NULL REFERENCES gejala(kode) ON DELETE CASCADE,
    cf_pakar          REAL NOT NULL CHECK (cf_pakar >= 0 AND cf_pakar <= 1),
    nama_pakar        TEXT NOT NULL DEFAULT 'Belum diisi',
    tanggal_wawancara TEXT NOT NULL DEFAULT 'Belum diisi'
);

CREATE TABLE IF NOT EXISTS riwayat (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    waktu       TEXT NOT NULL,
    nama_pemain TEXT,
    input_json  TEXT NOT NULL,
    hasil_json  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sumber (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    jenis   TEXT NOT NULL CHECK (jenis IN ('jurnal', 'pakar', 'praktisi')),
    sitasi  TEXT NOT NULL UNIQUE,
    url_doi TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS aturan_sumber (
    kode_aturan TEXT NOT NULL REFERENCES aturan(kode) ON DELETE CASCADE,
    id_sumber   INTEGER NOT NULL REFERENCES sumber(id) ON DELETE CASCADE,
    PRIMARY KEY (kode_aturan, id_sumber)
);

CREATE TABLE IF NOT EXISTS penilaian_pakar (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    waktu             TEXT NOT NULL,
    nama              TEXT NOT NULL,
    peran             TEXT NOT NULL,
    lama_bermain      TEXT NOT NULL,
    rank              TEXT NOT NULL DEFAULT '',
    izin_nama         TEXT NOT NULL,
    pengalaman_ciri   TEXT NOT NULL,
    pengalaman_beda   TEXT NOT NULL,
    pengalaman_mitos  TEXT NOT NULL,
    pengalaman_bukti  TEXT NOT NULL,
    penilaian_json    TEXT NOT NULL,
    ciri_lain         TEXT NOT NULL DEFAULT '',
    cheat_lain        TEXT NOT NULL DEFAULT '',
    boleh_dihubungi   TEXT NOT NULL,
    id_sumber         INTEGER REFERENCES sumber(id) ON DELETE SET NULL
);
"""


def get_connection(db_path=DEFAULT_DB_PATH):
    """Buka koneksi SQLite. Gunakan ':memory:' untuk pengujian tanpa file."""
    if db_path != ":memory:":
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn):
    """Buat seluruh tabel bila belum ada, lalu migrasi kolom aturan. Idempoten."""
    conn.executescript(SCHEMA)
    _migrasi_aturan(conn)


def _migrasi_aturan(conn):
    """Tambahkan kolom pakar pada tabel aturan lama tanpa menghapus data."""
    kolom = {baris[1] for baris in conn.execute("PRAGMA table_info(aturan)")}
    if "nama_pakar" not in kolom:
        conn.execute(
            "ALTER TABLE aturan ADD COLUMN nama_pakar TEXT NOT NULL "
            "DEFAULT 'Belum diisi'"
        )
    if "tanggal_wawancara" not in kolom:
        conn.execute(
            "ALTER TABLE aturan ADD COLUMN tanggal_wawancara TEXT NOT NULL "
            "DEFAULT 'Belum diisi'"
        )
