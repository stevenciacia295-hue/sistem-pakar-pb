"""Pembuat laporan PDF sistem pakar (hasil diagnosa, riwayat, referensi, uji)."""

import re
from datetime import datetime
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src import explain

JUDUL_APLIKASI = "Sistem Pakar Deteksi Cheat Point Blank"
CATATAN_PRAKTISI = "Sumber berjenis praktisi masih perlu validasi pakar."

_GANTI_KARAKTER = {
    "\u2014": "-",
    "\u2013": "-",
    "\u00d7": "x",
    "\u2265": ">=",
    "\u2264": "<=",
    "\u201c": '"',
    "\u201d": '"',
    "\u2018": "'",
    "\u2019": "'",
    "\u2026": "...",
    "\u2022": "-",
}

_GAYA = {
    "judul": ParagraphStyle(
        "judul",
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        spaceAfter=1.5 * mm,
    ),
    "sub": ParagraphStyle(
        "sub",
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#555555"),
    ),
    "h2": ParagraphStyle(
        "h2",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceBefore=4 * mm,
        spaceAfter=2 * mm,
    ),
    "h3": ParagraphStyle(
        "h3",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        spaceBefore=2.5 * mm,
        spaceAfter=1 * mm,
    ),
    "isi": ParagraphStyle(
        "isi", fontName="Helvetica", fontSize=9, leading=12
    ),
    "kecil": ParagraphStyle(
        "kecil", fontName="Helvetica", fontSize=7.5, leading=10
    ),
    "seksi": ParagraphStyle(
        "seksi",
        fontName="Helvetica-Bold",
        fontSize=8.2,
        leading=10.5,
        spaceBefore=1.8 * mm,
        spaceAfter=0.8 * mm,
    ),
    "sel": ParagraphStyle(
        "sel", fontName="Helvetica", fontSize=7.2, leading=9
    ),
    "kepala": ParagraphStyle(
        "kepala",
        fontName="Helvetica-Bold",
        fontSize=7.2,
        leading=9,
        textColor=colors.white,
    ),
    "peringatan": ParagraphStyle(
        "peringatan",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        backColor=colors.HexColor("#eeeeee"),
        borderColor=colors.black,
        borderWidth=0.6,
        borderPadding=4,
        spaceBefore=2 * mm,
    ),
}


def nama_berkas(teks, bawaan="laporan"):
    """Ubah teks bebas menjadi bagian nama berkas yang aman."""
    bersih = re.sub(r"[^A-Za-z0-9_-]+", "_", str(teks or "")).strip("_")
    return bersih[:60] or bawaan


def _waktu_sekarang():
    return datetime.now().strftime("%d-%m-%Y %H:%M")


def _bersih(nilai):
    teks = "" if nilai is None else str(nilai)
    for asal, ganti in _GANTI_KARAKTER.items():
        teks = teks.replace(asal, ganti)
    return escape(teks)


def _p(teks, gaya="isi"):
    return Paragraph(_bersih(teks), _GAYA[gaya])


def _footer(canvas, doc):
    canvas.saveState()
    lebar, _tinggi = doc.pagesize
    canvas.setStrokeGray(0.7)
    canvas.line(doc.leftMargin, 12 * mm, lebar - doc.rightMargin, 12 * mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillGray(0.35)
    canvas.drawString(doc.leftMargin, 8 * mm, JUDUL_APLIKASI)
    canvas.drawRightString(
        lebar - doc.rightMargin, 8 * mm, f"Halaman {doc.page}"
    )
    canvas.restoreState()


def _dokumen(judul, subjek, halaman=A4):
    aliran = BytesIO()
    doc = SimpleDocTemplate(
        aliran,
        pagesize=halaman,
        leftMargin=17 * mm,
        rightMargin=17 * mm,
        topMargin=15 * mm,
        bottomMargin=18 * mm,
        title=judul,
        author=JUDUL_APLIKASI,
        subject=subjek,
    )
    return aliran, doc


def _tutup(aliran, doc, cerita):
    doc.build(cerita, onFirstPage=_footer, onLaterPages=_footer)
    return aliran.getvalue()


def _kepala(judul, keterangan):
    return [
        _p(judul, "judul"),
        _p(keterangan, "sub"),
        _p(f"Dicetak: {_waktu_sekarang()}", "sub"),
        Spacer(1, 3 * mm),
    ]


def _tabel(judul_kolom, isi, lebar):
    data = [
        [Paragraph(_bersih(teks), _GAYA["kepala"]) for teks in judul_kolom]
    ]
    for baris in isi:
        data.append([Paragraph(_bersih(teks), _GAYA["sel"]) for teks in baris])
    tabel = Table(data, colWidths=lebar, repeatRows=1)
    tabel.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#eeeeee")],
                ),
            ]
        )
    )
    return tabel


