"""Halaman Diagnosa: konsol wawancara dan jejak inferensi sistem pakar."""

import html

import streamlit as st

from src import (
    auth,
    chatbot,
    explain,
    history,
    knowledge,
    laporan_pdf,
    percakapan,
    ui,
)
from src.db import get_connection, init_db
from src.engine import diagnose

st.set_page_config(page_title="Diagnosa — PB Expert AI", layout="wide")


@st.cache_resource
def get_conn():
    conn = get_connection()
    init_db(conn)
    knowledge.seed_if_empty(conn)
    return conn


conn = get_conn()
daftar_gejala = knowledge.get_gejala(conn)
daftar_aturan = knowledge.get_aturan(conn)
daftar_cheat = knowledge.get_cheats(conn)
peta_sumber = knowledge.peta_sumber_aturan(conn)
peta_gejala = {g["kode"]: g["deskripsi"] for g in daftar_gejala}

ui.terapkan_gaya()
auth.wajib_login()


def _mulai():
    st.session_state["dialog"] = []
    st.session_state["tahap"] = "nama"
    st.session_state["indeks"] = 0
    st.session_state["jumlah_tanya"] = 0
    st.session_state["pilihan"] = {}
    st.session_state["kode_aktif"] = None
    st.session_state["hasil"] = None
    st.session_state["peringatan"] = False
    st.session_state["nama"] = ""
    st.session_state["sudah_simpan"] = False


def _kirim(peran, teks=None, **tambahan):
    pesan = {"peran": peran}
    if teks is not None:
        pesan["teks"] = teks
    pesan.update(tambahan)
    st.session_state["dialog"].append(pesan)


def _tanya_gejala(awalan=None):
    gejala = daftar_gejala[st.session_state["indeks"]]
    st.session_state["jumlah_tanya"] += 1
    st.session_state["kode_aktif"] = gejala["kode"]
    st.session_state["tahap"] = "tanya"
    pertanyaan = percakapan.ambil_pertanyaan(gejala["kode"])
    teks = f"{awalan} {pertanyaan}" if awalan else pertanyaan
    _kirim("bot", f"{teks}\n({gejala['kode']} — {gejala['deskripsi']})")


def _selesaikan():
    _kirim("bot", percakapan.ambil_penutup())
    hasil = diagnose(
        st.session_state["pilihan"], daftar_aturan, daftar_cheat, daftar_gejala
    )
    hasil, tidak_konsisten = explain.rapikan_hasil(hasil)
    st.session_state["peringatan"] = tidak_konsisten
    if tidak_konsisten:
        _kirim("bot", tipe="peringatan", teks=explain.PERINGATAN_TIDAK_KONSISTEN)
    st.session_state["hasil"] = hasil
    _kirim("bot", tipe="hasil", hasil=hasil)
    st.session_state["tahap"] = "selesai"


def _lanjut():
    st.session_state["indeks"] += 1
    berhenti, _alasan = chatbot.keputusan_berhenti(
        st.session_state["pilihan"],
        daftar_aturan,
        daftar_cheat,
        st.session_state["jumlah_tanya"],
        st.session_state["indeks"] < len(daftar_gejala),
    )
    if berhenti:
        _selesaikan()
    else:
        _tanya_gejala(percakapan.ambil_respons())


def _tautan_sumber(sumber):
    alamat = (sumber.get("url_doi") or "").strip()
    if alamat.startswith(("http://", "https://")):
        tautan = alamat
    elif alamat.startswith("10."):
        tautan = f"https://doi.org/{alamat}"
    else:
        tautan = ""
    if not tautan:
        return ""
    return (
        f'<br><a href="{html.escape(tautan, quote=True)}" target="_blank" '
        f'rel="noopener">{html.escape(alamat)}</a>'
    )


def _isi_sumber(sumber):
    if not sumber:
        return (
            '<div class="sumber-butir">'
            "Sumber belum tersedia untuk aturan ini.</div>"
        )
    bagian = []
    for item in sumber:
        bagian.append(
            '<div class="sumber-butir">'
            f'<span class="sumber-jenis">[{html.escape(item["jenis"])}]</span> '
            f'{html.escape(item["sitasi"])}{_tautan_sumber(item)}</div>'
        )
    return "".join(bagian)


def _rincian(item):
    return "<br>".join(
        html.escape(baris)
        for baris in explain.penjelasan_perhitungan(item, peta_sumber)
    )


