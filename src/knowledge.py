"""Basis pengetahuan sistem pakar: data awal, pengambilan data, dan CRUD."""

CHEAT_AWAL = [
    {
        "kode": "C01",
        "nama": "Aimbot",
        "deskripsi": (
            "Program bantuan yang mengarahkan tembakan secara otomatis ke titik "
            "lemah musuh, biasanya kepala, tanpa usaha membidik manual."
        ),
        "saran": (
            "Rekam ulang pertandingan pemain, bandingkan headshot rate dengan "
            "rata-rata pemain wajar, lalu laporkan ke GM dengan bukti video."
        ),
    },
    {
        "kode": "C02",
        "nama": "Wallhack",
        "deskripsi": (
            "Bantuan visual yang menampilkan posisi musuh di balik tembok atau "
            "penghalang sehingga pemain selalu tahu keberadaan lawan."
        ),
        "saran": (
            "Amati pola pre-aim dan pelacakan musuh yang tidak terlihat, minta "
            "rekaman POV, lalu laporkan ke GM dengan bukti video."
        ),
    },
    {
        "kode": "C03",
        "nama": "No Recoil",
        "deskripsi": (
            "Modifikasi yang menghilangkan recoil senjata sehingga pola tembakan "
            "full-auto tetap lurus dan terkonsentrasi di satu titik."
        ),
        "saran": (
            "Bandingkan pola spray pemain dengan senjata dan jarak yang sama "
            "pada pemain wajar, lalu laporkan bila hasilnya tidak wajar."
        ),
    },
    {
        "kode": "C04",
        "nama": "Speedhack",
        "deskripsi": (
            "Modifikasi kecepatan gerak sehingga pemain berpindah posisi jauh "
            "lebih cepat daripada batas normal permainan."
        ),
        "saran": (
            "Ukur waktu berpindah posisi pemain antar titik peta, rekam "
            "bukti videonya, lalu laporkan ke GM."
        ),
    },
]

GEJALA_AWAL = [
    {"kode": "G01", "deskripsi": "headshot rate sangat tinggi dan konsisten"},
    {"kode": "G02", "deskripsi": "crosshair langsung mengunci kepala"},
    {"kode": "G03", "deskripsi": "reaksi tembakan sangat cepat"},
    {"kode": "G04", "deskripsi": "akurasi jarak jauh sangat tinggi"},
    {"kode": "G05", "deskripsi": "membidik musuh di balik tembok"},
    {"kode": "G06", "deskripsi": "selalu tahu posisi musuh"},
    {"kode": "G07", "deskripsi": "mengikuti musuh di balik penghalang"},
    {"kode": "G08", "deskripsi": "pola full-auto selalu lurus"},
    {"kode": "G09", "deskripsi": "peluru hampir tidak menyebar"},
    {"kode": "G10", "deskripsi": "bergerak jauh lebih cepat"},
    {"kode": "G11", "deskripsi": "berpindah posisi seperti teleport"},
    {
        "kode": "G12",
        "deskripsi": (
            "senjata tetap stabil walau menembak sambil bergerak atau melompat"
        ),
    },
    {
        "kode": "G13",
        "deskripsi": (
            "senjata dengan hentakan besar terasa seperti senjata ringan saat "
            "ditembakkan"
        ),
    },
]

GEJALA_TAMBAHAN = [gejala for gejala in GEJALA_AWAL if gejala["kode"] in ("G12", "G13")]

