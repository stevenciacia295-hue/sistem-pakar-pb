"""Aturan akun pengguna umum tanpa ketergantungan Streamlit."""

import os

AKUN_DEFAULT = {"username": "nesaa", "password": "1234"}


def sumber_akun(env=None):
    """Baca akun dari variabel lingkungan, dengan akun default sebagai cadangan."""
    env = os.environ if env is None else env
    nama_env = str(env.get("APP_USERNAME", "")).strip()
    sandi_env = str(env.get("APP_PASSWORD", ""))
    akun = {
        "username": nama_env or AKUN_DEFAULT["username"],
        "password": sandi_env or AKUN_DEFAULT["password"],
    }
    pakai_default = not (nama_env and sandi_env)
    return akun, pakai_default


def validasi_login(username, password, akun=None):
    """Terima nama apa pun yang tidak kosong selama kata sandi cocok."""
    akun = akun or sumber_akun()[0]
    nama = str(username).strip() if username is not None else ""
    sandi = str(password) if password is not None else ""
    return bool(nama) and sandi == akun["password"]
