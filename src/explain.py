"""Penyusun penjelasan hasil diagnosa dalam bahasa Indonesia (fungsi murni)."""

PERINGATAN_TIDAK_KONSISTEN = (
    "Jawaban cenderung tidak konsisten, banyak gejala dijawab tinggi sekaligus. "
    "Periksa kembali pengamatanmu."
)

CATATAN_INDIKASI = (
    "Catatan: ini indikasi dari pengamatanmu, bukan bukti pasti."
)

_FRASA_KATEGORI = {
    "Sangat mungkin": "kemungkinan besar",
    "Mungkin": "kemungkinan",
    "Kemungkinan kecil": "kemungkinan kecil",
}


def frasa_kategori(item):
    """Ubah label kategori menjadi frasa kalimat."""
    return _FRASA_KATEGORI.get(item.get("kategori"), "kemungkinan")


def judul_hasil(item):
    """Judul hasil bergaya laporan, misalnya 'Kemungkinan besar memakai Aimbot (89.0%)'."""
    frasa = frasa_kategori(item)
    return (
        f"{frasa[:1].upper()}{frasa[1:]} memakai {item['nama']} "
        f"({format_persen(item['persen'])})"
    )


def arti_hasil(item):
    """Kalimat arti hasil berdasarkan deskripsi cheat."""
    return (
        f"Artinya: dari pengamatanmu, pemain ini {frasa_kategori(item)} "
        f"memakai {item['nama']}. {item.get('deskripsi', '')}".strip()
    )


def label_jawaban(cf_user):
    """Ubah CF pengguna menjadi label jawaban Iya atau Tidak."""
    return "iya" if float(cf_user) > 0 else "tidak"


def alasan_hasil(item):
    """Daftar alasan gejala yang memicu sebuah hasil, dengan label jawaban pengguna."""
    alasan = []
    for langkah in item["aturan_terpicu"]:
        gejala = langkah.get("deskripsi_gejala") or langkah["kode_gejala"]
        gejala = f"{gejala[:1].upper()}{gejala[1:]}"
        alasan.append(f"{gejala} (kamu: {label_jawaban(langkah['cf_user'])})")
    return alasan


def sumber_terpicu(item, peta_sumber=None):
    """Kumpulkan sumber unik dari seluruh aturan yang memicu sebuah hasil."""
    peta_sumber = peta_sumber or {}
    daftar = []
    terlihat = set()
    for langkah in item["aturan_terpicu"]:
        for sumber in peta_sumber.get(langkah["kode_aturan"], []):
            if sumber["id"] in terlihat:
                continue
            terlihat.add(sumber["id"])
            daftar.append(sumber)
    return daftar


def format_cf(nilai):
    """Format nilai CF menjadi dua angka desimal."""
    return f"{nilai:.2f}"


def format_persen(persen):
    """Format persentase satu angka desimal."""
    return f"{persen:.1f}%"


def teks_sumber(daftar):
    """Susun teks sumber; tampilkan keterangan bila belum ada sumber tertaut."""
    if not daftar:
        return "belum tersedia"
    bagian = []
    for sumber in daftar:
        teks = f"[{sumber['jenis']}] {sumber['sitasi']}"
        if sumber.get("url_doi"):
            teks += f" ({sumber['url_doi']})"
        bagian.append(teks)
    return "; ".join(bagian)


def penjelasan_perhitungan(item, peta_sumber=None):
    """Susun baris perhitungan CF dan sumber untuk satu hasil cheat."""
    peta_sumber = peta_sumber or {}
    baris = []
    for langkah in item["aturan_terpicu"]:
        baris.append(
            f"Aturan {langkah['kode_aturan']} ({langkah['kode_gejala']}): "
            f"CF pengguna {format_cf(langkah['cf_user'])} x CF pakar "
            f"{format_cf(langkah['cf_pakar'])} = {format_cf(langkah['cf_aturan'])}"
        )
        baris.append(
            f"Gabungan: {format_cf(langkah['cf_lama'])} + "
            f"{format_cf(langkah['cf_aturan'])} x "
            f"(1 - {format_cf(langkah['cf_lama'])}) = "
            f"{format_cf(langkah['cf_gabungan'])}"
        )
        daftar_sumber = peta_sumber.get(langkah["kode_aturan"], [])
        baris.append(f"Sumber: {teks_sumber(daftar_sumber)}")
    return baris


def rapikan_hasil(hasil):
    """Batasi label Sangat mungkin ke peringkat teratas dan beri tanda peringatan.

    Kembalikan (hasil_baru, perlu_peringatan). Cheat selain peringkat teratas
    yang persentasenya masih 80 atau lebih diturunkan labelnya menjadi Mungkin.
    """
    if not hasil:
        return [], False
    hasil_baru = [dict(item) for item in hasil]
    for urutan, item in enumerate(hasil_baru):
        if urutan > 0 and item["persen"] >= 80:
            item["kategori"] = "Mungkin"
    jumlah_tinggi = sum(1 for item in hasil_baru if item["persen"] >= 80)
    return hasil_baru, jumlah_tinggi >= 3


def ringkasan_hasil(hasil):
    """Ringkasan satu baris untuk hasil peringkat teratas."""
    if not hasil:
        return "Tidak ada jenis cheat yang dapat disimpulkan dari gejala yang dipilih."
    teratas = hasil[0]
    return (
        f"Hasil teratas: {teratas['nama']} dengan keyakinan "
        f"{format_persen(teratas['persen'])} ({teratas['kategori']})."
    )


def daftar_gejala_terpicu(item):
    """Gabungkan kode gejala yang memicu sebuah hasil cheat."""
    return ", ".join(langkah["kode_gejala"] for langkah in item["aturan_terpicu"])