ATURAN_AWAL = [
    {"kode": "R01", "kode_cheat": "C01", "kode_gejala": "G01", "cf_pakar": 0.7},
    {"kode": "R02", "kode_cheat": "C01", "kode_gejala": "G02", "cf_pakar": 0.9},
    {"kode": "R03", "kode_cheat": "C01", "kode_gejala": "G03", "cf_pakar": 0.6},
    {"kode": "R04", "kode_cheat": "C01", "kode_gejala": "G04", "cf_pakar": 0.5},
    {"kode": "R05", "kode_cheat": "C02", "kode_gejala": "G05", "cf_pakar": 0.8},
    {"kode": "R06", "kode_cheat": "C02", "kode_gejala": "G06", "cf_pakar": 0.7},
    {"kode": "R07", "kode_cheat": "C02", "kode_gejala": "G07", "cf_pakar": 0.9},
    {"kode": "R08", "kode_cheat": "C03", "kode_gejala": "G08", "cf_pakar": 0.9},
    {"kode": "R09", "kode_cheat": "C03", "kode_gejala": "G09", "cf_pakar": 0.8},
    {"kode": "R10", "kode_cheat": "C04", "kode_gejala": "G10", "cf_pakar": 0.8},
    {"kode": "R11", "kode_cheat": "C04", "kode_gejala": "G11", "cf_pakar": 0.9},
    {"kode": "R12", "kode_cheat": "C03", "kode_gejala": "G12", "cf_pakar": 0.7},
    {"kode": "R13", "kode_cheat": "C03", "kode_gejala": "G13", "cf_pakar": 0.8},
]

ATURAN_TAMBAHAN = [aturan for aturan in ATURAN_AWAL if aturan["kode"] in ("R12", "R13")]

for _aturan in ATURAN_AWAL:
    _aturan["nama_pakar"] = "Belum diisi"
    _aturan["tanggal_wawancara"] = "Belum diisi"


SUMBER_AWAL = [
    {
        "jenis": "jurnal",
        "sitasi": (
            "Yu, Hammerla, Yan, Andras (2012). A statistical aimbot detection "
            "method for online FPS games. IJCNN 2012."
        ),
        "url_doi": "10.1109/IJCNN.2012.6252489",
    },
    {
        "jenis": "jurnal",
        "sitasi": "Choi, Ko, Cha (2023). BotScreen. USENIX Security 2023.",
        "url_doi": "",
    },
    {
        "jenis": "jurnal",
        "sitasi": (
            "Yan & Randell (2005). A systematic classification of cheating in "
            "online games. NetGames 2005."
        ),
        "url_doi": "10.1145/1103599.1103606",
    },
    {
        "jenis": "jurnal",
        "sitasi": (
            "Yan & Randell (2009). An investigation of cheating in online "
            "games. IEEE Security & Privacy 7(3)."
        ),
        "url_doi": "10.1109/MSP.2009.60",
    },
    {
        "jenis": "praktisi",
        "sitasi": "Pengamatan praktisi. Perlu validasi pakar.",
        "url_doi": "",
    },
]

_TAUTAN_SUMBER_AWAL = {
    "R01": [0, 1, 2, 3],
    "R02": [0, 1, 2, 3],
    "R03": [2, 3, 4],
    "R04": [0, 1, 2, 3],
    "R05": [2, 3, 4],
    "R06": [2, 3, 4],
    "R07": [2, 3, 4],
    "R08": [2, 3, 4],
    "R09": [2, 3, 4],
    "R10": [2, 3, 4],
    "R11": [2, 3, 4],
    "R12": [2, 3, 4],
    "R13": [2, 3, 4],
}

JENIS_SUMBER = ("jurnal", "pakar", "praktisi")


def seed_if_empty(conn):
    """Isi data awal bila kosong, lalu terapkan migrasi konten terbaru. Idempoten."""
    kosong = not (
        _jumlah(conn, "cheat") or _jumlah(conn, "gejala") or _jumlah(conn, "aturan")
    )
    if kosong:
        conn.executemany(
            "INSERT OR IGNORE INTO cheat (kode, nama, deskripsi, saran) "
            "VALUES (?, ?, ?, ?)",
            [(c["kode"], c["nama"], c["deskripsi"], c["saran"]) for c in CHEAT_AWAL],
        )
        conn.executemany(
            "INSERT OR IGNORE INTO gejala (kode, deskripsi) VALUES (?, ?)",
            [(g["kode"], g["deskripsi"]) for g in GEJALA_AWAL],
        )
        conn.executemany(
            "INSERT OR IGNORE INTO aturan (kode, kode_cheat, kode_gejala, "
            "cf_pakar, nama_pakar, tanggal_wawancara) VALUES (?, ?, ?, ?, ?, ?)",
            [
                (
                    a["kode"],
                    a["kode_cheat"],
                    a["kode_gejala"],
                    a["cf_pakar"],
                    a["nama_pakar"],
                    a["tanggal_wawancara"],
                )
                for a in ATURAN_AWAL
            ],
        )
    _migrasi_konten(conn)
    seed_sumber(conn)
    return kosong


