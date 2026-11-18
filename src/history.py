"""Penyimpanan dan pengambilan riwayat diagnosa (fungsi murni tanpa Streamlit)."""

import json
from datetime import datetime


def simpan_riwayat(conn, nama_pemain, input_cf, hasil):
    """Simpan satu hasil diagnosa ke tabel riwayat; kembalikan id baru."""
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    kursor = conn.execute(
        "INSERT INTO riwayat (waktu, nama_pemain, input_json, hasil_json) "
        "VALUES (?, ?, ?, ?)",
        (
            waktu,
            (nama_pemain or "").strip(),
            json.dumps(input_cf, ensure_ascii=False),
            json.dumps(hasil, ensure_ascii=False),
        ),
    )
    return kursor.lastrowid


def get_riwayat(conn):
    """Ambil seluruh riwayat (terbaru lebih dulu) dengan JSON yang sudah di-parse."""
    baris = conn.execute("SELECT * FROM riwayat ORDER BY id DESC").fetchall()
    return [_parse(dict(item)) for item in baris]


def get_riwayat_by_id(conn, riwayat_id):
    """Ambil satu riwayat berdasarkan id, atau None bila tidak ada."""
    baris = conn.execute(
        "SELECT * FROM riwayat WHERE id = ?", (riwayat_id,)
    ).fetchone()
    return _parse(dict(baris)) if baris else None


def hapus_riwayat(conn, riwayat_id):
    """Hapus satu riwayat berdasarkan id."""
    conn.execute("DELETE FROM riwayat WHERE id = ?", (riwayat_id,))


def hapus_semua_riwayat(conn):
    """Hapus seluruh riwayat."""
    conn.execute("DELETE FROM riwayat")


def _parse(data):
    data["input"] = json.loads(data["input_json"])
    data["hasil"] = json.loads(data["hasil_json"])
    return data
