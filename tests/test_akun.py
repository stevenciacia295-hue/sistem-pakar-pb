"""Tes aturan akun pengguna umum."""

from src import akun


def test_akun_default_bila_lingkungan_kosong():
    data, pakai_default = akun.sumber_akun({})
    assert data == {"username": "nesaa", "password": "1234"}
    assert pakai_default is True


def test_akun_dari_variabel_lingkungan():
    data, pakai_default = akun.sumber_akun(
        {"APP_USERNAME": "  budi  ", "APP_PASSWORD": "rahasia"}
    )
    assert data == {"username": "budi", "password": "rahasia"}
    assert pakai_default is False


def test_akun_sebagian_memakai_nilai_default():
    data, pakai_default = akun.sumber_akun({"APP_USERNAME": "budi"})
    assert data["username"] == "budi"
    assert data["password"] == "1234"
    assert pakai_default is True


def test_login_menerima_nama_apa_pun_dengan_sandi_benar():
    data = {"username": "nesaa", "password": "1234"}
    assert akun.validasi_login("nesaa", "1234", data)
    assert akun.validasi_login("steven", "1234", data)
    assert akun.validasi_login("  Budi  ", "1234", data)
    assert not akun.validasi_login("pengguna", "salah", data)
    assert not akun.validasi_login("", "1234", data)
    assert not akun.validasi_login(None, "1234", data)
