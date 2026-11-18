"""Aplikasi utama Streamlit — PB Expert AI, console sistem pakar Point Blank."""

import streamlit as st

from src import auth, knowledge, ui
from src.db import get_connection, init_db

st.set_page_config(
    page_title="PB Expert AI — Sistem Pakar Deteksi Kecurangan Point Blank",
    layout="wide",
)


@st.cache_resource
def get_db_connection():
    conn = get_connection()
    init_db(conn)
    knowledge.seed_if_empty(conn)
    return conn


conn = get_db_connection()
daftar_cheat = knowledge.get_cheats(conn)
daftar_gejala = knowledge.get_gejala(conn)
daftar_aturan = knowledge.get_aturan(conn)
daftar_sumber = knowledge.get_sumber(conn)

ui.terapkan_gaya()
auth.wajib_login()

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-grid">
            <div>
                <div class="hero-label">
                    <span class="status-dot"></span>
                    AI Expert System · Knowledge-Based Decision Support
                </div>
                <h1>PB Expert AI</h1>
                <p class="hero-sub">
                    Deteksi Kecurangan Point Blank dengan pendekatan expert system
                    profesional: fakta pengamatan diolah oleh mesin inferensi
                    forward chaining dan certainty factor menjadi kesimpulan yang
                    terukur, transparan, dan dapat ditelusuri.
                </p>
                <p class="hero-note">
                    Dirancang sebagai decision support untuk pemain, pelatih, dan
                    pengelola komunitas. Sistem tidak membaca memori game dan tidak
                    menyentuh proses game apa pun.
                </p>
            </div>
            <div class="hero-panel">
                <div class="hero-panel-label">Engine status</div>
                <div class="hero-status">
                    <span class="status-dot"></span> Inference engine aktif
                </div>
                <div class="hero-status-row">
                    <span>Metode inferensi</span><strong>Forward Chaining</strong>
                </div>
                <div class="hero-status-row">
                    <span>Ketidakpastian</span><strong>Certainty Factor</strong>
                </div>
                <div class="hero-status-row">
                    <span>Basis aturan</span><strong>{len(daftar_aturan)} rules</strong>
                </div>
                <div class="hero-status-row">
                    <span>Kedudukan sistem</span><strong>Human-in-the-loop</strong>
                </div>
            </div>
        </div>
        <div class="statistik">
            <div class="stat">
                <span>Jenis cheat</span><strong>{len(daftar_cheat)}</strong>
                <small>Kategori diagnosis</small>
            </div>
            <div class="stat">
                <span>Gejala</span><strong>{len(daftar_gejala)}</strong>
                <small>Fakta yang dapat diamati</small>
            </div>
            <div class="stat">
                <span>Aturan pakar</span><strong>{len(daftar_aturan)}</strong>
                <small>IF-THEN dengan CF</small>
            </div>
            <div class="stat">
                <span>Sumber</span><strong>{len(daftar_sumber)}</strong>
                <small>Jurnal dan praktisi</small>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

kolom_utama, kolom_panduan, kolom_info = st.columns([1.1, 1, 1.25])
with kolom_utama:
    if st.button("Mulai analisis AI", type="primary", use_container_width=True):
        st.switch_page("pages/1_Diagnosa.py")
with kolom_panduan:
    if st.button("Buka panduan gejala", use_container_width=True):
        st.switch_page("pages/8_Panduan_Gejala.py")
with kolom_info:
    st.caption(
        "Wawancara terarah, hasil ranking, jejak inferensi, dan sumber ilmiah "
        "tersedia dalam satu alur."
    )

