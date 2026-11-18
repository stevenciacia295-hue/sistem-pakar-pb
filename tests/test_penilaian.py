"""Tes formulir penilaian pakar: skala, validasi, sumber, dan ringkasan."""

import pytest

from src import knowledge, penilaian
from src.db import get_connection, init_db


def _conn():
    conn = get_connection(":memory:")
    init_db(conn)
    knowledge.seed_if_empty(conn)
    return conn


def _data(nama="Steven Cia", izin_nama="Ya", nilai_r01=1.0, nilai_r13=None):
    nilai = {kode: None for kode in penilaian.KODE_ATURAN_FORM}
    nilai["R01"] = nilai_r01
    nilai["R13"] = nilai_r13
    return {
        "nama": nama,
        "peran": "Pemain senior/ranked tinggi",
        "lama_bermain": "5-8 tahun",
        "rank": "Grandmaster",
        "izin_nama": izin_nama,
        "pengalaman_ciri": "Gerakan bidik tidak wajar.",
        "pengalaman_beda": "Pemain jago konsisten dengan usaha manual.",
        "pengalaman_mitos": "Headshot tinggi sesekali.",
        "pengalaman_bukti": "Rekaman layar dan replay.",
        "penilaian": nilai,
        "ciri_lain": "Gerakan kamera patah-patah.",
        "cheat_lain": "Macro.",
        "boleh_dihubungi": "Ya",
    }


def test_skala_penilaian_sesuai_form():
    assert penilaian.LABEL_SKALA == [
        "Tidak tahu",
        "Tidak yakin",
        "Kurang yakin",
        "Cukup yakin",
        "Yakin",
        "Sangat yakin",
    ]
    assert [nilai for _label, nilai in penilaian.SKALA_PENILAIAN] == [
        None,
        0.2,
        0.4,
        0.6,
        0.8,
        1.0,
    ]
    assert len(penilaian.ATURAN_FORM) == 13


def test_simpan_penilaian_membuat_sumber_pakar_dan_tautan():
    conn = _conn()
    id_penilaian = penilaian.simpan_penilaian(conn, _data())
    assert id_penilaian > 0

    tersimpan = penilaian.get_penilaian_by_id(conn, id_penilaian)
    assert tersimpan["nama_tampil"] == "Steven Cia"
    assert tersimpan["penilaian"]["R01"] == 1.0
    assert tersimpan["penilaian"]["R13"] is None
    assert tersimpan["id_sumber"] is not None

    sumber = next(
        s for s in knowledge.get_sumber(conn) if s["id"] == tersimpan["id_sumber"]
    )
    assert sumber["jenis"] == "pakar"
    assert "Penilaian pakar" in sumber["sitasi"]
    assert "Steven Cia" in sumber["sitasi"]

    peta = knowledge.peta_sumber_aturan(conn)
    assert any(
        "Penilaian pakar" in s["sitasi"] for s in peta["R01"]
    )
    assert not any(
        "Penilaian pakar" in s["sitasi"] for s in peta["R13"]
    )


def test_izin_inisial_menyembunyikan_nama_lengkap():
    conn = _conn()
    id_penilaian = penilaian.simpan_penilaian(
        conn, _data(nama="Steven Cia", izin_nama="Hanya inisial")
    )
    tersimpan = penilaian.get_penilaian_by_id(conn, id_penilaian)
    assert tersimpan["nama_tampil"] == "S.C."
    sumber = next(
        s for s in knowledge.get_sumber(conn) if s["id"] == tersimpan["id_sumber"]
    )
    assert "S.C." in sumber["sitasi"]
    assert "Steven Cia" not in sumber["sitasi"]


def test_validasi_kolom_wajib_dan_skala():
    conn = _conn()

    data = _data()
    data["nama"] = "   "
    with pytest.raises(ValueError, match="Nama lengkap wajib diisi"):
        penilaian.simpan_penilaian(conn, data)

    data = _data()
    data["pengalaman_bukti"] = ""
    with pytest.raises(ValueError, match="Bukti yang biasa dipakai wajib diisi"):
        penilaian.simpan_penilaian(conn, data)

    data = _data()
    data["peran"] = "Pemain kasual"
    with pytest.raises(ValueError, match="Pilihan peran tidak dikenali"):
        penilaian.simpan_penilaian(conn, data)

    data = _data(nilai_r01=None)
    with pytest.raises(ValueError, match="Isi minimal satu penilaian"):
        penilaian.simpan_penilaian(conn, data)

    data = _data()
    data["penilaian"]["R02"] = 0.5
    with pytest.raises(ValueError, match="Nilai penilaian R02 tidak dikenali"):
        penilaian.simpan_penilaian(conn, data)


def test_ringkasan_rata_rata_mengabaikan_tidak_tahu():
    conn = _conn()
    penilaian.simpan_penilaian(conn, _data(nilai_r01=1.0))
    penilaian.simpan_penilaian(conn, _data(nilai_r01=0.6))

    ringkasan = {item["kode"]: item for item in penilaian.ringkasan_cf(conn)}
    assert ringkasan["R01"]["jumlah"] == 2
    assert ringkasan["R01"]["rata_rata"] == pytest.approx(0.8)
    assert ringkasan["R02"]["jumlah"] == 0
    assert ringkasan["R02"]["rata_rata"] is None


def test_hapus_penilaian_menghapus_sumber_pakarnya():
    conn = _conn()
    id_penilaian = penilaian.simpan_penilaian(conn, _data())
    tersimpan = penilaian.get_penilaian_by_id(conn, id_penilaian)
    id_sumber = tersimpan["id_sumber"]

    penilaian.hapus_penilaian(conn, id_penilaian)

    assert penilaian.get_penilaian_by_id(conn, id_penilaian) is None
    assert all(s["id"] != id_sumber for s in knowledge.get_sumber(conn))
    peta = knowledge.peta_sumber_aturan(conn)
    assert not any(
        "Penilaian pakar" in s["sitasi"] for s in peta["R01"]
    )
    with pytest.raises(ValueError, match="Penilaian tidak ditemukan"):
        penilaian.hapus_penilaian(conn, id_penilaian)


def test_label_nilai_skala():
    assert penilaian.label_nilai(None) == "Tidak tahu"
    assert penilaian.label_nilai(0.2) == "Tidak yakin"
    assert penilaian.label_nilai(0.8) == "Yakin"
    assert penilaian.label_nilai(0.55) == "Tidak tahu"