def _migrasi_konten(conn):
    """Tambahkan gejala dan aturan No Recoil baru tanpa menghapus data lama."""
    conn.executemany(
        "INSERT OR IGNORE INTO gejala (kode, deskripsi) VALUES (?, ?)",
        [(g["kode"], g["deskripsi"]) for g in GEJALA_TAMBAHAN],
    )
    if not _kode_ada(conn, "cheat", "C03"):
        return
    conn.executemany(
        "INSERT OR IGNORE INTO aturan (kode, kode_cheat, kode_gejala, cf_pakar, "
        "nama_pakar, tanggal_wawancara) VALUES (?, ?, ?, ?, ?, ?)",
        [
            (
                a["kode"],
                a["kode_cheat"],
                a["kode_gejala"],
                a["cf_pakar"],
                a["nama_pakar"],
                a["tanggal_wawancara"],
            )
            for a in ATURAN_TAMBAHAN
        ],
    )


def seed_sumber(conn):
    """Isi sumber awal dan tautannya bila tabel sumber masih kosong."""
    if _jumlah(conn, "sumber"):
        return False
    for sumber in SUMBER_AWAL:
        conn.execute(
            "INSERT OR IGNORE INTO sumber (jenis, sitasi, url_doi) "
            "VALUES (?, ?, ?)",
            (sumber["jenis"], sumber["sitasi"], sumber["url_doi"]),
        )
    peta_id = {
        baris["sitasi"]: baris["id"]
        for baris in conn.execute("SELECT id, sitasi FROM sumber")
    }
    for kode_aturan, indeks in _TAUTAN_SUMBER_AWAL.items():
        if not _kode_ada(conn, "aturan", kode_aturan):
            continue
        for posisi in indeks:
            id_sumber = peta_id.get(SUMBER_AWAL[posisi]["sitasi"])
            if id_sumber is None:
                continue
            conn.execute(
                "INSERT OR IGNORE INTO aturan_sumber (kode_aturan, id_sumber) "
                "VALUES (?, ?)",
                (kode_aturan, id_sumber),
            )
    return True


def get_cheats(conn):
    """Kembalikan seluruh cheat sebagai list of dict, terurut berdasarkan kode."""
    return [dict(row) for row in conn.execute("SELECT * FROM cheat ORDER BY kode")]


def get_gejala(conn):
    """Kembalikan seluruh gejala sebagai list of dict, terurut berdasarkan kode."""
    return [dict(row) for row in conn.execute("SELECT * FROM gejala ORDER BY kode")]


def get_aturan(conn):
    """Kembalikan seluruh aturan sebagai list of dict, terurut berdasarkan kode."""
    return [dict(row) for row in conn.execute("SELECT * FROM aturan ORDER BY kode")]


def ringkasan_pakar(conn):
    """Hitung jumlah aturan per pakar, terurut dari yang terbanyak."""
    baris = conn.execute(
        "SELECT nama_pakar, COUNT(*) AS jumlah FROM aturan "
        "GROUP BY nama_pakar ORDER BY jumlah DESC, nama_pakar"
    )
    return [
        {"nama_pakar": row["nama_pakar"], "jumlah": row["jumlah"]} for row in baris
    ]


