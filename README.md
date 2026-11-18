# Sistem Pakar Deteksi Kecurangan Point Blank

Aplikasi web berbahasa Indonesia untuk menganalisis indikasi penggunaan cheat
pada game Point Blank menggunakan metode **Forward Chaining** dan
**Certainty Factor (CF)**.

Pengguna menjawab pertanyaan PB-Bot tentang gejala yang diamati pada pemain
yang dicurigai, lalu sistem menghitung jenis cheat yang paling mungkin beserta
persentase keyakinan, penjelasan perhitungan, dan saran tindakan.

Aplikasi hanya menganalisis gejala yang diinput pengguna. Aplikasi tidak
membaca memori game, tidak memodifikasi client game, dan tidak menyentuh
proses game apa pun.

## Tampilan dan pendekatan expert system

Antarmuka **PB Expert AI** memakai konsol analisis profesional bertema gelap
dengan aksen violet dan cyan. Halaman utama menampilkan status inference
engine, statistik basis pengetahuan, pipeline penalaran, dan ringkasan
kapabilitas sistem pakar.

Halaman **Diagnosa** berfungsi sebagai expert system console:

- menampilkan status sesi, fakta aktif, progres wawancara, dan model FC + CF,
- merekam jawaban Iya sebagai fakta pada working memory,
- menampilkan aturan yang terpicu beserta CF pengguna, CF pakar, CF aturan,
  CF sebelum, dan CF sesudah agregasi,
- menyediakan jejak inferensi dan penjelasan hasil yang dapat diaudit,
- menyertakan sumber ilmiah untuk setiap aturan yang mendukung kesimpulan.

Halaman **Tentang** menjelaskan arsitektur sistem pakar, forward chaining,
certainty factor, keterlacakan hasil, dan peran manusia dalam keputusan akhir.

## Login pengguna

Seluruh halaman dilindungi login pengguna umum. Nama pengguna boleh diisi
bebas (misalnya `nesaa` atau `steven`), sedangkan kata sandi awal adalah
`1234`. Ganti kata sandi lewat variabel lingkungan `APP_PASSWORD` atau kunci
`APP_PASSWORD` pada `st.secrets`. Tombol **Keluar** di sidebar mengakhiri sesi
pengguna sekaligus sesi admin.

Kata sandi admin untuk halaman Kelola Pengetahuan tetap terpisah dan memakai
`ADMIN_PASSWORD`.

## Metode

### Forward Chaining

Forward chaining bergerak dari fakta menuju kesimpulan. Fakta berupa gejala
yang dipilih pengguna dicocokkan dengan aturan basis pengetahuan (jika gejala
muncul maka jenis cheat tertentu mungkin terjadi). Seluruh aturan yang cocok
dieksekusi dan hasilnya digabungkan per jenis cheat.

### Certainty Factor

CF menyatakan tingkat keyakinan dalam rentang 0 sampai 1.

```
CF aturan   = CF pengguna x CF pakar
CF gabungan = CF lama + CF baru x (1 - CF lama)
Persentase  = CF gabungan x 100
```

Skala jawaban chatbot: Iya (1.0) dan Tidak (0.0). Jawaban Tidak tidak
mengaktifkan aturan gejala tersebut. Mesin inferensi tetap menerima nilai CF
pengguna mana pun dalam rentang 0 sampai 1.

Kategori hasil:

- 80 persen atau lebih: Sangat mungkin
- 50 sampai 79 persen: Mungkin
- Kurang dari 50 persen: Kemungkinan kecil

## Data awal

### Cheat

| Kode | Nama |
|------|------|
| C01 | Aimbot |
| C02 | Wallhack |
| C03 | No Recoil |
| C04 | Speedhack |

### Gejala