st.markdown(
    """
    <div class="section-heading">
        <span class="section-kicker">Expert System Pipeline</span>
        <h2>Dari fakta gejala ke kesimpulan yang dapat diaudit</h2>
        <p>Setiap diagnosis melewati empat lapisan penalaran yang sama, sehingga
        keputusan sistem dapat dijelaskan dan diperiksa kembali.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
ui.alur_expert_system(len(daftar_aturan))

st.markdown(
    """
    <div class="section-heading">
        <span class="section-kicker">Professional Capabilities</span>
        <h2>Dirancang seperti konsol analisis, bukan kotak hitam</h2>
    </div>
    <div class="feature-grid">
        <div class="feature-card">
            <span class="feature-tag">Knowledge base</span>
            <h3>Basis pengetahuan eksplisit</h3>
            <p>13 aturan IF-THEN, CF pakar, sumber jurnal, dan penilaian pakar
            tersimpan dalam basis data yang dapat dikelola admin.</p>
        </div>
        <div class="feature-card">
            <span class="feature-tag">Explainable AI</span>
            <h3>Penalaran transparan</h3>
            <p>Pengguna melihat fakta yang terekam, aturan yang terpicu, nilai CF
            sebelum dan sesudah agregasi, serta alasan di balik ranking.</p>
        </div>
        <div class="feature-card">
            <span class="feature-tag">Decision support</span>
            <h3>Keputusan tetap di tangan manusia</h3>
            <p>Hasil bersifat indikatif. Verifikasi video, pola bermain, dan
            keputusan moderator tetap menjadi otoritas manusia.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

kiri, kanan = st.columns([1.05, 1])
with kiri:
    st.subheader("Alur analisis")
    st.markdown(
        """
        <div class="langkah">1. Buka halaman Diagnosa dan mulai sesi wawancara gejala.</div>
        <div class="langkah">2. Jawab pertanyaan PB-Bot dengan Iya atau Tidak sesuai pengamatanmu.</div>
        <div class="langkah">3. Mesin inferensi menghitung ranking cheat, CF, dan penjelasan perhitungan.</div>
        <div class="langkah">4. Tinjau jejak inferensi, simpan ke riwayat, atau unduh laporan PDF.</div>
        """,
        unsafe_allow_html=True,
    )
with kanan:
    st.markdown(
        """
        <div class="note-panel">
            <h3>Prinsip penggunaan</h3>
            <p>Gunakan sistem sebagai alat bantu analisis, bukan sebagai vonis.</p>
            <ul>
                <li>Catat hanya gejala yang benar-benar terlihat.</li>
                <li>Bedakan skill tinggi, ping tidak stabil, bug, dan cheat.</li>
                <li>Verifikasi dengan replay atau bukti video sebelum melapor.</li>
                <li>Hasil adalah indikasi berdasarkan pengamatan pengguna dan bukan bukti pasti.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="section-heading">
        <span class="section-kicker">Knowledge Base</span>
        <h2>Basis pengetahuan yang dapat diperiksa</h2>
        <p>Buka panel berikut untuk melihat cakupan cheat, gejala, aturan, dan
        sumber yang dipakai mesin inferensi.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("Jenis cheat dan cakupan diagnosis"):
    st.dataframe(
        [
            {"Kode": c["kode"], "Nama": c["nama"], "Deskripsi": c["deskripsi"]}
            for c in daftar_cheat
        ],
        hide_index=True,
    )

with st.expander("Gejala yang dapat diamati"):
    st.dataframe(
        [
            {"Kode": g["kode"], "Gejala": g["deskripsi"]}
            for g in daftar_gejala
        ],
        hide_index=True,
    )

with st.expander("Aturan inferensi dan bobot CF pakar"):
    st.dataframe(
        [
            {
                "Aturan": a["kode"],
                "Cheat": a["kode_cheat"],
                "Gejala": a["kode_gejala"],
                "CF pakar": a["cf_pakar"],
            }
            for a in daftar_aturan
        ],
        hide_index=True,
    )

with st.expander("Sumber pengetahuan"):
    st.dataframe(
        [
            {
                "Jenis": s["jenis"],
                "Sitasi": s["sitasi"],
                "DOI / URL": s.get("url_doi") or "",
            }
            for s in daftar_sumber
        ],
        hide_index=True,
    )

st.markdown(
    '<div class="footer-note">PB Expert AI · Expert system for educational '
    "decision support · Forward chaining + certainty factor</div>",
    unsafe_allow_html=True,
)
