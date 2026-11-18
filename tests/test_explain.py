"""Tes perapian label kategori hasil dan peringatan inkonsistensi."""

from src import explain, knowledge
from src.engine import diagnose


def _diagnosa(input_cf):
    return diagnose(
        input_cf,
        knowledge.ATURAN_AWAL,
        knowledge.CHEAT_AWAL,
        knowledge.GEJALA_AWAL,
    )


def test_label_sangat_mungkin_hanya_untuk_peringkat_teratas():
    hasil = _diagnosa({"G01": 1.0, "G02": 1.0, "G05": 1.0, "G07": 1.0})
    assert [item["kode_cheat"] for item in hasil] == ["C02", "C01"]
    dirapikan, peringatan = explain.rapikan_hasil(hasil)
    assert dirapikan[0]["kategori"] == "Sangat mungkin"
    assert dirapikan[1]["kategori"] == "Mungkin"
    assert peringatan is False


def test_peringatan_muncul_bila_tiga_cheat_atau_lebih_di_atas_80():
    hasil = _diagnosa(
        {
            "G01": 1.0,
            "G02": 1.0,
            "G05": 1.0,
            "G07": 1.0,
            "G08": 1.0,
            "G09": 1.0,
        }
    )
    dirapikan, peringatan = explain.rapikan_hasil(hasil)
    assert peringatan is True
    assert [item["kategori"] for item in dirapikan].count("Sangat mungkin") == 1


def test_tanpa_peringatan_untuk_dua_cheat_tinggi():
    hasil = _diagnosa({"G02": 1.0, "G07": 1.0})
    dirapikan, peringatan = explain.rapikan_hasil(hasil)
    assert len(dirapikan) == 2
    assert peringatan is False


def test_input_kosong_tidak_menghasilkan_peringatan():
    dirapikan, peringatan = explain.rapikan_hasil([])
    assert dirapikan == []
    assert peringatan is False


def test_hasil_di_bawah_80_tetap_memakai_kategori_engine():
    hasil = _diagnosa({"G01": 0.4})
    dirapikan, peringatan = explain.rapikan_hasil(hasil)
    assert dirapikan[0]["kategori"] == "Kemungkinan kecil"
    assert peringatan is False


def test_frasa_dan_judul_hasil():
    hasil = _diagnosa({"G02": 1.0, "G01": 0.8})
    assert explain.frasa_kategori(hasil[0]) == "kemungkinan besar"
    assert explain.judul_hasil(hasil[0]) == "Kemungkinan besar memakai Aimbot (95.6%)"


def test_arti_hasil_memakai_deskripsi_cheat():
    hasil = _diagnosa({"G02": 1.0})
    teks = explain.arti_hasil(hasil[0])
    assert teks.startswith("Artinya: dari pengamatanmu")
    assert "memakai Aimbot" in teks
    assert "mengarahkan tembakan secara otomatis" in teks


def test_label_jawaban_hanya_iya_atau_tidak():
    assert explain.label_jawaban(1.0) == "iya"
    assert explain.label_jawaban(0.8) == "iya"
    assert explain.label_jawaban(0.0) == "tidak"


def test_alasan_hasil_memuat_deskripsi_dan_label_jawaban():
    hasil = _diagnosa({"G02": 1.0, "G01": 0.8})
    assert explain.alasan_hasil(hasil[0]) == [
        "Headshot rate sangat tinggi dan konsisten (kamu: iya)",
        "Crosshair langsung mengunci kepala (kamu: iya)",
    ]


def test_sumber_terpicu_unik_dan_berurutan():
    item = {
        "aturan_terpicu": [
            {"kode_aturan": "R01"},
            {"kode_aturan": "R02"},
        ]
    }
    peta = {
        "R01": [{"id": 1}, {"id": 2}],
        "R02": [{"id": 2}, {"id": 3}],
    }
    assert [s["id"] for s in explain.sumber_terpicu(item, peta)] == [1, 2, 3]
    assert explain.sumber_terpicu(item) == []
