"""Mesin inferensi forward chaining dengan certainty factor (fungsi murni)."""

SKALA_KEYAKINAN = [
    {"label": "Tidak yakin", "nilai": 0.2},
    {"label": "Kurang yakin", "nilai": 0.4},
    {"label": "Cukup yakin", "nilai": 0.6},
    {"label": "Yakin", "nilai": 0.8},
    {"label": "Sangat yakin", "nilai": 1.0},
]


def gabung_cf(cf_lama, cf_baru):
    """Gabungkan dua nilai certainty factor secara sekuensial."""
    return cf_lama + cf_baru * (1 - cf_lama)


def kategori_keyakinan(cf):
    """Kategori hasil berdasarkan nilai CF gabungan."""
    if cf >= 0.8:
        return "Sangat mungkin"
    if cf >= 0.5:
        return "Mungkin"
    return "Kemungkinan kecil"


def diagnose(input_cf, aturan, cheat, gejala=None):
    """Jalankan forward chaining pada gejala terpilih dan kembalikan ranking cheat.

    input_cf: {kode_gejala: cf_user}
    aturan: list dict aturan (kode, kode_cheat, kode_gejala, cf_pakar)
    cheat: list dict cheat (kode, nama, deskripsi, saran)
    gejala: list dict gejala (kode, deskripsi), opsional untuk keterangan
    """
    if not input_cf:
        return []

    peta_gejala = {g["kode"]: g["deskripsi"] for g in (gejala or [])}
    peta_cheat = {c["kode"]: c for c in cheat}
    akumulasi = {}

    for a in sorted(aturan, key=lambda x: x["kode"]):
        kode_gejala = a["kode_gejala"]
        if kode_gejala not in input_cf:
            continue
        cf_user = float(input_cf[kode_gejala])
        cf_pakar = float(a["cf_pakar"])
        cf_aturan = cf_user * cf_pakar
        kode_cheat = a["kode_cheat"]
        if kode_cheat not in akumulasi:
            akumulasi[kode_cheat] = {"cf": 0.0, "langkah": []}
        cf_lama = akumulasi[kode_cheat]["cf"]
        cf_gabungan = gabung_cf(cf_lama, cf_aturan)
        akumulasi[kode_cheat]["langkah"].append(
            {
                "kode_aturan": a["kode"],
                "kode_gejala": kode_gejala,
                "deskripsi_gejala": peta_gejala.get(kode_gejala, ""),
                "cf_user": cf_user,
                "cf_pakar": cf_pakar,
                "cf_aturan": cf_aturan,
                "cf_lama": cf_lama,
                "cf_gabungan": cf_gabungan,
            }
        )
        akumulasi[kode_cheat]["cf"] = cf_gabungan

    hasil = []
    for kode_cheat, data in akumulasi.items():
        info = peta_cheat.get(kode_cheat, {})
        cf = data["cf"]
        hasil.append(
            {
                "kode_cheat": kode_cheat,
                "nama": info.get("nama", kode_cheat),
                "deskripsi": info.get("deskripsi", ""),
                "saran": info.get("saran", ""),
                "cf_gabungan": cf,
                "persen": round(cf * 100, 1),
                "kategori": kategori_keyakinan(cf),
                "aturan_terpicu": data["langkah"],
            }
        )

    hasil.sort(key=lambda item: (-item["cf_gabungan"], item["kode_cheat"]))
    return hasil