def get_sumber(conn):
    """Kembalikan seluruh sumber pengetahuan terurut berdasarkan id."""
    return [dict(row) for row in conn.execute("SELECT * FROM sumber ORDER BY id")]


def get_sumber_aturan(conn, kode_aturan):
    """Kembalikan sumber yang tertaut ke satu aturan."""
    baris = conn.execute(
        "SELECT s.* FROM sumber s JOIN aturan_sumber a ON a.id_sumber = s.id "
        "WHERE a.kode_aturan = ? ORDER BY s.id",
        (kode_aturan,),
    )
    return [dict(row) for row in baris]


def peta_sumber_aturan(conn):
    """Petakan kode aturan ke daftar sumbernya."""
    peta = {}
    baris = conn.execute(
        "SELECT a.kode_aturan, s.id, s.jenis, s.sitasi, s.url_doi "
        "FROM aturan_sumber a JOIN sumber s ON s.id = a.id_sumber "
        "ORDER BY a.kode_aturan, s.id"
    )
    for row in baris:
        peta.setdefault(row["kode_aturan"], []).append(
            {
                "id": row["id"],
                "jenis": row["jenis"],
                "sitasi": row["sitasi"],
                "url_doi": row["url_doi"],
            }
        )
    return peta


def validasi_cf_pakar(nilai):
    """Validasi CF pakar: harus angka di antara 0 dan 1."""
    try:
        cf = float(nilai)
    except (TypeError, ValueError):
        raise ValueError("CF pakar harus berupa angka.")
    if not 0 <= cf <= 1:
        raise ValueError("CF pakar harus di antara 0 dan 1.")
    return cf


def add_cheat(conn, kode, nama, deskripsi="", saran=""):
    """Tambah cheat baru."""
    kode = _teks_wajib(kode, "Kode cheat")
    nama = _teks_wajib(nama, "Nama cheat")
    if _kode_ada(conn, "cheat", kode):
        raise ValueError(f"Kode cheat {kode} sudah ada.")
    conn.execute(
        "INSERT INTO cheat (kode, nama, deskripsi, saran) VALUES (?, ?, ?, ?)",
        (kode, nama, deskripsi, saran),
    )


def update_cheat(conn, kode, nama, deskripsi, saran):
    """Ubah nama, deskripsi, dan saran cheat."""
    nama = _teks_wajib(nama, "Nama cheat")
    if not _kode_ada(conn, "cheat", kode):
        raise ValueError(f"Cheat {kode} tidak ditemukan.")
    conn.execute(
        "UPDATE cheat SET nama = ?, deskripsi = ?, saran = ? WHERE kode = ?",
        (nama, deskripsi, saran, kode),
    )


def delete_cheat(conn, kode):
    """Hapus cheat; aturan terkait ikut terhapus (ON DELETE CASCADE)."""
    if not _kode_ada(conn, "cheat", kode):
        raise ValueError(f"Cheat {kode} tidak ditemukan.")
    conn.execute("DELETE FROM cheat WHERE kode = ?", (kode,))


def add_gejala(conn, kode, deskripsi):
    """Tambah gejala baru."""
    kode = _teks_wajib(kode, "Kode gejala")
    deskripsi = _teks_wajib(deskripsi, "Deskripsi gejala")
    if _kode_ada(conn, "gejala", kode):
        raise ValueError(f"Kode gejala {kode} sudah ada.")
    conn.execute("INSERT INTO gejala (kode, deskripsi) VALUES (?, ?)", (kode, deskripsi))


def update_gejala(conn, kode, deskripsi):
    """Ubah deskripsi gejala."""
    deskripsi = _teks_wajib(deskripsi, "Deskripsi gejala")
    if not _kode_ada(conn, "gejala", kode):
        raise ValueError(f"Gejala {kode} tidak ditemukan.")
    conn.execute("UPDATE gejala SET deskripsi = ? WHERE kode = ?", (deskripsi, kode))


