"""Halaman Penilaian Pakar: formulir validasi ahli untuk basis pengetahuan."""

import streamlit as st

from src import auth, penilaian, ui
from src.db import get_connection, init_db

st.set_page_config(page_title="Penilaian Pakar — PB Expert AI", layout="wide")


@st.cache_resource
def get_conn():
    conn = get_connection()
    init_db(conn)
    return conn


conn = get_conn()

ui.terapkan_gaya()
auth.wajib_login()
ui.judul_halaman("Penilaian Pakar: Indikasi Cheat pada Game Point Blank")

st.write(
    "Halo, saya Steven Cia (Teknik Komputer, ITEBA). Form ini untuk tugas "
    "aplikasi sistem pakar deteksi indikasi cheat di Point Blank. Mohon beri "
    "penilaian berdasarkan pengalaman Anda. Tidak ada jawaban benar atau salah. "
    "Waktu pengisian sekitar 10-15 menit. Nama Anda akan dicantumkan sebagai "
    "sumber pakar di laporan."
)

st.session_state.setdefault("pakar_nonce", 0)
st.session_state.setdefault("pakar_terkirim", False)
nonce = st.session_state["pakar_nonce"]

if st.session_state.get("pakar_terkirim"):
    st.success(
        "Terima kasih. Penilaian Anda sudah tersimpan dan akan dicantumkan "
        "sebagai sumber pakar pada laporan."
    )
    st.caption(
        "Nama ditampilkan sesuai pilihan izin: nama lengkap atau inisial saja."
    )
    if st.button("Isi penilaian baru", key="pakar_baru"):
        st.session_state["pakar_terkirim"] = False
        st.session_state["pakar_nonce"] += 1
        st.rerun()
    st.stop()

st.subheader("Bagian 1: Profil Pakar")
nama = st.text_input("1. Nama lengkap", key=f"pakar_nama_{nonce}")
peran = st.selectbox(
    "2. Peran di komunitas Point Blank",
    options=penilaian.PERAN_PAKAR,
    key=f"pakar_peran_{nonce}",
)
lama_bermain = st.selectbox(
    "3. Sudah berapa lama bermain atau berperan di Point Blank?",
    options=penilaian.LAMA_BERMAIN,
    key=f"pakar_lama_{nonce}",
)
rank = st.text_input(
    "4. Rank atau pengalaman yang bisa dibanggakan (boleh kosong)",
    key=f"pakar_rank_{nonce}",
)
izin_nama = st.radio(
    "5. Apakah Anda bersedia namanya dicantumkan di laporan?",
    options=penilaian.PILIHAN_IZIN,
    horizontal=True,
    key=f"pakar_izin_{nonce}",
)

st.subheader("Bagian 2: Pengalaman")
pengalaman_ciri = st.text_area(
    "6. Dari pengalaman Anda, ciri apa yang paling meyakinkan bahwa "
    "seseorang memakai cheat?",
    key=f"pakar_ciri_{nonce}",
)
pengalaman_beda = st.text_area(
    "7. Bagaimana Anda membedakan pemain yang memang jago dari pemain yang "
    "memakai cheat?",
    key=f"pakar_beda_{nonce}",
)
pengalaman_mitos = st.text_area(
    "8. Ciri apa yang sering disangka cheat padahal pemain tersebut hanya jago?",
    key=f"pakar_mitos_{nonce}",
)
pengalaman_bukti = st.text_area(
    "9. Bukti apa yang biasa dipakai saat melaporkan cheater (rekaman, replay, "
    "statistik, dll.)?",
    key=f"pakar_bukti_{nonce}",
)

st.subheader("Bagian 3: Penilaian Keyakinan")
st.write(
    'Petunjuk: "Jika ciri ini terlihat pada seorang pemain, seberapa yakin '
    'Anda bahwa ia memakai cheat jenis yang tertulis?"'
)
st.caption("Skala: " + " | ".join(penilaian.LABEL_SKALA))

nilai_penilaian = {}
for aturan in penilaian.ATURAN_FORM:
    kiri, kanan = st.columns([4, 3])
    kiri.markdown(
        f"**{aturan['kode']}** — {aturan['ciri']}  \n"
        f"Cheat: **{aturan['cheat']}**"
    )
    label = kanan.selectbox(
        f"Keyakinan {aturan['kode']}",
        options=penilaian.LABEL_SKALA,
        index=0,
        key=f"pakar_skala_{aturan['kode']}_{nonce}",
        label_visibility="collapsed",
    )
    nilai_penilaian[aturan["kode"]] = penilaian.NILAI_SKALA[label]

st.subheader("Bagian 4: Penutup")
ciri_lain = st.text_area(
    "10. Ciri lain yang menurut Anda penting tetapi belum ada di daftar di atas?",
    key=f"pakar_ciri_lain_{nonce}",
)
cheat_lain = st.text_area(
    "11. Cheat jenis lain yang sering Anda temui di Point Blank?",
    key=f"pakar_cheat_lain_{nonce}",
)
boleh_dihubungi = st.radio(
    "12. Bolehkah saya menghubungi Anda lagi bila ada pertanyaan lanjutan?",
    options=penilaian.PILIHAN_HUBUNGI,
    index=1,
    horizontal=True,
    key=f"pakar_hubungi_{nonce}",
)

if st.button(
    "Kirim penilaian",
    type="primary",
    key=f"kirim_penilaian_{nonce}",
):
    data = {
        "nama": nama,
        "peran": peran,
        "lama_bermain": lama_bermain,
        "rank": rank,
        "izin_nama": izin_nama,
        "pengalaman_ciri": pengalaman_ciri,
        "pengalaman_beda": pengalaman_beda,
        "pengalaman_mitos": pengalaman_mitos,
        "pengalaman_bukti": pengalaman_bukti,
        "penilaian": nilai_penilaian,
        "ciri_lain": ciri_lain,
        "cheat_lain": cheat_lain,
        "boleh_dihubungi": boleh_dihubungi,
    }
    try:
        penilaian.simpan_penilaian(conn, data)
    except ValueError as kesalahan:
        st.error(str(kesalahan))
    else:
        st.session_state["pakar_terkirim"] = True
        st.rerun()