| Kode | Gejala |
|------|--------|
| G01 | headshot rate sangat tinggi dan konsisten |
| G02 | crosshair langsung mengunci kepala |
| G03 | reaksi tembakan sangat cepat |
| G04 | akurasi jarak jauh sangat tinggi |
| G05 | membidik musuh di balik tembok |
| G06 | selalu tahu posisi musuh |
| G07 | mengikuti musuh di balik penghalang |
| G08 | pola full-auto selalu lurus |
| G09 | peluru hampir tidak menyebar |
| G10 | bergerak jauh lebih cepat |
| G11 | berpindah posisi seperti teleport |
| G12 | senjata tetap stabil walau menembak sambil bergerak atau melompat |
| G13 | senjata dengan hentakan besar terasa seperti senjata ringan |

### Aturan (CF pakar)

| Kode | Cheat | Gejala | CF pakar |
|------|-------|--------|----------|
| R01 | C01 | G01 | 0.7 |
| R02 | C01 | G02 | 0.9 |
| R03 | C01 | G03 | 0.6 |
| R04 | C01 | G04 | 0.5 |
| R05 | C02 | G05 | 0.8 |
| R06 | C02 | G06 | 0.7 |
| R07 | C02 | G07 | 0.9 |
| R08 | C03 | G08 | 0.9 |
| R09 | C03 | G09 | 0.8 |
| R10 | C04 | G10 | 0.8 |
| R11 | C04 | G11 | 0.9 |
| R12 | C03 | G12 | 0.7 |
| R13 | C03 | G13 | 0.8 |

Nilai CF pakar di atas masih berupa placeholder dan akan diganti dengan hasil
wawancara pakar.

## Materi percakapan

PB-Bot memakai sapaan, respons, dan penutup acak, serta lima varian pertanyaan
untuk setiap gejala (G01 sampai G13). Materi tersebut berada di
`src/percakapan.py` dan tidak bergantung pada Streamlit.

Percakapan berhenti lebih awal bila sudah ada cheat dengan persentase minimal
85 persen setelah sedikitnya 3 jawaban, bila sudah 8 pertanyaan, atau bila
semua gejala sudah ditanyakan. Aturan ini ada di `src/chatbot.py`.

Label **Sangat mungkin** hanya diberikan kepada cheat dengan persentase
tertinggi. Cheat lain yang masih 80 persen atau lebih diberi label **Mungkin**.
Bila tiga cheat atau lebih berada di 80 persen atau lebih, aplikasi menampilkan
peringatan bahwa jawaban cenderung tidak konsisten.

## Halaman Panduan Gejala

Halaman **Panduan Gejala** menampilkan seluruh gejala dari basis data beserta:

- penjelasan apa yang dimaksud dengan gejala tersebut,
- kemungkinan penyebabnya, termasuk kemungkinan skill, ping, atau bug,
- lima varian pertanyaan yang dipakai PB-Bot,
- pilihan jawaban beserta nilai CF dan artinya,
- langkah penyelesaian dan verifikasi,
- aturan serta cheat yang terkait.

Isi panduan berada di `src/panduan.py`. Halaman tetap menampilkan panduan umum
untuk gejala baru yang ditambahkan admin tetapi belum memiliki panduan khusus.

## Struktur proyek

```
sistem-pakar-pb/
├── app.py
├── requirements.txt
├── pytest.ini
├── .streamlit/
│   └── config.toml
├── src/
│   ├── db.py
│   ├── knowledge.py
│   ├── engine.py
│   ├── explain.py
│   ├── history.py
│   ├── chatbot.py
│   ├── percakapan.py
│   ├── laporan_pdf.py
│   ├── penilaian.py
│   ├── akun.py
│   ├── auth.py
│   └── panduan.py
├── pages/
│   ├── 1_Diagnosa.py
│   ├── 2_Riwayat.py
│   ├── 3_Kelola_Pengetahuan.py
│   ├── 4_Tentang.py
│   ├── 5_Pengujian.py
│   ├── 6_Referensi.py
│   ├── 7_Penilaian_Pakar.py
│   └── 8_Panduan_Gejala.py
├── data/
│   ├── pbexpert.db
│   ├── pertanyaan.json
│   └── skenario_uji.json
└── tests/
    ├── test_engine.py
    ├── test_explain.py
    ├── test_chatbot.py
    ├── test_db.py
    ├── test_percakapan.py
    ├── test_skenario.py
    ├── test_pdf.py
    ├── test_penilaian.py
    ├── test_akun.py
    └── test_panduan.py
```

