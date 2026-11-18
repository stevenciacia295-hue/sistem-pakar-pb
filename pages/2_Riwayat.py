"""Halaman Riwayat: tabel, detail, dan hapus riwayat diagnosa."""

import pandas as pd
import streamlit as st

from src import auth, explain, history, knowledge, laporan_pdf, ui
from src.db import get_connection, init_db

st.set_page_config(page_title="Riwayat — PB Expert AI", layout="wide")


@st.cache_resource
def get_conn():
    conn = get_connection()
    init_db(conn)
    knowledge.seed_if_empty(conn)
    return conn


conn = get_conn()
peta_gejala = {g["kode"]: g["deskripsi"] for g in knowledge.get_gejala(conn)}
peta_sumber = knowledge.peta_sumber_aturan(conn)

ui.terapkan_gaya()
auth.wajib_login()
ui.judul_halaman(
    "Riwayat Diagnosa",
    "Tinjau kembali hasil analisis yang pernah disimpan, lihat rinciannya, "
    "atau hapus data yang tidak diperlukan.",
)

daftar = history.get_riwayat(conn)

if not daftar:
    st.write("Belum ada riwayat diagnosa.")
else:
    baris_tabel = []
    for item in daftar:
        hasil = item["hasil"]
        teratas = hasil[0] if hasil else None
        ringkasan = (
            f"{teratas['nama']} {explain.format_persen(teratas['persen'])} "
            f"({teratas['kategori']})"
            if teratas
            else "Tidak ada kesimpulan"
        )
        baris_tabel.append(
            {
                "ID": item["id"],
                "Waktu": item["waktu"],
                "Pemain": item["nama_pemain"] or "-",
                "Hasil teratas": ringkasan,
                "Jumlah gejala": len(item["input"]),
            }
        )
    st.dataframe(pd.DataFrame(baris_tabel), hide_index=True)

    pilihan = st.selectbox(
        "Pilih riwayat untuk melihat detail",
        options=[item["id"] for item in daftar],
        format_func=lambda nilai: next(
            f"#{item['id']} — {item['waktu']} — {item['nama_pemain'] or 'tanpa nama'}"
            for item in daftar
            if item["id"] == nilai
        ),
    )

    detail = history.get_riwayat_by_id(conn, pilihan)
    if detail:
        with st.container(border=True):
            st.subheader(f"Detail riwayat #{detail['id']}")
            st.write(f"Waktu: {detail['waktu']}")
            st.write(f"Pemain: {detail['nama_pemain'] or '-'}")

            st.markdown("**Gejala yang diinput**")
            for kode, nilai_cf in detail["input"].items():
                deskripsi = peta_gejala.get(kode, "deskripsi tidak ditemukan")
                st.write(
                    f"{kode} - {deskripsi}, keyakinan pengguna {nilai_cf:.1f}"
                )

            st.markdown("**Hasil**")
            jumlah_tinggi = sum(
                1 for item in detail["hasil"] if item["persen"] >= 80
            )
            if jumlah_tinggi >= 3:
                st.warning(explain.PERINGATAN_TIDAK_KONSISTEN)
            if not detail["hasil"]:
                st.write("Tidak ada jenis cheat yang dapat disimpulkan.")
            else:
                for item in detail["hasil"]:
                    st.markdown(f"**{item['nama']} ({item['kode_cheat']})**")
                    st.progress(min(max(item["cf_gabungan"], 0.0), 1.0))
                    st.write(
                        f"Keyakinan: {explain.format_persen(item['persen'])} "
                        f"({item['kategori']})"
                    )
                    st.write(explain.arti_hasil(item))
                    st.markdown("**Kenapa sistem menyimpulkan ini:**")
                    for alasan in explain.alasan_hasil(item):
                        st.write(f"- {alasan}")
                    with st.expander(f"Penjelasan perhitungan {item['kode_cheat']}"):
                        for baris in explain.penjelasan_perhitungan(
                            item, peta_sumber
                        ):
                            st.write(baris)
                    st.divider()

            st.caption(explain.CATATAN_INDIKASI)

            data_pdf, berkas_pdf = laporan_pdf.buat_pdf_riwayat(
                detail, peta_gejala, peta_sumber
            )
            st.download_button(
                "Cetak PDF riwayat",
                data=data_pdf,
                file_name=berkas_pdf,
                mime="application/pdf",
                key=f"unduh_pdf_riwayat_{detail['id']}",
            )

            yakin = st.checkbox("Saya yakin ingin menghapus data yang dipilih.")
            kolom_satu, kolom_dua = st.columns(2)
            if kolom_satu.button("Hapus riwayat ini", disabled=not yakin):
                history.hapus_riwayat(conn, detail["id"])
                st.rerun()
            if kolom_dua.button("Hapus semua riwayat", disabled=not yakin):
                history.hapus_semua_riwayat(conn)
                st.rerun()
