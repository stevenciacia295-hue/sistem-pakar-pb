"""Materi percakapan PB-Bot: sapaan, respons, penutup, dan varian pertanyaan."""

import json
import random
from pathlib import Path

PEMBUKA = [
    "Halo! Ceritain pemain yang kamu curigai ya, aku bantu cek lewat beberapa pertanyaan singkat.",
    "Hai, siap bantu analisis pemain mencurigakan. Jawab sesuai yang kamu lihat aja.",
    "Yuk mulai. Aku tanya beberapa hal soal gaya main pemain yang kamu curigai.",
    "Selamat datang. Kita cek bareng apakah ada indikasi cheat, jawab sejujurnya ya.",
    "Oke, mulai dari pengamatanmu. Jawab sesuai yang benar-benar kamu lihat di game.",
]

RESPONS = [
    "Oke, dicatat.",
    "Noted, lanjut ya.",
    "Siap, terima kasih.",
    "Baik, aku simpan jawabannya.",
    "Oke, berikutnya.",
    "Dapat, lanjut pertanyaan berikutnya.",
]

PENUTUP = [
    "Sudah cukup datanya. Ini hasil analisisku:",
    "Terima kasih, aku sudah punya gambaran yang cukup. Hasilnya:",
    "Selesai. Berikut kesimpulan dari jawabanmu:",
]

PILIHAN_JAWABAN = [
    ("Iya", 1.0),
    ("Tidak", 0.0),
]

DATA_PERTANYAAN = Path(__file__).resolve().parent.parent / "data" / "pertanyaan.json"


def muat_pertanyaan(path=DATA_PERTANYAAN):
    """Muat varian pertanyaan per kode gejala dari berkas JSON."""
    try:
        with Path(path).open(encoding="utf-8") as berkas:
            data = json.load(berkas)
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict):
        return {}
    hasil = {}
    for kode, varian in data.items():
        if not isinstance(varian, list):
            continue
        bersih = [str(teks).strip() for teks in varian if str(teks).strip()]
        if bersih:
            hasil[str(kode)] = bersih
    return hasil


PERTANYAAN = muat_pertanyaan()


def ambil_pembuka(rng=None):
    """Pilih satu kalimat pembuka secara acak."""
    return (rng or random).choice(PEMBUKA)


def ambil_respons(rng=None):
    """Pilih satu kalimat respons secara acak."""
    return (rng or random).choice(RESPONS)


def ambil_penutup(rng=None):
    """Pilih satu kalimat penutup secara acak."""
    return (rng or random).choice(PENUTUP)


def ambil_pertanyaan(kode_gejala, rng=None):
    """Pilih satu varian pertanyaan untuk kode gejala tertentu."""
    varian = PERTANYAAN.get(kode_gejala)
    if not varian:
        return f"Apakah kamu melihat gejala {kode_gejala} pada pemain tersebut?"
    return (rng or random).choice(varian)
