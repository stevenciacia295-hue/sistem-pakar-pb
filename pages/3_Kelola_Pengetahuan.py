"""Halaman Kelola Pengetahuan: CRUD cheat, gejala, dan aturan (kata sandi admin)."""

import os

import pandas as pd
import streamlit as st

from src import auth, knowledge, penilaian, ui
from src.db import get_connection, init_db

st.set_page_config(page_title="Kelola Pengetahuan — PB Expert AI", layout="wide")

ui.terapkan_gaya()
auth.wajib_login()


def _sumber_kata_sandi():
    dari_env = os.environ.get("ADMIN_PASSWORD")
    if dari_env:
        return dari_env, False
    try:
        dari_secret = st.secrets["ADMIN_PASSWORD"]
    except Exception:
        dari_secret = None
    if dari_secret:
        return str(dari_secret), False
    return "nesaa", True


KATA_SANDI, PAKAI_DEFAULT = _sumber_kata_sandi()

if "admin_ok" not in st.session_state:
    st.session_state["admin_ok"] = False

if not st.session_state["admin_ok"]:
    ui.judul_halaman(
        "Kelola Pengetahuan",
        "Masuk untuk mengubah basis pengetahuan.",
    )
    isian = st.text_input("Kata sandi", type="password", key="admin_password")
    if st.button("Masuk", key="masuk_admin"):
        if isian == KATA_SANDI:
            st.session_state["admin_ok"] = True
            st.rerun()
        else:
            st.write("Kata sandi salah.")
    if PAKAI_DEFAULT:
        st.caption("Password default, segera ganti")
    st.stop()


@st.cache_resource
def get_conn():
    conn = get_connection()
    init_db(conn)
    knowledge.seed_if_empty(conn)
    return conn


conn = get_conn()

ui.judul_halaman(
    "Kelola Pengetahuan",
    "Perubahan langsung memengaruhi hasil diagnosa berikutnya.",
)
if PAKAI_DEFAULT:
    st.caption("Password default, segera ganti")

tab_cheat, tab_gejala, tab_aturan, tab_sumber, tab_penilaian = st.tabs(
    ["Cheat", "Gejala", "Aturan", "Sumber", "Penilaian Pakar"]
)

with tab_cheat:
    daftar_cheat = knowledge.get_cheats(conn)
    st.subheader("Daftar cheat")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Kode": c["kode"],
                    "Nama": c["nama"],
                    "Deskripsi": c["deskripsi"],
                    "Saran": c["saran"],
                }
                for c in daftar_cheat
            ]
        ),
        hide_index=True,
    )

    with st.expander("Tambah cheat"):
        with st.form("tambah_cheat", clear_on_submit=True):
            kode = st.text_input("Kode cheat")
            nama = st.text_input("Nama cheat")
            deskripsi = st.text_area("Deskripsi")
            saran = st.text_area("Saran")
            tombol = st.form_submit_button("Tambah cheat")
        if tombol:
            try:
                knowledge.add_cheat(conn, kode, nama, deskripsi, saran)
            except ValueError as kesalahan:
                st.write(f"Gagal menambah cheat: {kesalahan}")
            else:
                st.rerun()

    if daftar_cheat:
        peta_nama = {c["kode"]: c["nama"] for c in daftar_cheat}

        st.subheader("Ubah cheat")
        kode_ubah = st.selectbox(
            "Pilih cheat",
            options=list(peta_nama),
            format_func=lambda kode: f"{kode} — {peta_nama[kode]}",
            key="cheat_ubah_pilih",
        )
        cheat_terpilih = next(c for c in daftar_cheat if c["kode"] == kode_ubah)
        with st.form(f"ubah_cheat_{kode_ubah}"):
            nama_baru = st.text_input(
                "Nama",
                value=cheat_terpilih["nama"],
                key=f"cheat_ubah_nama_{kode_ubah}",
            )
            deskripsi_baru = st.text_area(
                "Deskripsi",
                value=cheat_terpilih["deskripsi"],
                key=f"cheat_ubah_deskripsi_{kode_ubah}",
            )
            saran_baru = st.text_area(
                "Saran",
                value=cheat_terpilih["saran"],
                key=f"cheat_ubah_saran_{kode_ubah}",
            )
            tombol = st.form_submit_button("Simpan perubahan")
        if tombol:
            try:
                knowledge.update_cheat(
                    conn, kode_ubah, nama_baru, deskripsi_baru, saran_baru
                )
            except ValueError as kesalahan:
                st.write(f"Gagal mengubah cheat: {kesalahan}")
            else:
                st.rerun()

        st.subheader("Hapus cheat")
        kode_hapus = st.selectbox(
            "Pilih cheat yang dihapus",
            options=list(peta_nama),
            format_func=lambda kode: f"{kode} — {peta_nama[kode]}",
            key="cheat_hapus_pilih",
        )
        yakin = st.checkbox(
            "Saya yakin. Menghapus cheat juga menghapus seluruh aturan yang memakainya.",
            key=f"cheat_hapus_yakin_{kode_hapus}",
        )
        if st.button("Hapus cheat", disabled=not yakin):
            try:
                knowledge.delete_cheat(conn, kode_hapus)
            except ValueError as kesalahan:
                st.write(f"Gagal menghapus cheat: {kesalahan}")
            else:
                st.rerun()

