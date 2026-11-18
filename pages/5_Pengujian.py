"""Halaman Pengujian: skenario uji perhitungan CF dan unduhan CSV."""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from src import auth, knowledge, laporan_pdf, ui
from src.db import get_connection, init_db
from src.engine import diagnose

st.set_page_config(page_title="Pengujian — PB Expert AI", layout="wide")

BERKAS_SKENARIO = (
    Path(__file__).resolve().parent.parent / "data" / "skenario_uji.json"
)
TOLERANSI = 0.01


@st.cache_resource
def get_conn():
    conn = get_connection()
    init_db(conn)
    knowledge.seed_if_empty(conn)
    return conn


conn = get_conn()
daftar_gejala = knowledge.get_gejala(conn)
daftar_aturan = knowledge.get_aturan(conn)
daftar_cheat = knowledge.get_cheats(conn)

ui.terapkan_gaya()
auth.wajib_login()
ui.judul_halaman(
    "Pengujian",
    "Verifikasi perhitungan certainty factor terhadap skenario manual. "
    "Berkas skenario dapat diedit pada data/skenario_uji.json.",
)

if not BERKAS_SKENARIO.exists():
    st.warning("Berkas data/skenario_uji.json tidak ditemukan.")
    st.stop()

try:
    skenario = json.loads(BERKAS_SKENARIO.read_text(encoding="utf-8"))
except (json.JSONDecodeError, OSError) as kesalahan:
    st.error(f"Gagal membaca skenario: {kesalahan}")
    st.stop()

if not isinstance(skenario, list) or not skenario:
    st.warning("Daftar skenario kosong atau formatnya tidak sesuai.")
    st.stop()


def _teks_input(input_cf):
    if not input_cf:
        return "Tidak ada"
    return ", ".join(f"{kode}={nilai:.1f}" for kode, nilai in input_cf.items())


def _teks_hasil(hasil):
    if not hasil:
        return "Tidak ada"
    teratas = hasil[0]
    return f"{teratas['nama']} {teratas['persen']:.1f}%"


baris = []
jumlah_lulus = 0
for data in skenario:
    input_cf = {
        kode: float(nilai) for kode, nilai in data.get("input", {}).items()
    }
    diharapkan = data.get("diharapkan", {})
    kode_harap = diharapkan.get("kode_cheat")
    persen_harap = float(diharapkan.get("persen", 0.0))

    hasil = diagnose(input_cf, daftar_aturan, daftar_cheat, daftar_gejala)
    if hasil:
        kode_sistem = hasil[0]["kode_cheat"]
        persen_sistem = float(hasil[0]["persen"])
    else:
        kode_sistem = None
        persen_sistem = 0.0

    lulus = kode_sistem == kode_harap and abs(
        persen_sistem - persen_harap
    ) <= TOLERANSI
    if lulus:
        jumlah_lulus += 1

    baris.append(
        {
            "ID": data.get("id", "-"),
            "Skenario": data.get("skenario", "-"),
            "Input gejala": _teks_input(input_cf),
            "Diharapkan": _teks_hasil(
                [{"nama": diharapkan.get("nama", "-"), "persen": persen_harap}]
                if kode_harap
                else []
            ),
            "Hasil sistem": _teks_hasil(hasil),
            "Status": "LULUS" if lulus else "GAGAL",
            "Langkah perhitungan manual": data.get("langkah", "-"),
        }
    )

tabel = pd.DataFrame(baris)

st.write(f"{jumlah_lulus} dari {len(baris)} skenario lulus.")
if jumlah_lulus < len(baris):
    st.warning("Ada skenario yang gagal. Periksa kembali basis pengetahuan.")
else:
    st.write("Seluruh skenario lulus dengan toleransi 0,01.")

st.dataframe(tabel, hide_index=True, width="stretch")

data_pdf, berkas_pdf = laporan_pdf.buat_pdf_pengujian(baris)

kolom_csv, kolom_pdf = st.columns(2)
kolom_csv.download_button(
    "Unduh CSV",
    data=tabel.to_csv(index=False).encode("utf-8"),
    file_name="hasil_pengujian.csv",
    mime="text/csv",
)
kolom_pdf.download_button(
    "Cetak PDF",
    data=data_pdf,
    file_name=berkas_pdf,
    mime="application/pdf",
    key="unduh_pdf_pengujian",
)
