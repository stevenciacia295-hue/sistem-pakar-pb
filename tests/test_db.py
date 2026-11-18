"""Tes migrasi skema, data No Recoil baru, dan pengelolaan sumber pengetahuan."""

import pytest

from src import knowledge
from src.db import get_connection, init_db


def _siapkan():
    conn = get_connection(":memory:")
    init_db(conn)
    knowledge.seed_if_empty(conn)
    return conn


def test_migrasi_kolom_pakar_pada_tabel_aturan_lama():
    conn = get_connection(":memory:")
    conn.executescript(
        "CREATE TABLE aturan ("
        "kode TEXT PRIMARY KEY, "
        "kode_cheat TEXT NOT NULL, "
        "kode_gejala TEXT NOT NULL, "
        "cf_pakar REAL NOT NULL"
        ");"
    )
    init_db(conn)
    kolom = {baris[1] for baris in conn.execute("PRAGMA table_info(aturan)")}
    assert {"nama_pakar", "tanggal_wawancara"} <= kolom

    knowledge.seed_if_empty(conn)
    aturan = knowledge.get_aturan(conn)
    assert len(aturan) == 13
    assert aturan[0]["nama_pakar"] == "Belum diisi"
    assert aturan[0]["tanggal_wawancara"] == "Belum diisi"


def test_tabel_sumber_dan_tautan_dibuat():
    conn = _siapkan()
    tabel = {
        baris[0]
        for baris in conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    assert {"sumber", "aturan_sumber"} <= tabel
    kolom_sumber = {baris[1] for baris in conn.execute("PRAGMA table_info(sumber)")}
    assert kolom_sumber == {"id", "jenis", "sitasi", "url_doi"}


def test_gejala_dan_aturan_no_recoil_baru_tersedia():
    conn = _siapkan()
    gejala = {g["kode"]: g["deskripsi"] for g in knowledge.get_gejala(conn)}
    assert len(gejala) == 13
    assert "bergerak atau melompat" in gejala["G12"]
    assert "hentakan besar" in gejala["G13"]

    aturan = {a["kode"]: a for a in knowledge.get_aturan(conn)}
    assert aturan["R12"]["kode_cheat"] == "C03"
    assert aturan["R12"]["kode_gejala"] == "G12"
    assert aturan["R12"]["cf_pakar"] == pytest.approx(0.7)
    assert aturan["R13"]["kode_gejala"] == "G13"
    assert aturan["R13"]["cf_pakar"] == pytest.approx(0.8)


def test_seed_dan_migrasi_idempoten():
    conn = _siapkan()
    knowledge.seed_if_empty(conn)
    knowledge.seed_if_empty(conn)
    assert len(knowledge.get_cheats(conn)) == 4
    assert len(knowledge.get_gejala(conn)) == 13
    assert len(knowledge.get_aturan(conn)) == 13
    assert len(knowledge.get_sumber(conn)) == 5


def test_crud_menyimpan_sumber_pakar():
    conn = _siapkan()

    knowledge.update_aturan(
        conn, "R01", "C01", "G01", 0.7, "Pakar A", "2026-11-13"
    )
    aturan = {item["kode"]: item for item in knowledge.get_aturan(conn)}
    assert aturan["R01"]["nama_pakar"] == "Pakar A"
    assert aturan["R01"]["tanggal_wawancara"] == "2026-11-13"

    ringkasan = knowledge.ringkasan_pakar(conn)
    assert {"nama_pakar": "Pakar A", "jumlah": 1} in ringkasan


def test_seed_sumber_dan_tautan_awal():
    conn = _siapkan()
    sumber = knowledge.get_sumber(conn)
    assert len(sumber) == 5
    assert [s["jenis"] for s in sumber].count("jurnal") == 4
    assert [s["jenis"] for s in sumber].count("praktisi") == 1

    peta = knowledge.peta_sumber_aturan(conn)
    assert len(peta) == 13
    sitasi_r01 = " | ".join(s["sitasi"] for s in peta["R01"])
    assert "Yu" in sitasi_r01
    assert "Choi" in sitasi_r01
    assert "Yan & Randell (2005)" in sitasi_r01
    assert "Yan & Randell (2009)" in sitasi_r01

    assert {s["jenis"] for s in peta["R03"]} == {"jurnal", "praktisi"}
    praktisi_r13 = [s for s in peta["R13"] if s["jenis"] == "praktisi"]
    assert praktisi_r13
    assert "validasi pakar" in praktisi_r13[0]["sitasi"].lower()


def test_admin_dapat_mengelola_sumber_dan_tautannya():
    conn = _siapkan()
    knowledge.add_sumber(conn, "pakar", "Wawancara Pakar B, 2026", "https://contoh")
    baru = next(
        s for s in knowledge.get_sumber(conn) if s["sitasi"] == "Wawancara Pakar B, 2026"
    )

    knowledge.set_sumber_aturan(conn, "R01", [baru["id"]])
    assert [s["id"] for s in knowledge.get_sumber_aturan(conn, "R01")] == [baru["id"]]

    knowledge.update_sumber(
        conn, baru["id"], "jurnal", "Pakar B (2026). Validasi.", "10.0000/contoh"
    )
    ubah = next(s for s in knowledge.get_sumber(conn) if s["id"] == baru["id"])
    assert ubah["jenis"] == "jurnal"
    assert ubah["sitasi"] == "Pakar B (2026). Validasi."
    assert ubah["url_doi"] == "10.0000/contoh"

    knowledge.delete_sumber(conn, baru["id"])
    assert knowledge.get_sumber_aturan(conn, "R01") == []
    assert all(s["id"] != baru["id"] for s in knowledge.get_sumber(conn))


def test_validasi_sumber_menolak_jenis_asing_sitasi_kosong_dan_ganda():
    conn = _siapkan()
    with pytest.raises(ValueError):
        knowledge.add_sumber(conn, "blog", "Contoh sitasi", "")
    with pytest.raises(ValueError):
        knowledge.add_sumber(conn, "jurnal", "   ", "")
    sitasi = knowledge.get_sumber(conn)[0]["sitasi"]
    with pytest.raises(ValueError):
        knowledge.add_sumber(conn, "jurnal", sitasi, "")
    with pytest.raises(ValueError):
        knowledge.set_sumber_aturan(conn, "R01", [9999])