def delete_gejala(conn, kode):
    """Hapus gejala; aturan terkait ikut terhapus (ON DELETE CASCADE)."""
    if not _kode_ada(conn, "gejala", kode):
        raise ValueError(f"Gejala {kode} tidak ditemukan.")
    conn.execute("DELETE FROM gejala WHERE kode = ?", (kode,))


def add_aturan(
    conn,
    kode,
    kode_cheat,
    kode_gejala,
    cf_pakar,
    nama_pakar="Belum diisi",
    tanggal_wawancara="Belum diisi",
):
    """Tambah aturan baru; kode cheat dan kode gejala harus sudah ada."""
    kode = _teks_wajib(kode, "Kode aturan")
    kode_cheat = _teks_wajib(kode_cheat, "Kode cheat")
    kode_gejala = _teks_wajib(kode_gejala, "Kode gejala")
    cf = validasi_cf_pakar(cf_pakar)
    if _kode_ada(conn, "aturan", kode):
        raise ValueError(f"Kode aturan {kode} sudah ada.")
    if not _kode_ada(conn, "cheat", kode_cheat):
        raise ValueError(f"Cheat {kode_cheat} tidak ditemukan.")
    if not _kode_ada(conn, "gejala", kode_gejala):
        raise ValueError(f"Gejala {kode_gejala} tidak ditemukan.")
    conn.execute(
        "INSERT INTO aturan (kode, kode_cheat, kode_gejala, cf_pakar, "
        "nama_pakar, tanggal_wawancara) VALUES (?, ?, ?, ?, ?, ?)",
        (
            kode,
            kode_cheat,
            kode_gejala,
            cf,
            _teks_pakar(nama_pakar),
            _teks_pakar(tanggal_wawancara),
        ),
    )


def update_aturan(
    conn,
    kode,
    kode_cheat,
    kode_gejala,
    cf_pakar,
    nama_pakar="Belum diisi",
    tanggal_wawancara="Belum diisi",
):
    """Ubah relasi cheat-gejala, CF pakar, dan sumber pakar sebuah aturan."""
    kode_cheat = _teks_wajib(kode_cheat, "Kode cheat")
    kode_gejala = _teks_wajib(kode_gejala, "Kode gejala")
    cf = validasi_cf_pakar(cf_pakar)
    if not _kode_ada(conn, "aturan", kode):
        raise ValueError(f"Aturan {kode} tidak ditemukan.")
    if not _kode_ada(conn, "cheat", kode_cheat):
        raise ValueError(f"Cheat {kode_cheat} tidak ditemukan.")
    if not _kode_ada(conn, "gejala", kode_gejala):
        raise ValueError(f"Gejala {kode_gejala} tidak ditemukan.")
    conn.execute(
        "UPDATE aturan SET kode_cheat = ?, kode_gejala = ?, cf_pakar = ?, "
        "nama_pakar = ?, tanggal_wawancara = ? WHERE kode = ?",
        (
            kode_cheat,
            kode_gejala,
            cf,
            _teks_pakar(nama_pakar),
            _teks_pakar(tanggal_wawancara),
            kode,
        ),
    )


def delete_aturan(conn, kode):
    """Hapus aturan."""
    if not _kode_ada(conn, "aturan", kode):
        raise ValueError(f"Aturan {kode} tidak ditemukan.")
    conn.execute("DELETE FROM aturan WHERE kode = ?", (kode,))


def add_sumber(conn, jenis, sitasi, url_doi=""):
    """Tambah sumber pengetahuan baru."""
    jenis, sitasi = _validasi_sumber(jenis, sitasi)
    if conn.execute("SELECT 1 FROM sumber WHERE sitasi = ?", (sitasi,)).fetchone():
        raise ValueError("Sitasi sumber sudah ada.")
    kursor = conn.execute(
        "INSERT INTO sumber (jenis, sitasi, url_doi) VALUES (?, ?, ?)",
        (jenis, sitasi, str(url_doi or "").strip()),
    )
    return kursor.lastrowid