def _tabel_gejala(input_cf, peta_gejala):
    isi = [
        (
            kode,
            peta_gejala.get(kode, "deskripsi tidak ditemukan"),
            f"{float(nilai):.1f}",
        )
        for kode, nilai in input_cf.items()
    ]
    return _tabel(
        ["Kode", "Gejala", "Keyakinan pengguna"],
        isi,
        [20 * mm, 120 * mm, 36 * mm],
    )


def _cerita_hasil(hasil, peta_sumber=None, peringatan=False):
    cerita = [_p("Hasil analisis", "h2")]
    if peringatan:
        cerita.append(_p(explain.PERINGATAN_TIDAK_KONSISTEN, "peringatan"))
        cerita.append(Spacer(1, 2 * mm))
    if not hasil:
        cerita.append(
            _p(
                "Tidak ada jenis cheat yang dapat disimpulkan dari gejala "
                "yang dipilih."
            )
        )
        return cerita

    for item in hasil:
        blok = [_p(f"HASIL: {explain.judul_hasil(item)}", "h3")]
        blok.append(_p(explain.arti_hasil(item), "isi"))
        alasan = explain.alasan_hasil(item)
        if alasan:
            blok.append(_p("Kenapa sistem menyimpulkan ini:", "seksi"))
            for teks in alasan:
                blok.append(_p(f"- {teks}", "kecil"))
        blok.append(_p("Yang sebaiknya kamu lakukan:", "seksi"))
        saran = item.get("saran") or (
            "Rekam ulang pertandingan, bandingkan dengan pemain lain, lalu "
            "laporkan ke GM dengan bukti video."
        )
        blok.append(_p(saran, "kecil"))
        rincian = "<br/>".join(
            _bersih(baris)
            for baris in explain.penjelasan_perhitungan(item, peta_sumber)
        )
        if rincian:
            blok.append(_p("Rincian perhitungan:", "seksi"))
            blok.append(Paragraph(rincian, _GAYA["kecil"]))
        blok.append(Spacer(1, 2 * mm))
        cerita.append(KeepTogether(blok))
    return cerita


def buat_pdf_hasil(
    nama,
    input_cf,
    hasil,
    peta_gejala,
    peta_sumber=None,
    peringatan=False,
):
    """Bangun PDF hasil diagnosa dari percakapan chatbot."""
    aliran, doc = _dokumen("Hasil Diagnosa Cheat", "Laporan diagnosa")
    pemain = nama or "tanpa nama"
    cerita = _kepala(
        "Hasil Diagnosa Cheat",
        f"Pemain: {pemain} | Sumber data: percakapan diagnosa",
    )
    cerita.append(_p("Gejala yang dijawab", "h2"))
    if input_cf:
        cerita.append(_tabel_gejala(input_cf, peta_gejala))
    else:
        cerita.append(_p("Tidak ada jawaban gejala yang tercatat."))
    cerita.extend(_cerita_hasil(hasil, peta_sumber, peringatan))
    cerita.append(Spacer(1, 4 * mm))
    cerita.append(_p(explain.CATATAN_INDIKASI, "sub"))
    return _tutup(aliran, doc, cerita), f"hasil_diagnosa_{nama_berkas(pemain, 'tanpa_nama')}.pdf"


