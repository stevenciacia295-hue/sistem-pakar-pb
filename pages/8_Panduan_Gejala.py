"""Halaman Panduan Gejala: pertanyaan, jawaban, penyebab, dan solusi."""

import pandas as pd
import streamlit as st

from src import auth, knowledge, panduan, percakapan, ui
from src.db import get_connection, init_db

st.set_page_config(page_title="Panduan Gejala — PB Expert AI", layout="wide")


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
peta_nama_cheat = {c["kode"]: c["nama"] for c in daftar_cheat}
peta_aturan = {}
for aturan in daftar_aturan:
    peta_aturan.setdefault(aturan["kode_gejala"], []).append(aturan)

ARTI_JAWABAN = {
    "Iya": "Gejala terlihat dan mendukung indikasi.",
    "Tidak": "Gejala tidak terlihat dan tidak mendukung indikasi.",
}

ui.terapkan_gaya()
auth.wajib_login()

ui.judul_halaman(
    "Panduan Gejala",
    "Daftar pertanyaan PB-Bot, arti jawaban, penyebab gejala, dan cara "
    "penyelesaiannya.",
)
st.write(
    "Halaman ini menjelaskan setiap gejala yang dipakai sistem: apa yang "
    "dimaksud, mengapa bisa terjadi, pertanyaan yang akan diajukan PB-Bot, "
    "arti pilihan jawaban, dan langkah verifikasi yang bisa dilakukan."
)
st.caption(panduan.CATATAN)

baris_ringkas = []
for gejala in daftar_gejala:
    aturan_terkait = peta_aturan.get(gejala["kode"], [])
    baris_ringkas.append(
        {
            "Kode": gejala["kode"],
            "Gejala": gejala["deskripsi"],
            "Cheat terkait": ", ".join(
                sorted(
                    {
                        peta_nama_cheat.get(a["kode_cheat"], a["kode_cheat"])
                        for a in aturan_terkait
                    }
                )
            )
            or "-",
            "Jumlah aturan": len(aturan_terkait),
        }
    )
st.dataframe(pd.DataFrame(baris_ringkas), hide_index=True)

pilihan = st.selectbox(
    "Tampilkan panduan",
    options=["Semua gejala"] + [g["kode"] for g in daftar_gejala],
    format_func=lambda kode: (
        "Semua gejala"
        if kode == "Semua gejala"
        else next(
            f"{g['kode']} — {g['deskripsi']}"
            for g in daftar_gejala
            if g["kode"] == kode
        )
    ),
    key="panduan_pilih",
)

gejala_tampil = [
    g for g in daftar_gejala if pilihan in ("Semua gejala", g["kode"])
]
for gejala in gejala_tampil:
    kode = gejala["kode"]
    deskripsi = gejala["deskripsi"]
    judul = deskripsi[:1].upper() + deskripsi[1:]
    isi = panduan.get_panduan(kode)
    with st.expander(f"{kode} — {judul}"):
        st.markdown(f"**Apa yang dimaksud?**  \n{isi['apa']}")
        st.markdown(f"**Mengapa bisa terjadi?**  \n{isi['mengapa']}")

        st.markdown("**Pertanyaan PB-Bot**")
        varian = percakapan.PERTANYAAN.get(kode) or [
            f"Apakah kamu melihat gejala {kode} pada pemain tersebut?"
        ]
        st.markdown("\n".join(f"{nomor}. {teks}" for nomor, teks in enumerate(varian, 1)))

        st.markdown("**Pilihan jawaban**")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Jawaban": label,
                        "Nilai CF": "-" if nilai is None else f"{nilai:.1f}",
                        "Arti": ARTI_JAWABAN.get(label, "-"),
                    }
                    for label, nilai in percakapan.PILIHAN_JAWABAN
                ]
            ),
            hide_index=True,
        )

        st.markdown("**Cara penyelesaian dan verifikasi**")
        st.markdown(
            "\n".join(
                f"{nomor}. {langkah}"
                for nomor, langkah in enumerate(isi["solusi"], 1)
            )
        )

        aturan_terkait = peta_aturan.get(kode, [])
        if aturan_terkait:
            st.markdown("**Aturan terkait**")
            st.markdown(
                "\n".join(
                    f"- {a['kode']} → "
                    f"{peta_nama_cheat.get(a['kode_cheat'], a['kode_cheat'])} "
                    f"(CF pakar {a['cf_pakar']:.1f})"
                    for a in aturan_terkait
                )
            )
        st.caption(panduan.CATATAN)

st.markdown(
    "Buka halaman **Diagnosa** melalui menu di kiri untuk mulai menganalisis "
    "pemain dengan PB-Bot."
)
