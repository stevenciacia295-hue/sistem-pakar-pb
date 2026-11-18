"""Panduan gejala: arti, penyebab, dan cara penyelesaian. Tanpa Streamlit."""

CATATAN = (
    "Ciri ini bisa juga muncul karena keterampilan, ping tinggi, atau bug "
    "permainan. Hasil sistem hanya indikasi, bukan bukti pasti."
)

PANDUAN_GEJALA = {
    "G01": {
        "apa": (
            "Pemain mendapat headshot jauh lebih sering daripada pemain lain, "
            "dan polanya tetap tinggi dari ronde ke ronde."
        ),
        "mengapa": (
            "Aimbot dapat mengarahkan tembakan ke kepala secara otomatis. "
            "Pemain yang sangat terlatih juga bisa memiliki headshot rate "
            "tinggi, sehingga perlu bukti tambahan."
        ),
        "solusi": [
            "Bandingkan headshot rate pemain dengan rata-rata pemain di ronde yang sama.",
            "Tonton beberapa ronde, bukan hanya satu momen, untuk melihat apakah polanya konsisten.",
            "Minta atau simpan rekaman POV agar gerakan bidikan bisa diperiksa.",
            "Laporkan ke GM dengan statistik dan video pendukung, bukan tuduhan lisan saja.",
        ],
    },
    "G02": {
        "apa": (
            "Crosshair terlihat langsung menempel atau mengunci ke kepala musuh "
            "tanpa gerakan mouse yang wajar."
        ),
        "mengapa": (
            "Fitur snap aim atau aim lock pada aimbot mengoreksi bidikan dalam "
            "waktu yang sangat singkat, sering terlihat patah-patah."
        ),
        "solusi": [
            "Periksa rekaman gerakan mouse atau POV pemain.",
            "Perhatikan apakah bidikan melompat tajam ke kepala lalu menempel.",
            "Bandingkan dengan flick manual pemain berpengalaman yang masih punya lintasan gerak.",
            "Simpan klip momen mencurigakan dan laporkan ke GM.",
        ],
    },
    "G03": {
        "apa": (
            "Pemain menembak nyaris seketika saat musuh muncul, seolah tanpa "
            "waktu reaksi manusia."
        ),
        "mengapa": (
            "Triggerbot atau aimbot dapat menembak otomatis begitu crosshair "
            "mengenai target. Reaksi cepat wajar tetap punya jeda kecil."
        ),
        "solusi": [
            "Tonton klip frame demi frame untuk memperkirakan waktu reaksi.",
            "Bandingkan reaksi saat pemain siap dan saat benar-benar terkejut.",
            "Cek apakah tembakan selalu keluar tepat saat target melewati crosshair.",
            "Kumpulkan beberapa klip lalu laporkan ke GM.",
        ],
    },
    "G04": {
        "apa": (
            "Tembakan jarak jauh hampir selalu mengenai sasaran, termasuk "
            "target yang bergerak."
        ),
        "mengapa": (
            "Aimbot dapat mengompensasi jarak dan pergerakan target. Namun "
            "akurasi tinggi juga bisa berasal dari latihan dan penguasaan senjata."
        ),
        "solusi": [
            "Uji dengan senjata dan jarak yang sama seperti yang dipakai pemain.",
            "Bandingkan hasilnya dengan pemain wajar di kondisi serupa.",
            "Perhatikan apakah ada koreksi bidikan instan yang tidak wajar.",
            "Rekam bukti dan sertakan konteks senjata serta jaraknya saat melapor.",
        ],
    },
    "G05": {
        "apa": (
            "Pemain membidik atau menembak ke arah musuh yang masih tertutup "
            "tembok atau penghalang."
        ),
        "mengapa": (
            "Wallhack atau ESP menampilkan posisi musuh di balik penghalang, "
            "sehingga pemain tahu arah tanpa melihat target."
        ),
        "solusi": [
            "Simpan replay beberapa ronde yang memuat momen pre-aim.",
            "Pastikan tidak ada informasi suara, radar, atau laporan tim yang membenarkan bidikan tersebut.",
            "Minta rekaman POV untuk melihat apakah crosshair mengikuti target tak terlihat.",
            "Laporkan ke GM dengan timestamp momen yang mencurigakan.",
        ],
    },
    "G06": {
        "apa": (
            "Pemain seperti selalu mengetahui posisi musuh, termasuk saat "
            "musuh bersembunyi atau mencoba mengepung."
        ),
        "mengapa": (
            "ESP atau wallhack menampilkan lokasi musuh. Komunikasi tim yang "
            "baik dan kebiasaan membaca pola lawan juga bisa memberi kesan serupa."
        ),
        "solusi": [
            "Periksa apakah tim pemain memang aktif memberi informasi posisi.",
            "Bandingkan pengetahuan pemain dengan info radar dan suara yang tersedia.",
            "Perhatikan pola menghindar atau menyergap yang terlalu tepat.",
            "Kumpulkan beberapa klip sebelum melapor ke GM.",
        ],
    },
    "G07": {
        "apa": (
            "Crosshair mengikuti pergerakan musuh yang berjalan di balik "
            "penghalang dan tidak terlihat."
        ),
        "mengapa": (
            "Wallhack menampilkan kerangka atau posisi musuh, sehingga bidikan "
            "bisa mengikuti target di balik dinding."
        ),
        "solusi": [
            "Rekam momen ketika crosshair melacak target yang tidak terlihat.",
            "Pastikan tidak ada suara langkah atau informasi tim saat itu.",
            "Ulangi pengamatan di ronde lain untuk melihat apakah polanya berulang.",
            "Laporkan dengan timeline dan klip pendukung.",
        ],
    },
    "G08": {
        "apa": (
            "Saat menembak full-auto, pola peluru tetap lurus dan tidak naik "
            "seperti recoil senjata pada umumnya."
        ),
        "mengapa": (
            "No recoil atau anti-recoil menghapus hentakan senjata. Pemain "
            "terlatih juga bisa menahan recoil, tetapi masih terlihat koreksi mouse."
        ),
        "solusi": [
            "Bandingkan pola spray dengan senjata yang sama pada dinding.",
            "Ukur apakah pola tembakan menyimpang sebagaimana mestinya.",
            "Periksa POV untuk melihat apakah mouse ditarik ke bawah saat menembak.",
            "Laporkan bila pola di luar batas wajar disertai bukti rekaman.",
        ],
    },
    "G09": {
        "apa": (
            "Peluru hampir tidak menyebar, sehingga tembakan beruntun tetap "
            "mengumpul di satu titik."
        ),
        "mengapa": (
            "No spread atau no recoil membuat penyebaran peluru jauh lebih kecil "
            "daripada seharusnya. Kondisi senjata dan posisi juga memengaruhi spread."
        ),
        "solusi": [
            "Uji tembak ke dinding dari jarak yang sama dengan senjata serupa.",
            "Bandingkan spread pemain dengan pemain wajar.",
            "Perhatikan apakah spread tetap kecil saat pemain bergerak.",
            "Simpan rekaman uji dan laporkan ke GM.",
        ],
    },
    "G10": {
        "apa": (
            "Pemain bergerak jauh lebih cepat daripada batas normal karakter "
            "atau pemain lain."
        ),
        "mengapa": (
            "Speedhack menaikkan kecepatan gerak. Ping tinggi, desync, atau "
            "efek tertentu juga bisa membuat gerakan terlihat lebih cepat."
        ),
        "solusi": [
            "Ukur waktu tempuh pemain antar titik peta yang sama.",
            "Bandingkan dengan pemain lain pada kondisi dan jalur serupa.",
            "Periksa ping dan apakah ada tanda desync saat pengamatan.",
            "Rekam momen dan laporkan bila kecepatannya konsisten di luar batas.",
        ],
    },
    "G11": {
        "apa": (
            "Karakter pemain seolah berpindah posisi secara mendadak seperti "
            "teleport tanpa lintasan gerak yang terlihat."
        ),
        "mengapa": (
            "Speedhack berat atau lonjakan jaringan dapat membuat posisi karakter "
            "melompat. Bug permainan juga bisa menghasilkan tampilan serupa."
        ),
        "solusi": [
            "Cek ping dan kestabilan koneksi saat momen itu terjadi.",
            "Ulangi pengamatan untuk memastikan apakah kejadiannya berulang.",
            "Lihat rekaman dari beberapa sudut atau POV pemain lain.",
            "Laporkan dengan timestamp dan klip bila polanya konsisten.",
        ],
    },
    "G12": {
        "apa": (
            "Senjata tetap stabil walau pemain menembak sambil bergerak atau "
            "melompat, padahal biasanya akurasi menurun."
        ),
        "mengapa": (
            "No recoil atau no spread dapat mengabaikan penalti gerak sehingga "
            "akurasi tetap tinggi. Ini ciri tambahan yang memperkuat indikasi."
        ),
        "solusi": [
            "Bandingkan tembakan saat diam dan saat bergerak dengan senjata yang sama.",
            "Uji pada jarak dan posisi yang serupa dengan pemain wajar.",
            "Minta replay untuk melihat apakah akurasi tetap sama saat melompat.",
            "Laporkan bersama bukti pola tembakan yang konsisten.",
        ],
    },
    "G13": {
        "apa": (
            "Senjata dengan hentakan besar terasa ringan dan mudah dikendalikan "
            "saat dipakai pemain tersebut."
        ),
        "mengapa": (
            "Modifikasi recoil membuat senjata berat kehilangan hentakan. "
            "Pengalaman memakai senjata itu juga bisa mengurangi kesan berat."
        ),
        "solusi": [
            "Bandingkan pola tembak senjata yang sama pada pemain lain.",
            "Catat jenis senjata, jarak, dan posisi saat menembak.",
            "Periksa POV apakah recoil benar-benar tidak terjadi.",
            "Laporkan bila senjata berat konsisten terasa ringan di beberapa ronde.",
        ],
    },
}

PANDUAN_UMUM = {
    "apa": "Gejala baru yang belum memiliki panduan khusus.",
    "mengapa": (
        "Penyebabnya perlu diverifikasi langsung oleh pengamat atau pakar."
    ),
    "solusi": [
        "Amati gejala berulang di beberapa ronde.",
        "Kumpulkan rekaman video sebagai bukti.",
        "Laporkan ke GM atau pihak berwenang untuk pemeriksaan lanjutan.",
    ],
}


def get_panduan(kode):
    """Kembalikan panduan satu gejala, atau panduan umum bila tidak dikenal."""
    return PANDUAN_GEJALA.get(str(kode), PANDUAN_UMUM)
