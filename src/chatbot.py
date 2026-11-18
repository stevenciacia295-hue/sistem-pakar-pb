"""Aturan penghentian percakapan chatbot (fungsi murni, tanpa Streamlit)."""

from src.engine import diagnose

BATAS_PERSEN = 85.0
MIN_JAWABAN = 3
BATAS_PERTANYAAN = 8


def keputusan_berhenti(input_cf, aturan, cheat, jumlah_pertanyaan, masih_ada_gejala):
    """Tentukan apakah percakapan harus berhenti dan alasannya.

    Berhenti bila salah satu terpenuhi (mana yang lebih dulu):
    1. sudah BATAS_PERTANYAAN pertanyaan diajukan;
    2. sudah MIN_JAWABAN jawaban dan ada cheat dengan persentase >= BATAS_PERSEN;
    3. seluruh gejala sudah ditanyakan.
    """
    if jumlah_pertanyaan >= BATAS_PERTANYAAN:
        return True, "batas_pertanyaan"
    if jumlah_pertanyaan >= MIN_JAWABAN:
        hasil = diagnose(input_cf, aturan, cheat)
        if hasil and hasil[0]["persen"] >= BATAS_PERSEN:
            return True, "keyakinan_tinggi"
    if not masih_ada_gejala:
        return True, "semua_gejala"
    return False, None
