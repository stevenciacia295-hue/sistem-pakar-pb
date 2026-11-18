"""Formulir penilaian pakar: skala keyakinan, penyimpanan, dan ringkasan."""

import json
from datetime import datetime

from src import knowledge

SKALA_PENILAIAN = [
    ("Tidak tahu", None),
    ("Tidak yakin", 0.2),
    ("Kurang yakin", 0.4),
    ("Cukup yakin", 0.6),
    ("Yakin", 0.8),
    ("Sangat yakin", 1.0),
]
LABEL_SKALA = [label for label, _nilai in SKALA_PENILAIAN]
NILAI_SKALA = dict(SKALA_PENILAIAN)
NILAI_SAH = {nilai for _label, nilai in SKALA_PENILAIAN}

PERAN_PAKAR = [
    "Admin/moderator komunitas",
    "Pemain tim e-sports",
    "Pemain senior/ranked tinggi",
    "Pengelola warnet",
    "Lainnya",
]
LAMA_BERMAIN = ["< 2 tahun", "2-4 tahun", "5-8 tahun", "> 8 tahun"]
PILIHAN_IZIN = ["Ya", "Hanya inisial"]
PILIHAN_HUBUNGI = ["Ya", "Tidak"]

ATURAN_FORM = [
    {
        "kode": "R01",
        "ciri": "Persentase headshot sangat tinggi dan konsisten antar ronde",
        "cheat": "AIMBOT",
    },
    {
        "kode": "R02",
        "ciri": "Crosshair langsung mengunci ke kepala tanpa gerakan mouse wajar",
        "cheat": "AIMBOT",
    },
    {
        "kode": "R03",
        "ciri": "Reaksi tembakan sangat cepat saat musuh baru muncul",
        "cheat": "AIMBOT",
    },
    {
        "kode": "R04",
        "ciri": "Akurasi tembakan sangat tinggi pada jarak jauh",
        "cheat": "AIMBOT",
    },
    {
        "kode": "R05",
        "ciri": "Membidik musuh di balik tembok sebelum musuh terlihat",
        "cheat": "WALLHACK",
    },
    {
        "kode": "R06",
        "ciri": "Selalu tahu posisi musuh dan flank tepat sasaran",
        "cheat": "WALLHACK",
    },
    {
        "kode": "R07",
        "ciri": (
            "Mengikuti pergerakan musuh di balik penghalang secara konsisten"
        ),
        "cheat": "WALLHACK",
    },
    {
        "kode": "R08",
        "ciri": "Pola tembakan full-auto selalu lurus tanpa recoil",
        "cheat": "NO RECOIL",
    },
    {
        "kode": "R09",
        "ciri": "Peluru hampir tidak menyebar saat menembak terus-menerus",
        "cheat": "NO RECOIL",
    },
    {
        "kode": "R10",
        "ciri": "Bergerak jauh lebih cepat dari pemain normal",
        "cheat": "SPEEDHACK",
    },
    {
        "kode": "R11",
        "ciri": "Berpindah posisi tiba-tiba seperti teleport",
        "cheat": "SPEEDHACK",
    },
    {
        "kode": "R12",
        "ciri": (
            "Senjata tetap stabil walau menembak sambil bergerak atau melompat"
        ),
        "cheat": "NO RECOIL",
    },
    {
        "kode": "R13",
        "ciri": "Senjata berhentakan besar terasa seperti senjata ringan",
        "cheat": "NO RECOIL",
    },
]
KODE_ATURAN_FORM = [aturan["kode"] for aturan in ATURAN_FORM]

_WAJIB = {
    "nama": "Nama lengkap",
    "peran": "Peran di komunitas",
    "lama_bermain": "Lama bermain atau berperan",
    "izin_nama": "Izin pencantuman nama",
    "pengalaman_ciri": "Ciri paling meyakinkan",
    "pengalaman_beda": "Cara membedakan pemain jago dan cheat",
    "pengalaman_mitos": "Ciri yang sering disangka cheat",
    "pengalaman_bukti": "Bukti yang biasa dipakai",
    "boleh_dihubungi": "Izin dihubungi kembali",
}


def nama_tampil(nama, izin_nama):
    """Nama yang dicantumkan sebagai sumber pakar (inisial bila diminta)."""
    nama = str(nama or "").strip()
    if izin_nama == "Hanya inisial":
        inisial = "".join(
            f"{bagian[0].upper()}." for bagian in nama.split() if bagian
        )
        return inisial or "(tanpa nama)"
    return nama or "(tanpa nama)"


def label_nilai(nilai):
    """Kembalikan label skala dari nilai CF pakar."""
    for label, angka in SKALA_PENILAIAN:
        if angka == nilai:
            return label
    return "Tidak tahu"