with tab_gejala:
    daftar_gejala = knowledge.get_gejala(conn)
    st.subheader("Daftar gejala")
    st.dataframe(
        pd.DataFrame(
            [{"Kode": g["kode"], "Deskripsi": g["deskripsi"]} for g in daftar_gejala]
        ),
        hide_index=True,
    )

    with st.expander("Tambah gejala"):
        with st.form("tambah_gejala", clear_on_submit=True):
            kode = st.text_input("Kode gejala")
            deskripsi = st.text_area("Deskripsi gejala")
            tombol = st.form_submit_button("Tambah gejala")
        if tombol:
            try:
                knowledge.add_gejala(conn, kode, deskripsi)
            except ValueError as kesalahan:
                st.write(f"Gagal menambah gejala: {kesalahan}")
            else:
                st.rerun()

    if daftar_gejala:
        peta_deskripsi = {g["kode"]: g["deskripsi"] for g in daftar_gejala}

        st.subheader("Ubah gejala")
        kode_ubah = st.selectbox(
            "Pilih gejala",
            options=list(peta_deskripsi),
            format_func=lambda kode: f"{kode} — {peta_deskripsi[kode]}",
            key="gejala_ubah_pilih",
        )
        with st.form(f"ubah_gejala_{kode_ubah}"):
            deskripsi_baru = st.text_area(
                "Deskripsi",
                value=peta_deskripsi[kode_ubah],
                key=f"gejala_ubah_deskripsi_{kode_ubah}",
            )
            tombol = st.form_submit_button("Simpan perubahan")
        if tombol:
            try:
                knowledge.update_gejala(conn, kode_ubah, deskripsi_baru)
            except ValueError as kesalahan:
                st.write(f"Gagal mengubah gejala: {kesalahan}")
            else:
                st.rerun()

        st.subheader("Hapus gejala")
        kode_hapus = st.selectbox(
            "Pilih gejala yang dihapus",
            options=list(peta_deskripsi),
            format_func=lambda kode: f"{kode} — {peta_deskripsi[kode]}",
            key="gejala_hapus_pilih",
        )
        yakin = st.checkbox(
            "Saya yakin. Menghapus gejala juga menghapus seluruh aturan yang memakainya.",
            key=f"gejala_hapus_yakin_{kode_hapus}",
        )
        if st.button("Hapus gejala", disabled=not yakin):
            try:
                knowledge.delete_gejala(conn, kode_hapus)
            except ValueError as kesalahan:
                st.write(f"Gagal menghapus gejala: {kesalahan}")
            else:
                st.rerun()