def update_sumber(conn, id_sumber, jenis, sitasi, url_doi=""):
    """Ubah jenis, sitasi, dan tautan sebuah sumber."""
    jenis, sitasi = _validasi_sumber(jenis, sitasi)
    if not _sumber_ada(conn, id_sumber):
        raise ValueError("Sumber tidak ditemukan.")
    bentrok = conn.execute(
        "SELECT 1 FROM sumber WHERE sitasi = ? AND id <> ?",
        (sitasi, int(id_sumber)),
    ).fetchone()
    if bentrok:
        raise ValueError("Sitasi sumber sudah ada.")
    conn.execute(
        "UPDATE sumber SET jenis = ?, sitasi = ?, url_doi = ? WHERE id = ?",
        (jenis, sitasi, str(url_doi or "").strip(), int(id_sumber)),
    )


def delete_sumber(conn, id_sumber):
    """Hapus sumber; tautan ke aturan ikut terhapus (ON DELETE CASCADE)."""
    if not _sumber_ada(conn, id_sumber):
        raise ValueError("Sumber tidak ditemukan.")
    conn.execute("DELETE FROM sumber WHERE id = ?", (int(id_sumber),))


def set_sumber_aturan(conn, kode_aturan, daftar_id):
    """Ganti seluruh tautan sumber untuk satu aturan."""
    if not _kode_ada(conn, "aturan", kode_aturan):
        raise ValueError(f"Aturan {kode_aturan} tidak ditemukan.")
    id_bersih = []
    for id_sumber in daftar_id:
        if not _sumber_ada(conn, id_sumber):
            raise ValueError(f"Sumber {id_sumber} tidak ditemukan.")
        id_bersih.append(int(id_sumber))
    conn.execute("DELETE FROM aturan_sumber WHERE kode_aturan = ?", (kode_aturan,))
    conn.executemany(
        "INSERT OR IGNORE INTO aturan_sumber (kode_aturan, id_sumber) VALUES (?, ?)",
        [(kode_aturan, id_sumber) for id_sumber in id_bersih],
    )


def tautkan_sumber(conn, kode_aturan, id_sumber):
    """Tambahkan satu tautan sumber ke aturan tanpa menghapus tautan lain."""
    if not _kode_ada(conn, "aturan", kode_aturan):
        raise ValueError(f"Aturan {kode_aturan} tidak ditemukan.")
    if not _sumber_ada(conn, id_sumber):
        raise ValueError(f"Sumber {id_sumber} tidak ditemukan.")
    conn.execute(
        "INSERT OR IGNORE INTO aturan_sumber (kode_aturan, id_sumber) "
        "VALUES (?, ?)",
        (kode_aturan, int(id_sumber)),
    )


def _validasi_sumber(jenis, sitasi):
    jenis = str(jenis).strip().lower() if jenis is not None else ""
    if jenis not in JENIS_SUMBER:
        raise ValueError("Jenis sumber harus jurnal, pakar, atau praktisi.")
    return jenis, _teks_wajib(sitasi, "Sitasi")


def _sumber_ada(conn, id_sumber):
    try:
        id_sumber = int(id_sumber)
    except (TypeError, ValueError):
        return False
    return conn.execute("SELECT 1 FROM sumber WHERE id = ?", (id_sumber,)).fetchone() is not None


def _jumlah(conn, tabel):
    return conn.execute(f"SELECT COUNT(*) FROM {tabel}").fetchone()[0]


def _kode_ada(conn, tabel, kode):
    return conn.execute(f"SELECT 1 FROM {tabel} WHERE kode = ?", (kode,)).fetchone() is not None


def _teks_wajib(nilai, label):
    teks = str(nilai).strip() if nilai is not None else ""
    if not teks:
        raise ValueError(f"{label} wajib diisi.")
    return teks


def _teks_pakar(nilai):
    teks = str(nilai).strip() if nilai is not None else ""
    return teks or "Belum diisi"