def _render_jejak():
    """Tampilkan jejak penalaran expert system untuk kandidat teratas."""
    hasil = st.session_state.get("hasil") or []
    pilihan = st.session_state.get("pilihan") or {}

    with st.expander("Jejak inferensi — dari fakta ke kesimpulan", expanded=True):
        st.caption(
            "Panel ini memperlihatkan cara mesin pakar bekerja: fakta yang "
            "terekam, aturan yang terpicu, agregasi certainty factor, lalu "
            "kesimpulan akhir."
        )

        st.markdown("**1. Working memory — fakta yang terekam**")
        if pilihan:
            st.dataframe(
                [
                    {
                        "Kode": kode,
                        "Gejala": peta_gejala.get(kode, ""),
                        "Jawaban": "Iya",
                        "CF pengguna": f"{float(nilai):.1f}",
                    }
                    for kode, nilai in sorted(pilihan.items())
                ],
                hide_index=True,
            )
        else:
            st.caption("Belum ada fakta Iya yang mengaktifkan aturan.")

        if not hasil:
            st.caption(
                "Tidak ada aturan yang terpicu, sehingga mesin tidak "
                "menghasilkan kandidat cheat."
            )
            return

        utama = hasil[0]
        st.markdown(
            f"**2. Rule matching — aturan yang terpicu untuk "
            f"{html.escape(utama['nama'])}**"
        )
        st.dataframe(
            [
                {
                    "Aturan": langkah["kode_aturan"],
                    "Gejala": langkah["kode_gejala"],
                    "CF pengguna": f"{langkah['cf_user']:.1f}",
                    "CF pakar": f"{langkah['cf_pakar']:.1f}",
                    "CF aturan": f"{langkah['cf_aturan']:.2f}",
                    "CF sebelum": f"{langkah['cf_lama']:.2f}",
                    "CF sesudah": f"{langkah['cf_gabungan']:.2f}",
                }
                for langkah in utama["aturan_terpicu"]
            ],
            hide_index=True,
        )

        st.markdown("**3. Certainty factor — agregasi keyakinan**")
        st.code(
            "CF aturan   = CF pengguna x CF pakar\n"
            "CF gabungan = CF lama + CF baru x (1 - CF lama)\n"
            "Persentase  = CF gabungan x 100",
            language="text",
        )
        st.caption(
            "Aturan dieksekusi berurutan. CF sesudah pada baris terakhir "
            "menjadi CF gabungan kandidat teratas."
        )

        st.markdown("**4. Explanation — kesimpulan dan peringkat**")
        peringkat = " · ".join(
            f"{html.escape(item['nama'])} {item['persen']:.1f}%"
            for item in hasil[:3]
        )
        st.markdown(
            f'<div class="trace-conclusion">'
            f"Kesimpulan: <strong>{html.escape(explain.judul_hasil(utama))}</strong>"
            f"<br>Peringkat: {peringkat}"
            f"</div>",
            unsafe_allow_html=True,
        )


def _kartu_utama(item):
    lebar = int(round(min(max(item["cf_gabungan"], 0.0), 1.0) * 100))
    alasan = "".join(
        f"<li>{html.escape(teks)}</li>" for teks in explain.alasan_hasil(item)
    )
    sumber = explain.sumber_terpicu(item, peta_sumber)
    saran = item["saran"] or (
        "Rekam ulang pertandingan, bandingkan dengan pemain lain, lalu "
        "laporkan ke GM dengan bukti video."
    )
    return (
        '<div class="hasil-kartu utama">'
        f'<div class="hasil-nama">HASIL: '
        f"{html.escape(explain.judul_hasil(item))}</div>"
        f'<div class="bar"><span style="width:{lebar}%"></span></div>'
        f'<div class="hasil-arti">{html.escape(explain.arti_hasil(item))}</div>'
        '<div class="hasil-bagian">Kenapa sistem menyimpulkan ini:</div>'
        f'<ul class="hasil-alasan">{alasan}</ul>'
        '<div class="hasil-bagian">Yang sebaiknya kamu lakukan:</div>'
        f'<div class="hasil-saran">{html.escape(saran)}</div>'
        f'<div class="hasil-catatan">'
        f"{html.escape(explain.CATATAN_INDIKASI)}</div>"
        "<details><summary>Lihat rincian perhitungan</summary>"
        f"<pre>{_rincian(item)}</pre></details>"
        "<details><summary>Lihat sumber ilmiah</summary>"
        f'<div class="daftar-sumber">{_isi_sumber(sumber)}</div></details>'
        "</div>"
    )


