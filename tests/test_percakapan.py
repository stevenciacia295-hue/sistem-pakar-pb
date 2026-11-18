"""Tes materi percakapan PB-Bot (sapaan, respons, penutup, pertanyaan)."""

import random

from src import knowledge, percakapan
from src.db import get_connection, init_db


def _kode_gejala():
    conn = get_connection(":memory:")
    init_db(conn)
    knowledge.seed_if_empty(conn)
    return [g["kode"] for g in knowledge.get_gejala(conn)]


def test_setiap_gejala_di_database_punya_lima_varian_pertanyaan():
    kode_gejala = _kode_gejala()
    assert len(kode_gejala) == 13
    assert sorted(percakapan.PERTANYAAN) == sorted(kode_gejala)
    for kode in kode_gejala:
        varian = percakapan.PERTANYAAN[kode]
        assert len(varian) == 5
        assert all(isinstance(tanya, str) and tanya.strip() for tanya in varian)
        assert len(set(varian)) == 5


def test_pertanyaan_dimuat_dari_berkas_json():
    assert percakapan.DATA_PERTANYAAN.exists()
    assert percakapan.muat_pertanyaan() == percakapan.PERTANYAAN


def test_pilihan_jawaban_hanya_iya_dan_tidak():
    assert percakapan.PILIHAN_JAWABAN == [
        ("Iya", 1.0),
        ("Tidak", 0.0),
    ]


def test_pembuka_respons_penutup_tidak_kosong():
    assert len(percakapan.PEMBUKA) >= 3
    assert len(percakapan.RESPONS) >= 3
    assert len(percakapan.PENUTUP) >= 3
    for daftar in (percakapan.PEMBUKA, percakapan.RESPONS, percakapan.PENUTUP):
        assert all(isinstance(teks, str) and teks.strip() for teks in daftar)


def test_ambil_kalimat_berasal_dari_daftar():
    rng = random.Random(7)
    assert percakapan.ambil_pembuka(rng) in percakapan.PEMBUKA
    assert percakapan.ambil_respons(rng) in percakapan.RESPONS
    assert percakapan.ambil_penutup(rng) in percakapan.PENUTUP


def test_ambil_pertanyaan_memilih_salah_satu_varian():
    rng = random.Random(3)
    for kode, varian in percakapan.PERTANYAAN.items():
        assert percakapan.ambil_pertanyaan(kode, rng) in varian


def test_kode_gejala_tidak_dikenal_memakai_pertanyaan_umum():
    teks = percakapan.ambil_pertanyaan("G99")
    assert "G99" in teks