def buat_pdf_riwayat(detail, peta_gejala, peta_sumber=None):
    """Bangun PDF satu riwayat diagnosa yang tersimpan."""
    aliran, doc = _dokumen(
        f"Riwayat Diagnosa #{detail['id']}", "Laporan riwayat diagnosa"
    )
    pemain = detail.get("nama_pemain") or "tanpa nama"
    peringatan = (
        sum(1 for item in detail["hasil"] if item["persen"] >= 80) >= 3
    )
    cerita = _kepala(
        f"Riwayat Diagnosa #{detail['id']}",
        f"Pemain: {pemain} | Waktu: {detail.get('waktu', '-')}",
    )
    cerita.append(_p("Gejala yang diinput", "h2"))
    if detail["input"]:
        cerita.append(_tabel_gejala(detail["input"], peta_gejala))
    else:
        cerita.append(_p("Tidak ada jawaban gejala yang tercatat."))
    cerita.extend(_cerita_hasil(detail["hasil"], peta_sumber, peringatan))
    cerita.append(Spacer(1, 4 * mm))
    cerita.append(_p(explain.CATATAN_INDIKASI, "sub"))
    return (
        _tutup(aliran, doc, cerita),
        f"riwayat_{detail['id']}.pdf",
    )


def buat_pdf_referensi(baris):
    """Bangun PDF tabel aturan beserta sumber pengetahuannya."""
    aliran, doc = _dokumen(
        "Referensi Aturan", "Daftar aturan dan sumber", halaman=landscape(A4)
    )
    cerita = _kepala(
        "Referensi Aturan dan Sumber",
        f"Total {len(baris)} aturan pada basis pengetahuan.",
    )
    isi = [
        (
            item.get("Kode", "-"),
            item.get("Cheat", "-"),
            item.get("Gejala", "-"),
            item.get("CF pakar", "-"),
            item.get("Nama pakar", "-"),
            item.get("Tanggal wawancara", "-"),
            item.get("Jenis sumber", "-"),
            item.get("Sumber", "-"),
        )
        for item in baris
    ]
    cerita.append(
        _tabel(
            [
                "Kode",
                "Cheat",
                "Gejala",
                "CF pakar",
                "Nama pakar",
                "Tanggal",
                "Jenis sumber",
                "Sumber",
            ],
            isi,
            [
                12 * mm,
                29 * mm,
                41 * mm,
                14 * mm,
                29 * mm,
                21 * mm,
                18 * mm,
                97 * mm,
            ],
        )
    )
    cerita.append(Spacer(1, 4 * mm))
    cerita.append(_p(CATATAN_PRAKTISI, "sub"))
    return _tutup(aliran, doc, cerita), "referensi_aturan.pdf"


def buat_pdf_pengujian(baris):
    """Bangun PDF hasil pengujian skenario certainty factor."""
    aliran, doc = _dokumen(
        "Hasil Pengujian", "Verifikasi skenario CF", halaman=landscape(A4)
    )
    jumlah_lulus = sum(1 for item in baris if item.get("Status") == "LULUS")
    total = len(baris)
    status = "SELURUHNYA LULUS" if jumlah_lulus == total else "ADA YANG GAGAL"
    cerita = _kepala(
        "Hasil Pengujian Skenario",
        f"{jumlah_lulus} dari {total} skenario lulus - {status}. "
        "Toleransi perhitungan 0,01.",
    )
    isi = [
        (
            item.get("ID", "-"),
            item.get("Skenario", "-"),
            item.get("Input gejala", "-"),
            item.get("Diharapkan", "-"),
            item.get("Hasil sistem", "-"),
            item.get("Status", "-"),
            item.get("Langkah perhitungan manual", "-"),
        )
        for item in baris
    ]
    cerita.append(
        _tabel(
            [
                "ID",
                "Skenario",
                "Input gejala",
                "Diharapkan",
                "Hasil sistem",
                "Status",
                "Langkah perhitungan manual",
            ],
            isi,
            [
                12 * mm,
                44 * mm,
                34 * mm,
                29 * mm,
                29 * mm,
                15 * mm,
                98 * mm,
            ],
        )
    )
    return _tutup(aliran, doc, cerita), "hasil_pengujian.pdf"
