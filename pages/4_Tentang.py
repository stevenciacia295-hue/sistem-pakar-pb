"""Halaman Tentang: penjelasan metode dan batasan aplikasi."""

import pandas as pd
import streamlit as st

from src import auth, knowledge, ui
from src.db import get_connection, init_db

st.set_page_config(page_title="Tentang — PB Expert AI", layout="wide")


@st.cache_resource
def get_conn():
    conn = get_connection()
    init_db(conn)
    knowledge.seed_if_empty(conn)
    return conn


conn = get_conn()

ui.terapkan_gaya()
auth.wajib_login()
ui.judul_halaman(
    "Tentang",
    "Penjelasan metode, rumus perhitungan, dan batasan aplikasi.",
)

st.write(
    "Aplikasi ini adalah sistem pakar untuk mendeteksi indikasi kecurangan "
    "(cheat) pada permainan Point Blank berdasarkan gejala yang diamati oleh "
    "pengguna. Aplikasi ini hanya menganalisis gejala yang diinput pengguna."
)

st.write(
    "Hasil adalah indikasi berdasarkan pengamatan pengguna dan bukan bukti pasti."
)

st.markdown(
    """
    <div class="section-heading">
        <span class="section-kicker">Expert System Architecture</span>
        <h2>Empat lapisan penalaran yang dapat ditelusuri</h2>
        <p>PB Expert AI memisahkan pengetahuan pakar, fakta pengguna, mesin
        inferensi, dan fasilitas penjelasan agar setiap keputusan dapat diperiksa.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
ui.alur_expert_system(len(knowledge.get_aturan(conn)))

st.write(
    "Komponen utamanya adalah basis pengetahuan (cheat, gejala, aturan, CF "
    "pakar, dan sumber), working memory (jawaban Iya yang terekam sebagai "
    "fakta), inference engine (forward chaining dan agregasi CF), serta "
    "explanation facility (alasan, jejak hitung, dan sumber ilmiah)."
)

st.subheader("Forward Chaining")
st.write(
    "Forward chaining adalah metode inferensi yang bergerak dari fakta menuju "
    "kesimpulan. Fakta berupa gejala yang dipilih pengguna dicocokkan dengan "
    "aturan basis pengetahuan: jika gejala tertentu muncul, maka jenis cheat "
    "tertentu mungkin terjadi. Seluruh aturan yang cocok dieksekusi untuk "
    "menghasilkan daftar jenis cheat yang mungkin."
)

st.subheader("Certainty Factor")
st.write(
    "Certainty Factor (CF) menyatakan tingkat keyakinan terhadap suatu fakta "
    "atau aturan dalam rentang 0 sampai 1. CF pengguna berasal dari pilihan "
    "tingkat keyakinan pengamat, sedangkan CF pakar berasal dari basis "
    "pengetahuan. Perhitungan yang digunakan:"
)
st.code(
    "CF aturan   = CF pengguna x CF pakar\n"
    "CF gabungan = CF lama + CF baru x (1 - CF lama)\n"
    "Persentase  = CF gabungan x 100",
    language="text",
)
st.write(
    "Nilai CF dari beberapa aturan yang menuju jenis cheat yang sama "
    "digabungkan berurutan hingga diperoleh satu nilai akhir per jenis cheat."
)

st.subheader("Keterlacakan hasil")
st.write(
    "Setiap kesimpulan dapat ditelusuri dari fakta hingga sumber. Halaman "
    "Diagnosa menampilkan working memory, aturan yang terpicu, nilai CF "
    "sebelum dan sesudah agregasi, ranking akhir, serta sumber ilmiah yang "
    "mendukung aturan tersebut."
)
st.code(
    "Fakta gejala (G01 = Iya)\n"
    "  -> Rule R01 (C01, CF pakar 0.7)\n"
    "  -> CF aturan = 1.0 x 0.7 = 0.70\n"
    "  -> Agregasi CF per jenis cheat\n"
    "  -> Ranking + kategori + sumber",
    language="text",
)

st.subheader("Peran manusia")
st.write(
    "Sistem ini adalah decision support, bukan pengganti moderator. Pengguna "
    "tetap harus membedakan skill tinggi, ping tidak stabil, bug, dan cheat, "
    "lalu memverifikasi temuan dengan replay atau bukti video."
)

st.subheader("Alur percakapan")
st.write(
    "PB-Bot menanyakan satu gejala pada satu waktu dengan kalimat yang "
    "bervariasi. Pengguna menjawab Iya atau Tidak, lalu bot menghitung hasil "
    "setelah seluruh pertanyaan selesai."
)

st.subheader("Skala jawaban")
st.write(
    "Iya bernilai 1.0 dan Tidak bernilai 0.0. Jawaban Tidak tidak mengaktifkan "
    "aturan gejala tersebut."
)

st.subheader("Kategori hasil")
st.write("- 80 persen atau lebih: Sangat mungkin, hanya untuk peringkat teratas")
st.write("- Cheat lain yang masih 80 persen atau lebih: Mungkin")
st.write("- 50 sampai 79 persen: Mungkin")
st.write("- Kurang dari 50 persen: Kemungkinan kecil")

st.subheader("Sumber pakar")
ringkasan_pakar = knowledge.ringkasan_pakar(conn)
if ringkasan_pakar:
    st.dataframe(
        pd.DataFrame(
            [
                {"Pakar": item["nama_pakar"], "Jumlah aturan": item["jumlah"]}
                for item in ringkasan_pakar
            ]
        ),
        hide_index=True,
    )
else:
    st.write("Belum ada aturan pada basis pengetahuan.")

with st.container(border=True):
    st.subheader("Batasan")
    st.write(
        "Aplikasi hanya menganalisis gejala yang diinput pengguna. Aplikasi tidak "
        "membaca memori game, tidak memodifikasi client game, dan tidak menyentuh "
        "proses game apa pun."
    )
    st.write(
        "Nilai CF pakar pada data awal masih berupa placeholder dan akan diganti "
        "dengan hasil wawancara pakar."
    )
    st.write(
        "Hasil analisis bersifat indikatif, bukan bukti mutlak. Keputusan akhir "
        "tetap memerlukan verifikasi pihak berwenang, misalnya GM atau sistem "
        "anti-cheat resmi."
    )