def _kartu_lain(item):
    lebar = int(round(min(max(item["cf_gabungan"], 0.0), 1.0) * 100))
    sumber = explain.sumber_terpicu(item, peta_sumber)
    return (
        '<div class="hasil-kartu">'
        f'<div class="hasil-nama">HASIL: '
        f"{html.escape(explain.judul_hasil(item))}</div>"
        f'<div class="bar"><span style="width:{lebar}%"></span></div>'
        f'<div class="hasil-arti">{html.escape(explain.arti_hasil(item))}</div>'
        "<details><summary>Lihat rincian perhitungan</summary>"
        f"<pre>{_rincian(item)}</pre></details>"
        "<details><summary>Lihat sumber ilmiah</summary>"
        f'<div class="daftar-sumber">{_isi_sumber(sumber)}</div></details>'
        "</div>"
    )


def _isi_hasil(hasil):
    if not hasil:
        return (
            '<div class="hasil-kartu">'
            '<div class="hasil-nama">HASIL: tidak ada kesimpulan</div>'
            '<div class="hasil-arti">Tidak ada jenis cheat yang dapat '
            "disimpulkan dari jawabanmu.</div></div>"
        )
    bagian = [_kartu_utama(hasil[0])]
    if len(hasil) > 1:
        bagian.append('<div class="hasil-bagian">Indikasi lain</div>')
        bagian.extend(_kartu_lain(item) for item in hasil[1:])
    return "".join(bagian)


def _gelembung(pesan):
    bot = pesan["peran"] == "bot"
    kelas = "bot" if bot else "user"
    avatar = "AI" if bot else "ME"
    if pesan.get("tipe") == "hasil":
        isi = _isi_hasil(pesan["hasil"])
    elif pesan.get("tipe") == "peringatan":
        isi = (
            '<div class="peringatan-chat">'
            f'{html.escape(pesan.get("teks", ""))}</div>'
        )
    else:
        isi = html.escape(pesan.get("teks", "")).replace("\n", "<br>")
    return (
        f'<div class="baris-pesan {kelas}">'
        f'<div class="avatar">{avatar}</div>'
        f'<div class="gelembung {kelas}">{isi}</div>'
        "</div>"
    )


def _render_dialog():
    isi = "".join(_gelembung(pesan) for pesan in st.session_state["dialog"])
    st.markdown(f'<div class="jendela-chat">{isi}</div>', unsafe_allow_html=True)


if "tahap" not in st.session_state:
    _mulai()

if st.sidebar.button("Mulai ulang", key="tombol_ulang"):
    _mulai()
    st.rerun()

