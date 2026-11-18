"""Tes panduan gejala: cakupan, isi, pertanyaan, dan pilihan jawaban."""

from src import knowledge, panduan, percakapan
from src.db import get_connection, init_db


def _kode_gejala():
    conn = get_connection(":memory:")
    init_db(conn)
    knowledge.seed_if_empty(conn)
    return [g["kode"] for g in knowledge.get_gejala(conn)]


def test_semua_gejala_database_punya_panduan_lengkap():
    kode = _kode_gejala()
    assert len(kode) == 13
    assert set(kode) == set(panduan.PANDUAN_GEJALA)
    for kode_gejala in kode:
        isi = panduan.get_panduan(kode_gejala)
        assert isi["apa"].strip()
        assert isi["mengapa"].strip()
        assert len(isi["solusi"]) >= 3
        assert all(langkah.strip() for langkah in isi["solusi"])


def test_setiap_gejala_punya_lima_varian_pertanyaan():
    for kode in panduan.PANDUAN_GEJALA:
        varian = percakapan.PERTANYAAN.get(kode)
        assert varian, kode
        assert len(varian) == 5
        assert all(teks.strip() for teks in varian)


def test_pilihan_jawaban_hanya_iya_dan_tidak():
    pilihan = dict(percakapan.PILIHAN_JAWABAN)
    assert pilihan == {"Iya": 1.0, "Tidak": 0.0}


def test_kode_tidak_dikenal_memakai_panduan_umum():
    assert panduan.get_panduan("G99") == panduan.PANDUAN_UMUM
    assert "bukan bukti pasti" in panduan.CATATAN
