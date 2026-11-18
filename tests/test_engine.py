"""Tes mesin inferensi forward chaining dan certainty factor."""

import pytest

from src import knowledge
from src.engine import SKALA_KEYAKINAN, diagnose, gabung_cf, kategori_keyakinan


def _semua_menurun(hasil):
    persen = [item["persen"] for item in hasil]
    return persen == sorted(persen, reverse=True)


def test_uji_wajib_aimbot_95_6_persen():
    hasil = diagnose(
        {"G02": 1.0, "G01": 0.8},
        knowledge.ATURAN_AWAL,
        knowledge.CHEAT_AWAL,
    )
    assert len(hasil) == 1
    assert hasil[0]["kode_cheat"] == "C01"
    assert hasil[0]["nama"] == "Aimbot"
    assert hasil[0]["persen"] == pytest.approx(95.6)
    assert hasil[0]["kategori"] == "Sangat mungkin"


def test_uji_wajib_input_kosong():
    assert diagnose({}, knowledge.ATURAN_AWAL, knowledge.CHEAT_AWAL) == []


def test_input_tanpa_aturan_terkait_menghasilkan_list_kosong():
    assert diagnose({"G99": 1.0}, knowledge.ATURAN_AWAL, knowledge.CHEAT_AWAL) == []


def test_gejala_tidak_dikenal_diabaikan():
    hasil = diagnose(
        {"G02": 1.0, "GXX": 1.0},
        knowledge.ATURAN_AWAL,
        knowledge.CHEAT_AWAL,
    )
    assert len(hasil) == 1
    assert hasil[0]["kode_cheat"] == "C01"


def test_skala_keyakinan_sesuai_spesifikasi():
    assert [item["nilai"] for item in SKALA_KEYAKINAN] == [0.2, 0.4, 0.6, 0.8, 1.0]
    assert [item["label"] for item in SKALA_KEYAKINAN] == [
        "Tidak yakin",
        "Kurang yakin",
        "Cukup yakin",
        "Yakin",
        "Sangat yakin",
    ]


def test_rumus_gabung_cf():
    assert gabung_cf(0.0, 0.9) == pytest.approx(0.9)
    assert gabung_cf(0.9, 0.56) == pytest.approx(0.956)


def test_kategori_batas():
    assert kategori_keyakinan(1.0) == "Sangat mungkin"
    assert kategori_keyakinan(0.8) == "Sangat mungkin"
    assert kategori_keyakinan(0.79) == "Mungkin"
    assert kategori_keyakinan(0.5) == "Mungkin"
    assert kategori_keyakinan(0.49) == "Kemungkinan kecil"


def test_rincian_aturan_terpicu():
    hasil = diagnose(
        {"G02": 1.0, "G01": 0.8},
        knowledge.ATURAN_AWAL,
        knowledge.CHEAT_AWAL,
    )
    langkah = hasil[0]["aturan_terpicu"]
    assert [baris["kode_aturan"] for baris in langkah] == ["R01", "R02"]
    assert langkah[0]["cf_user"] == pytest.approx(0.8)
    assert langkah[0]["cf_pakar"] == pytest.approx(0.7)
    assert langkah[0]["cf_aturan"] == pytest.approx(0.56)
    assert langkah[1]["cf_aturan"] == pytest.approx(0.9)
    assert langkah[1]["cf_gabungan"] == pytest.approx(0.956)


def test_ranking_urut_menurun_dan_multi_cheat():
    hasil = diagnose(
        {"G07": 1.0, "G11": 1.0, "G01": 1.0},
        knowledge.ATURAN_AWAL,
        knowledge.CHEAT_AWAL,
    )
    assert [item["kode_cheat"] for item in hasil] == ["C02", "C04", "C01"]
    assert hasil[0]["persen"] == pytest.approx(90.0)
    assert hasil[1]["persen"] == pytest.approx(90.0)
    assert hasil[2]["persen"] == pytest.approx(70.0)
    assert _semua_menurun(hasil)


def test_no_recoil_diperkuat_gejala_gerak_dan_hentakan():
    hasil = diagnose(
        {"G12": 1.0, "G13": 1.0},
        knowledge.ATURAN_AWAL,
        knowledge.CHEAT_AWAL,
    )
    assert len(hasil) == 1
    assert hasil[0]["kode_cheat"] == "C03"
    assert hasil[0]["persen"] == pytest.approx(94.0)
    assert [baris["kode_aturan"] for baris in hasil[0]["aturan_terpicu"]] == [
        "R12",
        "R13",
    ]


def test_persen_tidak_melebihi_100():
    hasil = diagnose(
        {kode: 1.0 for kode in ("G01", "G02", "G03", "G04")},
        knowledge.ATURAN_AWAL,
        knowledge.CHEAT_AWAL,
    )
    assert len(hasil) == 1
    assert hasil[0]["kode_cheat"] == "C01"
    assert hasil[0]["persen"] <= 100.0
    assert 0.0 < hasil[0]["cf_gabungan"] <= 1.0