label_tahap = {
    "nama": "Akuisisi identitas",
    "tanya": "Wawancara gejala",
    "selesai": "Inferensi selesai",
}.get(st.session_state.get("tahap"), "Siaga")
with st.sidebar:
    st.markdown(
        f"""
        <div class="sidebar-panel">
            <div class="sidebar-title">Status inferensi</div>
            <div class="sidebar-row"><span>Tahap</span><strong>{label_tahap}</strong></div>
            <div class="sidebar-row"><span>Fakta aktif</span><strong>{len(st.session_state.get("pilihan", {}))}</strong></div>
            <div class="sidebar-row"><span>Gejala aktif</span><strong>{st.session_state.get("kode_aktif") or "—"}</strong></div>
            <div class="sidebar-row"><span>Aturan</span><strong>{len(daftar_aturan)}</strong></div>
            <div class="sidebar-row"><span>Model</span><strong>FC + CF</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if not st.session_state["dialog"]:
    _kirim(
        "bot",
        f"{percakapan.ambil_pembuka()}\n"
        "Sebelum mulai, siapa nama pemain yang mau diperiksa?",
    )

ui.judul_halaman(
    "Diagnosa",
    "Konsol wawancara gejala dengan mesin inferensi forward chaining dan "
    "certainty factor. Setiap fakta, aturan, dan nilai CF dapat ditelusuri.",
)

total_gejala = max(len(daftar_gejala), 1)
terjawab = min(st.session_state.get("jumlah_tanya", 0), total_gejala)
progres = 1.0 if st.session_state.get("tahap") == "selesai" else terjawab / total_gejala
st.markdown(
    f"""
    <div class="console-bar">
        <span class="label">Session</span>
        <span class="pill ok"><span class="status-dot"></span> Engine aktif</span>
        <span class="pill">Forward chaining</span>
        <span class="pill">Certainty factor</span>
        <span class="pill">Fakta {len(st.session_state.get("pilihan", {}))}</span>
        <span class="pill">Pertanyaan {terjawab}/{total_gejala}</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.progress(
    min(max(progres, 0.0), 1.0),
    text=f"Progres wawancara: {terjawab} dari {total_gejala} gejala ditanyakan",
)

with st.expander("Basis pertanyaan — 13 gejala, jawaban Iya atau Tidak"):
    st.caption(
        "PB-Bot memilih salah satu varian pertanyaan untuk setiap gejala. "
        "Jawaban Tidak tidak mengaktifkan aturan gejala tersebut."
    )
    st.dataframe(
        [
            {
                "Kode": gejala["kode"],
                "Gejala": gejala["deskripsi"],
                "Pertanyaan utama": (
                    percakapan.PERTANYAAN.get(gejala["kode"])
                    or [
                        f"Apakah kamu melihat gejala {gejala['kode']} pada pemain tersebut?"
                    ]
                )[0],
            }
            for gejala in daftar_gejala
        ],
        hide_index=True,
    )
    st.caption("Semua varian pertanyaan")
    st.dataframe(
        [
            {"Kode": gejala["kode"], "Pertanyaan": pertanyaan}
            for gejala in daftar_gejala
            for pertanyaan in (
                percakapan.PERTANYAAN.get(gejala["kode"])
                or [
                    f"Apakah kamu melihat gejala {gejala['kode']} pada pemain tersebut?"
                ]
            )
        ],
        hide_index=True,
    )

_render_dialog()
tahap = st.session_state["tahap"]

if tahap == "nama":
    st.markdown(
        '<div class="petunjuk-chat">Ketik nama di kolom bawah, atau lewati.</div>',
        unsafe_allow_html=True,
    )
    if st.button("Lewati", key="lewati_nama"):
        _kirim("user", "(tanpa nama)")
        _kirim("bot", "Baik, tanpa nama. Kita mulai ya.")
        _tanya_gejala()
        st.rerun()
    nama = st.chat_input("Ketik nama pemain...", key="input_nama")
    if nama:
        st.session_state["nama"] = nama.strip()
        _kirim("user", st.session_state["nama"])
        _kirim("bot", f"Siap, {st.session_state['nama']}. Kita mulai ya.")
        _tanya_gejala()
        st.rerun()

elif tahap == "tanya":
    kode = st.session_state["kode_aktif"]
    st.markdown(
        '<div class="petunjuk-chat">Pilih jawaban:</div>', unsafe_allow_html=True
    )
    kolom = st.columns(len(percakapan.PILIHAN_JAWABAN))
    for kolom_jawab, (label, nilai) in zip(kolom, percakapan.PILIHAN_JAWABAN):
        kunci = f"jawab_{kode}_{label.lower().replace(' ', '_')}"
        if kolom_jawab.button(label, key=kunci):
            _kirim("user", label)
            if nilai:
                st.session_state["pilihan"][kode] = nilai
            _lanjut()
            st.rerun()

elif tahap == "selesai":
    st.markdown(
        '<div class="petunjuk-chat">Percakapan selesai.</div>',
        unsafe_allow_html=True,
    )
    kolom_simpan, kolom_pdf, kolom_baru = st.columns(3)
    if st.session_state.get("sudah_simpan"):
        kolom_simpan.caption("Riwayat sudah disimpan.")
    else:
        if kolom_simpan.button("Simpan ke riwayat", key="simpan_riwayat"):
            history.simpan_riwayat(
                conn,
                st.session_state.get("nama", ""),
                st.session_state.get("pilihan", {}),
                st.session_state.get("hasil", []),
            )
            st.session_state["sudah_simpan"] = True
            _kirim("bot", "Riwayat berhasil disimpan. Terima kasih.")
            st.rerun()
    data_pdf, berkas_pdf = laporan_pdf.buat_pdf_hasil(
        st.session_state.get("nama", ""),
        st.session_state.get("pilihan", {}),
        st.session_state.get("hasil", []),
        peta_gejala,
        peta_sumber,
        peringatan=st.session_state.get("peringatan", False),
    )
    kolom_pdf.download_button(
        "Cetak PDF",
        data=data_pdf,
        file_name=berkas_pdf,
        mime="application/pdf",
        key="unduh_pdf_hasil",
    )
    if kolom_baru.button("Diagnosa baru", key="diagnosa_baru"):
        _mulai()
        st.rerun()

if st.session_state.get("tahap") == "selesai" and "hasil" in st.session_state:
    _render_jejak()