with tab_aturan:
    daftar_aturan = knowledge.get_aturan(conn)
    peta_cheat = {c["kode"]: c["nama"] for c in knowledge.get_cheats(conn)}
    peta_gejala = {g["kode"]: g["deskripsi"] for g in knowledge.get_gejala(conn)}
    peta_sumber_aturan = knowledge.peta_sumber_aturan(conn)

    st.subheader("Daftar aturan")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Kode": a["kode"],
                    "Cheat": f"{a['kode_cheat']} — {peta_cheat.get(a['kode_cheat'], '?')}",
                    "Gejala": f"{a['kode_gejala']} — {peta_gejala.get(a['kode_gejala'], '?')}",
                    "CF pakar": a["cf_pakar"],
                    "Pakar": a["nama_pakar"],
                    "Tanggal wawancara": a["tanggal_wawancara"],
                    "Jumlah sumber": len(peta_sumber_aturan.get(a["kode"], [])),
                }
                for a in daftar_aturan
            ]
        ),
        hide_index=True,
    )

    if peta_cheat and peta_gejala:
        with st.expander("Tambah aturan"):
            with st.form("tambah_aturan", clear_on_submit=True):
                kode = st.text_input("Kode aturan")
                cheat_pilih = st.selectbox(
                    "Cheat",
                    options=list(peta_cheat),
                    format_func=lambda kode_cheat: f"{kode_cheat} — {peta_cheat[kode_cheat]}",
                )
                gejala_pilih = st.selectbox(
                    "Gejala",
                    options=list(peta_gejala),
                    format_func=lambda kode_gejala: f"{kode_gejala} — {peta_gejala[kode_gejala]}",
                )
                cf_pakar = st.number_input(
                    "CF pakar (0 sampai 1)",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.5,
                    step=0.05,
                )
                nama_pakar = st.text_input(
                    "Nama pakar", placeholder="Belum diisi"
                )
                tanggal_wawancara = st.text_input(
                    "Tanggal wawancara", placeholder="Belum diisi"
                )
                tombol = st.form_submit_button("Tambah aturan")
            if tombol:
                try:
                    knowledge.add_aturan(
                        conn,
                        kode,
                        cheat_pilih,
                        gejala_pilih,
                        cf_pakar,
                        nama_pakar,
                        tanggal_wawancara,
                    )
                except ValueError as kesalahan:
                    st.write(f"Gagal menambah aturan: {kesalahan}")
                else:
                    st.rerun()
    else:
        st.write("Tambahkan minimal satu cheat dan satu gejala sebelum membuat aturan.")

    if daftar_aturan and peta_cheat and peta_gejala:
        st.subheader("Ubah aturan")
        kode_ubah = st.selectbox(
            "Pilih aturan",
            options=[a["kode"] for a in daftar_aturan],
            key="aturan_ubah_pilih",
        )
        aturan_terpilih = next(a for a in daftar_aturan if a["kode"] == kode_ubah)
        with st.form(f"ubah_aturan_{kode_ubah}"):
            cheat_baru = st.selectbox(
                "Cheat",
                options=list(peta_cheat),
                index=list(peta_cheat).index(aturan_terpilih["kode_cheat"]),
                format_func=lambda kode_cheat: f"{kode_cheat} — {peta_cheat[kode_cheat]}",
                key=f"aturan_ubah_cheat_{kode_ubah}",
            )
            gejala_baru = st.selectbox(
                "Gejala",
                options=list(peta_gejala),
                index=list(peta_gejala).index(aturan_terpilih["kode_gejala"]),
                format_func=lambda kode_gejala: f"{kode_gejala} — {peta_gejala[kode_gejala]}",
                key=f"aturan_ubah_gejala_{kode_ubah}",
            )
            cf_baru = st.number_input(
                "CF pakar (0 sampai 1)",
                min_value=0.0,
                max_value=1.0,
                value=float(aturan_terpilih["cf_pakar"]),
                step=0.05,
                key=f"aturan_ubah_cf_{kode_ubah}",
            )
            nama_pakar_baru = st.text_input(
                "Nama pakar",
                value=aturan_terpilih["nama_pakar"],
                key=f"aturan_ubah_pakar_{kode_ubah}",
            )
            tanggal_baru = st.text_input(
                "Tanggal wawancara",
                value=aturan_terpilih["tanggal_wawancara"],
                key=f"aturan_ubah_tanggal_{kode_ubah}",
            )
            tombol = st.form_submit_button("Simpan perubahan")
        if tombol:
            try:
                knowledge.update_aturan(
                    conn,
                    kode_ubah,
                    cheat_baru,
                    gejala_baru,
                    cf_baru,
                    nama_pakar_baru,
                    tanggal_baru,
                )
            except ValueError as kesalahan:
                st.write(f"Gagal mengubah aturan: {kesalahan}")
            else:
                st.rerun()

        st.subheader("Hapus aturan")
        kode_hapus = st.selectbox(
            "Pilih aturan yang dihapus",
            options=[a["kode"] for a in daftar_aturan],
            key="aturan_hapus_pilih",
        )
        yakin = st.checkbox(
            "Saya yakin ingin menghapus aturan ini.",
            key=f"aturan_hapus_yakin_{kode_hapus}",
        )
        if st.button("Hapus aturan", disabled=not yakin):
            try:
                knowledge.delete_aturan(conn, kode_hapus)
            except ValueError as kesalahan:
                st.write(f"Gagal menghapus aturan: {kesalahan}")
            else:
                st.rerun()

