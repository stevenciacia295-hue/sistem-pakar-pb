"""Halaman Referensi: seluruh aturan beserta sumber pengetahuannya."""

import pandas as pd
import streamlit as st

from src import auth, explain, knowledge, laporan_pdf, ui
from src.db import get_connection, init_db

st.set_page_config(page_title="Referensi — PB Expert AI", layout="wide")


@st.cache_resource
def get_conn():
    conn = get_connection()
    init_db(conn)
    knowledge.seed_if_empty(conn)
    return conn


conn = get_conn()
daftar_aturan = knowledge.get_aturan(conn)
daftar_cheat = knowledge.get_cheats(conn)
daftar_gejala = knowledge.get_gejala(conn)
daftar_sumber = knowledge.get_sumber(conn)
peta_sumber = knowledge.peta_sumber_aturan(conn)

ui.terapkan_gaya()
auth.wajib_login()
ui.judul_halaman(
    "Referensi",
    "Setiap aturan pada basis pengetahuan ditautkan ke sumber jurnal, pakar, "
    "atau pengamatan praktisi.",
)

peta_cheat = {c["kode"]: c["nama"] for c in daftar_cheat}
peta_gejala = {g["kode"]: g["deskripsi"] for g in daftar_gejala}


def _jenis_sumber(daftar):
    jenis = []
    for sumber in daftar:
        if sumber["jenis"] not in jenis:
            jenis.append(sumber["jenis"])
    return ", ".join(jenis) if jenis else "-"


baris = []
for aturan in daftar_aturan:
    sumber_aturan = peta_sumber.get(aturan["kode"], [])
    baris.append(
        {
            "Kode": aturan["kode"],
            "Cheat": peta_cheat.get(aturan["kode_cheat"], aturan["kode_cheat"]),
            "Gejala": peta_gejala.get(aturan["kode_gejala"], aturan["kode_gejala"]),
            "CF pakar": f"{aturan['cf_pakar']:.2f}",
            "Nama pakar": aturan["nama_pakar"],
            "Tanggal wawancara": aturan["tanggal_wawancara"],
            "Jenis sumber": _jenis_sumber(sumber_aturan),
            "Sumber": explain.teks_sumber(sumber_aturan),
        }
    )

tabel = pd.DataFrame(baris)

st.subheader("Aturan dan sumber")
st.write(f"Total {len(baris)} aturan, {len(daftar_sumber)} sumber pengetahuan.")
st.dataframe(tabel, hide_index=True, width="stretch")

data_pdf, berkas_pdf = laporan_pdf.buat_pdf_referensi(baris)

kolom_csv, kolom_pdf = st.columns(2)
kolom_csv.download_button(
    "Unduh CSV",
    data=tabel.to_csv(index=False).encode("utf-8"),
    file_name="referensi_aturan.csv",
    mime="text/csv",
)
kolom_pdf.download_button(
    "Cetak PDF",
    data=data_pdf,
    file_name=berkas_pdf,
    mime="application/pdf",
    key="unduh_pdf_referensi",
)

with st.expander("Daftar sumber pengetahuan"):
    if not daftar_sumber:
        st.write("Belum ada sumber pengetahuan.")
    else:
        jumlah_tautan = {}
        for kode, daftar in peta_sumber.items():
            for sumber in daftar:
                jumlah_tautan[sumber["id"]] = jumlah_tautan.get(sumber["id"], 0) + 1
        tabel_sumber = pd.DataFrame(
            [
                {
                    "ID": sumber["id"],
                    "Jenis": sumber["jenis"],
                    "Sitasi": sumber["sitasi"],
                    "URL atau DOI": sumber["url_doi"] or "-",
                    "Jumlah aturan": jumlah_tautan.get(sumber["id"], 0),
                }
                for sumber in daftar_sumber
            ]
        )
        st.dataframe(tabel_sumber, hide_index=True, width="stretch")
