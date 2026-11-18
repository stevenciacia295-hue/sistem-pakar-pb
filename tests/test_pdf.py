"""Tes pembuatan laporan PDF (hasil, riwayat, referensi, pengujian)."""

from src import explain, history, knowledge, laporan_pdf
from src.db import get_connection, init_db
from src.engine import diagnose


def _siapkan():
    conn = get_connection(":memory:")
    init_db(conn)
    knowledge.seed_if_empty(conn)
    return conn


def _data():
    conn = _siapkan()
    peta_gejala = {g["kode"]: g["deskripsi"] for g in knowledge.get_gejala(conn)}
    peta_sumber = knowledge.peta_sumber_aturan(conn)
    aturan = knowledge.get_aturan(conn)
    cheat = knowledge.get_cheats(conn)
    gejala = knowledge.get_gejala(conn)
    return conn, peta_gejala, peta_sumber, aturan, cheat, gejala


def _pdf_valid(data):
    assert isinstance(data, bytes)
    assert data.startswith(b"%PDF")
    assert b"%%EOF" in data
    assert len(data) > 1500


def test_pdf_hasil_diagnosa():
    _conn, peta_gejala, peta_sumber, aturan, cheat, gejala = _data()
    hasil = diagnose({"G02": 1.0, "G01": 0.8}, aturan, cheat, gejala)
    hasil, _ = explain.rapikan_hasil(hasil)

    data, nama = laporan_pdf.buat_pdf_hasil(
        "Budi 42", {"G01": 0.8, "G02": 1.0}, hasil, peta_gejala, peta_sumber
    )

    _pdf_valid(data)
    assert nama == "hasil_diagnosa_Budi_42.pdf"


def test_pdf_hasil_tanpa_kesimpulan_dan_nama_aneh():
    _conn, peta_gejala, peta_sumber = _data()[:3]
    data, nama = laporan_pdf.buat_pdf_hasil(
        "Pemain — Uji \u2264 3", {}, [], peta_gejala, peta_sumber
    )

    _pdf_valid(data)
    assert nama == "hasil_diagnosa_Pemain_Uji_3.pdf"


def test_pdf_hasil_dengan_peringatan_inkonsisten():
    _conn, peta_gejala, peta_sumber, aturan, cheat, gejala = _data()
    hasil = diagnose(
        {
            "G01": 1.0,
            "G02": 1.0,
            "G05": 1.0,
            "G07": 1.0,
            "G08": 1.0,
            "G09": 1.0,
        },
        aturan,
        cheat,
        gejala,
    )
    hasil, peringatan = explain.rapikan_hasil(hasil)
    assert peringatan is True

    data, _nama = laporan_pdf.buat_pdf_hasil(
        "Budi",
        {"G01": 1.0},
        hasil,
        peta_gejala,
        peta_sumber,
        peringatan=peringatan,
    )
    _pdf_valid(data)


def test_pdf_riwayat_tersimpan():
    conn, peta_gejala, peta_sumber, aturan, cheat, gejala = _data()
    hasil = diagnose({"G12": 1.0, "G13": 1.0}, aturan, cheat, gejala)
    hasil, _ = explain.rapikan_hasil(hasil)
    history.simpan_riwayat(conn, "Budi", {"G12": 1.0, "G13": 1.0}, hasil)
    detail = history.get_riwayat(conn)[0]

    data, nama = laporan_pdf.buat_pdf_riwayat(detail, peta_gejala, peta_sumber)

    _pdf_valid(data)
    assert nama == f"riwayat_{detail['id']}.pdf"


def test_pdf_referensi_seluruh_aturan():
    conn, peta_gejala, _peta, _aturan, _cheat, _gejala = _data()
    peta_sumber = knowledge.peta_sumber_aturan(conn)
    peta_cheat = {c["kode"]: c["nama"] for c in knowledge.get_cheats(conn)}
    baris = [
        {
            "Kode": a["kode"],
            "Cheat": peta_cheat.get(a["kode_cheat"], a["kode_cheat"]),
            "Gejala": peta_gejala.get(a["kode_gejala"], a["kode_gejala"]),
            "CF pakar": f"{a['cf_pakar']:.2f}",
            "Nama pakar": a["nama_pakar"],
            "Tanggal wawancara": a["tanggal_wawancara"],
            "Jenis sumber": ", ".join(
                {s["jenis"] for s in peta_sumber.get(a["kode"], [])}
            )
            or "-",
            "Sumber": explain.teks_sumber(peta_sumber.get(a["kode"], [])),
        }
        for a in knowledge.get_aturan(conn)
    ]

    data, nama = laporan_pdf.buat_pdf_referensi(baris)

    _pdf_valid(data)
    assert nama == "referensi_aturan.pdf"


def test_pdf_pengujian():
    baris = [
        {
            "ID": "S01",
            "Skenario": "Aimbot dari G01 dan G02",
            "Input gejala": "G01=0.8, G02=1.0",
            "Diharapkan": "Aimbot 95.6%",
            "Hasil sistem": "Aimbot 95.6%",
            "Status": "LULUS",
            "Langkah perhitungan manual": "R01: 0.8 x 0.7 = 0.56. R02: 1.0 x 0.9 = 0.90. Gabungan 95.6%.",
        },
        {
            "ID": "S02",
            "Skenario": "Tanpa gejala",
            "Input gejala": "Tidak ada",
            "Diharapkan": "Tidak ada",
            "Hasil sistem": "Tidak ada",
            "Status": "LULUS",
            "Langkah perhitungan manual": "Tidak ada aturan terpicu.",
        },
    ]

    data, nama = laporan_pdf.buat_pdf_pengujian(baris)

    _pdf_valid(data)
    assert nama == "hasil_pengujian.pdf"


def test_nama_berkas_aman():
    assert laporan_pdf.nama_berkas("Budi 42!!", "x") == "Budi_42"
    assert laporan_pdf.nama_berkas("   ", "laporan") == "laporan"
    assert laporan_pdf.nama_berkas(None, "laporan") == "laporan"
