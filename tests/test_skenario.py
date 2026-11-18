"""Tes berkas skenario uji pada halaman Pengujian."""

import json
from pathlib import Path

import pytest

from src import knowledge
from src.db import get_connection, init_db
from src.engine import diagnose

BERKAS = Path(__file__).resolve().parent.parent / "data" / "skenario_uji.json"
SKENARIO = json.loads(BERKAS.read_text(encoding="utf-8"))

_CONN = get_connection(":memory:")
init_db(_CONN)
knowledge.seed_if_empty(_CONN)
ATURAN = knowledge.get_aturan(_CONN)
CHEAT = knowledge.get_cheats(_CONN)
GEJALA = knowledge.get_gejala(_CONN)


def test_skenario_minimal_sepuluh():
    assert len(SKENARIO) >= 10


def test_basis_pengetahuan_uji_dibaca_dari_database():
    assert len(GEJALA) == 13
    assert len(ATURAN) == 13
    kode_gejala = {item["kode"] for item in GEJALA}
    for data in SKENARIO:
        assert set(data["input"]) <= kode_gejala


@pytest.mark.parametrize("data", SKENARIO, ids=[item["id"] for item in SKENARIO])
def test_skenario_sesuai_perhitungan_manual(data):
    hasil = diagnose(data["input"], ATURAN, CHEAT, GEJALA)
    diharapkan = data["diharapkan"]
    if not diharapkan["kode_cheat"]:
        assert hasil == []
        return
    assert hasil[0]["kode_cheat"] == diharapkan["kode_cheat"]
    assert hasil[0]["persen"] == pytest.approx(diharapkan["persen"], abs=0.01)
