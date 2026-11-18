"""Gerbang login pengguna umum dan tombol keluar untuk seluruh halaman."""

import streamlit as st

from src import akun, ui

KUNCI_LOGIN = ("pengguna_ok", "pengguna_nama", "admin_ok", "admin_password")


def sumber_akun():
    """Ambil akun dari st.secrets bila lengkap, jika tidak dari lingkungan."""
    try:
        nama = st.secrets["APP_USERNAME"]
        sandi = st.secrets["APP_PASSWORD"]
    except Exception:
        nama = sandi = None
    if nama and sandi:
        return {"username": str(nama), "password": str(sandi)}, False
    return akun.sumber_akun()


def keluar():
    """Hapus status login pengguna dan admin, lalu muat ulang halaman."""
    for kunci in KUNCI_LOGIN:
        st.session_state.pop(kunci, None)
    st.session_state.pop("login_password", None)
    st.session_state["login_username"] = ""
    st.rerun()


def _tampilkan_sidebar():
    nama = st.session_state.get("pengguna_nama", "pengguna")
    st.sidebar.caption(f"Masuk sebagai {nama}")
    if st.sidebar.button("Keluar", key="keluar_pengguna"):
        keluar()


def wajib_login():
    """Tampilkan formulir masuk bila belum login, lalu hentikan halaman."""
    if st.session_state.get("pengguna_ok"):
        _tampilkan_sidebar()
        return

    data, pakai_default = sumber_akun()

    kiri, kanan = st.columns([1.15, 1], gap="large")
    with kiri:
        ui.judul_halaman(
            "Masuk",
            "Masuk untuk memakai sistem pakar deteksi kecurangan Point Blank.",
        )
        st.markdown(
            """
            <div class="feature-card">
                <span class="feature-tag">Secure access</span>
                <h3>PB Expert AI Console</h3>
                <p>Ruang kerja untuk wawancara gejala, penalaran forward
                chaining, agregasi certainty factor, dan penelusuran hasil.
                Setiap kesimpulan disertai alasan dan sumber.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if pakai_default:
            st.caption(
                "Nama bebas. Kata sandi awal ada di README, lalu ganti lewat "
                "APP_PASSWORD."
            )
    with kanan:
        with st.container(border=True):
            st.markdown(
                '<div class="sidebar-title">Akses pengguna</div>',
                unsafe_allow_html=True,
            )
            nama = st.text_input("Nama pengguna", key="login_username")
            sandi = st.text_input(
                "Kata sandi", type="password", key="login_password"
            )
            if st.button("Masuk", key="masuk_pengguna", type="primary"):
                if akun.validasi_login(nama, sandi, data):
                    st.session_state["pengguna_ok"] = True
                    st.session_state["pengguna_nama"] = str(nama).strip()
                    st.rerun()
                else:
                    st.error("Nama pengguna atau kata sandi salah.")
    st.stop()
