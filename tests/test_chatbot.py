"""Tes aturan penghentian percakapan chatbot (maksimal 8 pertanyaan)."""

import itertools
import random

from src import knowledge
from src.chatbot import BATAS_PERTANYAAN, keputusan_berhenti
from src.db import get_connection, init_db

_CONN = get_connection(":memory:")
init_db(_CONN)
knowledge.seed_if_empty(_CONN)
GEJALA = knowledge.get_gejala(_CONN)
ATURAN = knowledge.get_aturan(_CONN)
CHEAT = knowledge.get_cheats(_CONN)


def _simulasi(jawaban, gejala=None):
    """Jalankan loop tanya-jawab dan kembalikan (jumlah pertanyaan, alasan)."""
    gejala = gejala or GEJALA
    pilihan = {}
    nomor = 0
    for nomor, (item, cf) in enumerate(zip(gejala, jawaban), start=1):
        if cf:
            pilihan[item["kode"]] = cf
        berhenti, alasan = keputusan_berhenti(
            pilihan,
            ATURAN,
            CHEAT,
            nomor,
            nomor < len(gejala),
        )
        if berhenti:
            return nomor, alasan
    return nomor, "habis"


def test_batas_pertanyaan_adalah_delapan():
    assert BATAS_PERTANYAAN == 8


def test_gejala_yang_diuji_berasal_dari_database():
    kode = [item["kode"] for item in GEJALA]
    assert len(kode) == 13
    assert kode == [f"G{nomor:02d}" for nomor in range(1, 14)]


def test_jawaban_tinggi_berhenti_setelah_tiga_jawaban():
    nomor, alasan = _simulasi([1.0] * len(GEJALA))
    assert nomor == 3
    assert alasan == "keyakinan_tinggi"


def test_jawaban_rendah_berhenti_tepat_di_batas_pertanyaan():
    nomor, alasan = _simulasi([0.0] * len(GEJALA))
    assert nomor == 8
    assert alasan == "batas_pertanyaan"


def test_semua_kombinasi_jawaban_biner_tidak_melebihi_batas():
    for jawaban in itertools.product([0.0, 1.0], repeat=len(GEJALA)):
        nomor, _alasan = _simulasi(list(jawaban))
        assert nomor <= BATAS_PERTANYAAN


def test_kombinasi_acak_tidak_pernah_melebihi_batas():
    rng = random.Random(11)
    nilai = [0.0, 0.4, 0.7, 1.0]
    for _ in range(300):
        jawaban = [rng.choice(nilai) for _ in range(len(GEJALA))]
        nomor, _alasan = _simulasi(jawaban)
        assert nomor <= BATAS_PERTANYAAN


def test_semua_gejala_pendek_berhenti_karena_habis():
    gejala = GEJALA[:5]
    nomor, alasan = _simulasi([0.4] * 5, gejala)
    assert nomor == 5
    assert alasan == "semua_gejala"


def test_belum_berhenti_sebelum_tiga_jawaban():
    berhenti, alasan = keputusan_berhenti(
        {"G01": 1.0, "G02": 1.0},
        ATURAN,
        CHEAT,
        2,
        True,
    )
    assert berhenti is False
    assert alasan is None