Seluruh logika bisnis (basis pengetahuan, mesin inferensi, penjelasan, riwayat)
berupa fungsi murni tanpa impor Streamlit.

## Skema database

Basis data SQLite dibuat otomatis di `data/pbexpert.db`.

```sql
CREATE TABLE cheat (
    kode      TEXT PRIMARY KEY,
    nama      TEXT NOT NULL,
    deskripsi TEXT NOT NULL DEFAULT '',
    saran     TEXT NOT NULL DEFAULT ''
);

CREATE TABLE gejala (
    kode      TEXT PRIMARY KEY,
    deskripsi TEXT NOT NULL
);

CREATE TABLE aturan (
    kode        TEXT PRIMARY KEY,
    kode_cheat  TEXT NOT NULL REFERENCES cheat(kode) ON DELETE CASCADE,
    kode_gejala TEXT NOT NULL REFERENCES gejala(kode) ON DELETE CASCADE,
    cf_pakar    REAL NOT NULL CHECK (cf_pakar >= 0 AND cf_pakar <= 1)
);

CREATE TABLE riwayat (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    waktu       TEXT NOT NULL,
    nama_pemain TEXT,
    input_json  TEXT NOT NULL,
    hasil_json  TEXT NOT NULL
);
```

## Menjalankan aplikasi

```powershell
pip install -r requirements.txt
streamlit run app.py
```

Buka `http://localhost:8501` bila peramban tidak terbuka otomatis.

## Menjalankan tes

```powershell
python -m pytest
```

## Halaman Kelola Pengetahuan

Halaman ini memakai form login dengan kata sandi dari `ADMIN_PASSWORD`
(variabel lingkungan) atau `ADMIN_PASSWORD` pada `st.secrets`. Bila keduanya
tidak tersedia, kata sandi default adalah `nesaa` dan halaman menampilkan
peringatan "Password default, segera ganti". Status login disimpan pada sesi
dan dapat diakhiri lewat tombol Keluar.

Tabel aturan menyimpan kolom `nama_pakar` dan `tanggal_wawancara`. Database
lama dimigrasi otomatis dengan nilai awal "Belum diisi".

## Halaman Pengujian

Halaman Pengujian menjalankan skenario dari `data/skenario_uji.json`,
menghitung hasil sistem dengan mesin inferensi, membandingkannya dengan
perhitungan manual (toleransi 0,01), lalu menampilkan status lulus/gagal dan
tombol unduh CSV. Berkas skenario dapat diedit tanpa mengubah kode.

## Contoh perhitungan

Input gejala G02 dengan keyakinan 1.0 dan G01 dengan keyakinan 0.8:

```
G02: CF aturan = 1.0 x 0.9 = 0.90
G01: CF aturan = 0.8 x 0.7 = 0.56
Gabungan      = 0.90 + 0.56 x (1 - 0.90) = 0.956
Persentase    = 0.956 x 100 = 95.6 persen
```

Hasil: **Aimbot 95.6 persen (Sangat mungkin)**. Contoh ini juga diuji otomatis
pada `tests/test_engine.py`.

## Batasan

- Hanya menganalisis gejala yang diinput pengguna.
- Tidak membaca memori game, tidak memodifikasi client game, dan tidak
  menyentuh proses game apa pun.
- Hasil bersifat indikatif, bukan bukti mutlak; keputusan akhir tetap
  memerlukan verifikasi pihak berwenang.
- Nilai CF pakar masih placeholder sampai wawancara pakar dilakukan.