def validasi_data(data):
    """Validasi dan normalisasi data formulir penilaian pakar."""
    bersih = {}
    for kunci, label in _WAJIB.items():
        teks = str(data.get(kunci) or "").strip()
        if not teks:
            raise ValueError(f"{label} wajib diisi.")
        bersih[kunci] = teks
    bersih["rank"] = str(data.get("rank") or "").strip()
    bersih["ciri_lain"] = str(data.get("ciri_lain") or "").strip()
    bersih["cheat_lain"] = str(data.get("cheat_lain") or "").strip()

    if bersih["peran"] not in PERAN_PAKAR:
        raise ValueError("Pilihan peran tidak dikenali.")
    if bersih["lama_bermain"] not in LAMA_BERMAIN:
        raise ValueError("Pilihan lama bermain tidak dikenali.")
    if bersih["izin_nama"] not in PILIHAN_IZIN:
        raise ValueError("Pilihan izin nama tidak dikenali.")
    if bersih["boleh_dihubungi"] not in PILIHAN_HUBUNGI:
        raise ValueError("Pilihan izin dihubungi tidak dikenali.")

    masuk = data.get("penilaian") or {}
    penilaian = {}
    for kode in KODE_ATURAN_FORM:
        nilai = masuk.get(kode)
        if nilai not in NILAI_SAH:
            raise ValueError(f"Nilai penilaian {kode} tidak dikenali.")
        penilaian[kode] = nilai
    if not any(nilai is not None for nilai in penilaian.values()):
        raise ValueError("Isi minimal satu penilaian keyakinan.")
    bersih["penilaian"] = penilaian
    return bersih


def simpan_penilaian(conn, data):
    """Simpan penilaian pakar, buat sumber pakar, dan tautkan ke aturan dinilai."""
    data = validasi_data(data)
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    kursor = conn.execute(
        "INSERT INTO penilaian_pakar (waktu, nama, peran, lama_bermain, rank, "
        "izin_nama, pengalaman_ciri, pengalaman_beda, pengalaman_mitos, "
        "pengalaman_bukti, penilaian_json, ciri_lain, cheat_lain, "
        "boleh_dihubungi) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            waktu,
            data["nama"],
            data["peran"],
            data["lama_bermain"],
            data["rank"],
            data["izin_nama"],
            data["pengalaman_ciri"],
            data["pengalaman_beda"],
            data["pengalaman_mitos"],
            data["pengalaman_bukti"],
            json.dumps(data["penilaian"]),
            data["ciri_lain"],
            data["cheat_lain"],
            data["boleh_dihubungi"],
        ),
    )
    id_penilaian = kursor.lastrowid
    tampil = nama_tampil(data["nama"], data["izin_nama"])
    sitasi = (
        f"Penilaian pakar #{id_penilaian}: {tampil} "
        f"({data['peran']}; {data['lama_bermain']}), {waktu[:10]}."
    )
    id_sumber = knowledge.add_sumber(conn, "pakar", sitasi, "")
    for kode, nilai in data["penilaian"].items():
        if nilai is not None:
            knowledge.tautkan_sumber(conn, kode, id_sumber)
    conn.execute(
        "UPDATE penilaian_pakar SET id_sumber = ? WHERE id = ?",
        (id_sumber, id_penilaian),
    )
    return id_penilaian


def get_penilaian(conn):
    """Kembalikan seluruh penilaian pakar terbaru lebih dulu."""
    hasil = []
    for baris in conn.execute("SELECT * FROM penilaian_pakar ORDER BY id DESC"):
        item = dict(baris)
        item["penilaian"] = json.loads(item["penilaian_json"])
        item["nama_tampil"] = nama_tampil(item["nama"], item["izin_nama"])
        hasil.append(item)
    return hasil


def get_penilaian_by_id(conn, id_penilaian):
    """Ambil satu penilaian pakar berdasarkan id."""
    baris = conn.execute(
        "SELECT * FROM penilaian_pakar WHERE id = ?", (int(id_penilaian),)
    ).fetchone()
    if not baris:
        return None
    item = dict(baris)
    item["penilaian"] = json.loads(item["penilaian_json"])
    item["nama_tampil"] = nama_tampil(item["nama"], item["izin_nama"])
    return item


def ringkasan_cf(conn):
    """Hitung rata-rata CF pakar per aturan dari seluruh penilaian."""
    daftar = get_penilaian(conn)
    ringkasan = []
    for aturan in ATURAN_FORM:
        nilai = [
            item["penilaian"].get(aturan["kode"]) for item in daftar
        ]
        nilai = [angka for angka in nilai if angka is not None]
        rata = sum(nilai) / len(nilai) if nilai else None
        ringkasan.append(
            {
                "kode": aturan["kode"],
                "ciri": aturan["ciri"],
                "cheat": aturan["cheat"],
                "rata_rata": rata,
                "jumlah": len(nilai),
            }
        )
    return ringkasan


def hapus_penilaian(conn, id_penilaian):
    """Hapus penilaian beserta sumber pakar yang dibuat darinya."""
    baris = conn.execute(
        "SELECT id_sumber FROM penilaian_pakar WHERE id = ?",
        (int(id_penilaian),),
    ).fetchone()
    if not baris:
        raise ValueError("Penilaian tidak ditemukan.")
    id_sumber = baris["id_sumber"]
    conn.execute(
        "DELETE FROM penilaian_pakar WHERE id = ?", (int(id_penilaian),)
    )
    if id_sumber is not None:
        try:
            knowledge.delete_sumber(conn, id_sumber)
        except ValueError:
            pass