with tab_sumber:
    daftar_sumber = knowledge.get_sumber(conn)
    peta_id_sumber = {s["id"]: s for s in daftar_sumber}

    st.subheader("Daftar sumber")
    if not daftar_sumber:
        st.write("Belum ada sumber pengetahuan.")
    else:
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "ID": s["id"],
                        "Jenis": s["jenis"],
                        "Sitasi": s["sitasi"],
                        "URL atau DOI": s["url_doi"],
                    }
                    for s in daftar_sumber
                ]
            ),
            hide_index=True,
        )

    with st.expander("Tambah sumber"):
        with st.form("tambah_sumber", clear_on_submit=True):
            jenis = st.selectbox(
                "Jenis",
                options=list(knowledge.JENIS_SUMBER),
                key="tambah_sumber_jenis",
            )
            sitasi = st.text_area("Sitasi", key="tambah_sumber_sitasi")
            url_doi = st.text_input("URL atau DOI", key="tambah_sumber_url")
            tombol = st.form_submit_button("Tambah sumber")
        if tombol:
            try:
                knowledge.add_sumber(conn, jenis, sitasi, url_doi)
            except ValueError as kesalahan:
                st.write(f"Gagal menambah sumber: {kesalahan}")
            else:
                st.rerun()

    if daftar_sumber:
        st.subheader("Ubah sumber")
        id_ubah = st.selectbox(
            "Pilih sumber",
            options=list(peta_id_sumber),
            format_func=lambda id_sumber: (
                f"#{id_sumber} — {peta_id_sumber[id_sumber]['sitasi']}"
            ),
            key="sumber_ubah_pilih",
        )
        sumber_ubah = peta_id_sumber[id_ubah]
        with st.form(f"ubah_sumber_{id_ubah}"):
            jenis_baru = st.selectbox(
                "Jenis",
                options=list(knowledge.JENIS_SUMBER),
                index=list(knowledge.JENIS_SUMBER).index(sumber_ubah["jenis"]),
                key=f"ubah_sumber_jenis_{id_ubah}",
            )
            sitasi_baru = st.text_area(
                "Sitasi",
                value=sumber_ubah["sitasi"],
                key=f"ubah_sumber_sitasi_{id_ubah}",
            )
            url_baru = st.text_input(
                "URL atau DOI",
                value=sumber_ubah["url_doi"],
                key=f"ubah_sumber_url_{id_ubah}",
            )
            tombol = st.form_submit_button("Simpan perubahan")
        if tombol:
            try:
                knowledge.update_sumber(
                    conn, id_ubah, jenis_baru, sitasi_baru, url_baru
                )
            except ValueError as kesalahan:
                st.write(f"Gagal mengubah sumber: {kesalahan}")
            else:
                st.rerun()

        st.subheader("Hapus sumber")
        id_hapus = st.selectbox(
            "Pilih sumber yang dihapus",
            options=list(peta_id_sumber),
            format_func=lambda id_sumber: (
                f"#{id_sumber} — {peta_id_sumber[id_sumber]['sitasi']}"
            ),
            key="sumber_hapus_pilih",
        )
        yakin = st.checkbox(
            "Saya yakin ingin menghapus sumber ini beserta tautannya.",
            key=f"sumber_hapus_yakin_{id_hapus}",
        )
        if st.button("Hapus sumber", disabled=not yakin, key="hapus_sumber"):
            try:
                knowledge.delete_sumber(conn, id_hapus)
            except ValueError as kesalahan:
                st.write(f"Gagal menghapus sumber: {kesalahan}")
            else:
                st.rerun()

    st.subheader("Hubungkan sumber ke aturan")
    daftar_aturan = knowledge.get_aturan(conn)
    if not daftar_sumber or not daftar_aturan:
        st.write("Tambahkan minimal satu sumber dan satu aturan terlebih dahulu.")
    else:
        kode_aturan = st.selectbox(
            "Pilih aturan",
            options=[a["kode"] for a in daftar_aturan],
            key="tautan_aturan_pilih",
        )
        terpilih = [
            s["id"] for s in knowledge.get_sumber_aturan(conn, kode_aturan)
        ]
        pilihan = st.multiselect(
            "Sumber untuk aturan ini",
            options=list(peta_id_sumber),
            default=terpilih,
            format_func=lambda id_sumber: (
                f"#{id_sumber} [{peta_id_sumber[id_sumber]['jenis']}] "
                f"{peta_id_sumber[id_sumber]['sitasi']}"
            ),
            key=f"tautan_sumber_{kode_aturan}",
        )
        if st.button("Simpan tautan sumber", key="simpan_tautan_sumber"):
            try:
                knowledge.set_sumber_aturan(conn, kode_aturan, pilihan)
            except ValueError as kesalahan:
                st.write(f"Gagal menyimpan tautan: {kesalahan}")
            else:
                st.rerun()

with tab_penilaian:
    daftar_penilaian = penilaian.get_penilaian(conn)
    ringkasan = penilaian.ringkasan_cf(conn)

    st.subheader("Rata-rata keyakinan pakar")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Kode": item["kode"],
                    "Ciri": item["ciri"],
                    "Cheat": item["cheat"],
                    "Rata-rata CF": (
                        f"{item['rata_rata']:.2f}"
                        if item["rata_rata"] is not None
                        else "-"
                    ),
                    "Jumlah penilaian": item["jumlah"],
                }
                for item in ringkasan
            ]
        ),
        hide_index=True,
    )
    st.caption(
        "Rata-rata ini dapat dijadikan acuan saat memperbarui CF pakar pada "
        "tab Aturan."
    )

    if not daftar_penilaian:
        st.write(
            "Belum ada penilaian pakar. Formulir tersedia di halaman "
            "Penilaian Pakar."
        )
    else:
        st.subheader("Daftar kiriman penilaian")
        baris_kiriman = []
        for item in daftar_penilaian:
            baris = {
                "ID": item["id"],
                "Waktu": item["waktu"],
                "Nama": item["nama_tampil"],
                "Peran": item["peran"],
                "Lama bermain": item["lama_bermain"],
                "Rank": item["rank"] or "-",
                "Izin nama": item["izin_nama"],
                "Boleh dihubungi": item["boleh_dihubungi"],
                "Jumlah dinilai": sum(
                    1 for nilai in item["penilaian"].values() if nilai is not None
                ),
            }
            for kode in penilaian.KODE_ATURAN_FORM:
                baris[kode] = penilaian.label_nilai(
                    item["penilaian"].get(kode)
                )
            baris_kiriman.append(baris)
        tabel_kiriman = pd.DataFrame(baris_kiriman)
        st.dataframe(tabel_kiriman, hide_index=True)

        st.download_button(
            "Unduh CSV penilaian",
            data=tabel_kiriman.to_csv(index=False).encode("utf-8"),
            file_name="penilaian_pakar.csv",
            mime="text/csv",
        )

        id_pilih = st.selectbox(
            "Lihat detail penilaian",
            options=[item["id"] for item in daftar_penilaian],
            format_func=lambda nilai: next(
                f"#{item['id']} — {item['nama_tampil']} — {item['waktu']}"
                for item in daftar_penilaian
                if item["id"] == nilai
            ),
            key="penilaian_detail_pilih",
        )
        detail = penilaian.get_penilaian_by_id(conn, id_pilih)
        if detail:
            with st.expander(f"Detail penilaian #{detail['id']}"):
                st.write(f"Nama: {detail['nama_tampil']}")
                st.write(f"Peran: {detail['peran']}")
                st.write(f"Lama bermain: {detail['lama_bermain']}")
                st.write(f"Rank atau pengalaman: {detail['rank'] or '-'}")
                st.write(f"Izin nama: {detail['izin_nama']}")
                st.write(f"Boleh dihubungi: {detail['boleh_dihubungi']}")
                st.markdown("**Pengalaman**")
                for label, kunci in (
                    ("Ciri paling meyakinkan", "pengalaman_ciri"),
                    ("Membedakan jago dan cheat", "pengalaman_beda"),
                    ("Ciri yang sering disangka cheat", "pengalaman_mitos"),
                    ("Bukti yang biasa dipakai", "pengalaman_bukti"),
                    ("Ciri lain", "ciri_lain"),
                    ("Cheat lain", "cheat_lain"),
                ):
                    st.markdown(f"**{label}:** {detail[kunci] or '-'}")
                st.markdown("**Penilaian keyakinan**")
                st.dataframe(
                    pd.DataFrame(
                        [
                            {
                                "Kode": aturan["kode"],
                                "Ciri": aturan["ciri"],
                                "Cheat": aturan["cheat"],
                                "Penilaian": penilaian.label_nilai(
                                    detail["penilaian"].get(aturan["kode"])
                                ),
                            }
                            for aturan in penilaian.ATURAN_FORM
                        ]
                    ),
                    hide_index=True,
                )

        yakin = st.checkbox(
            "Saya yakin ingin menghapus penilaian ini beserta sumber pakarnya.",
            key=f"hapus_penilaian_yakin_{id_pilih}",
        )
        if st.button(
            "Hapus penilaian",
            disabled=not yakin,
            key="hapus_penilaian",
        ):
            try:
                penilaian.hapus_penilaian(conn, id_pilih)
            except ValueError as kesalahan:
                st.write(f"Gagal menghapus penilaian: {kesalahan}")
            else:
                st.rerun()
