import streamlit as st
import pandas as pd
import numpy as np

# ======================================================
# KONFIGURASI HALAMAN
# ======================================================

st.set_page_config(
    page_title="SPK Platform AI",
    page_icon="🤖",
    layout="wide"
)

# ======================================================
# JUDUL
# ======================================================

st.title("🤖 Sistem Pendukung Keputusan Pemilihan Platform AI")
st.subheader("Metode AHP - TOPSIS")

st.markdown("""
Sistem ini digunakan untuk membantu mahasiswa menentukan 
platform AI terbaik untuk menunjang produktivitas akademik 
menggunakan metode AHP dan TOPSIS.
""")

# ======================================================
# DATA KRITERIA DAN BOBOT AHP
# ======================================================

kriteria = [
    "Akurasi Jawaban",
    "Kemudahan Penggunaan",
    "Kecepatan Respon",
    "Kelengkapan Fitur Gratis",
    "Kemampuan Membantu Akademik",
    "Keamanan Data dan Privasi"
]

# Bobot hasil AHP
bobot = np.array([
    0.46,
    0.18,
    0.10,
    0.04,
    0.15,
    0.07
])

# ======================================================
# DATA ALTERNATIF HASIL AHP
# ======================================================

alternatif = [
    "ChatGPT",
    "Gemini",
    "Claude",
    "Microsoft Copilot",
    "Perplexity AI"
]

data_awal = pd.DataFrame({
    "Alternatif": alternatif,
    "Akurasi Jawaban": [0.34, 0.13, 0.34, 0.06, 0.13],
    "Kemudahan Penggunaan": [0.44, 0.17, 0.17, 0.17, 0.06],
    "Kecepatan Respon": [0.23, 0.23, 0.08, 0.23, 0.23],
    "Kelengkapan Fitur Gratis": [0.13, 0.34, 0.06, 0.13, 0.34],
    "Kemampuan Membantu Akademik": [0.34, 0.13, 0.34, 0.06, 0.13],
    "Keamanan Data dan Privasi": [0.17, 0.17, 0.44, 0.17, 0.06]
})

# ======================================================
# SIDEBAR MENU
# ======================================================

st.sidebar.title("📋 Menu")

menu = st.sidebar.radio(
    "Pilih Halaman",
    [
        "Dashboard",
        "Data Alternatif",
        "Bobot AHP",
        "Perhitungan TOPSIS",
        "Hasil Ranking"
    ]
)

# ======================================================
# DASHBOARD
# ======================================================

if menu == "Dashboard":

    st.header("📌 Dashboard")

    st.write("""
    Sistem Pendukung Keputusan ini digunakan untuk menentukan 
    platform AI terbaik berdasarkan beberapa kriteria menggunakan 
    metode AHP-TOPSIS.
    """)

    st.subheader("🎯 Tujuan Sistem")

    st.write("""
    Membantu mahasiswa memilih platform AI terbaik 
    untuk meningkatkan produktivitas akademik.
    """)

    st.subheader("📊 Kriteria")

    for i, k in enumerate(kriteria):
        st.write(f"C{i+1} : {k}")

# ======================================================
# DATA ALTERNATIF
# ======================================================

elif menu == "Data Alternatif":

    st.header("📥 Data Alternatif")

    st.write("""
    Berikut merupakan data alternatif hasil perhitungan AHP 
    untuk masing-masing kriteria.
    """)

    st.dataframe(
        data_awal,
        use_container_width=True
    )

# ======================================================
# BOBOT AHP
# ======================================================

elif menu == "Bobot AHP":

    st.header("⚖️ Bobot Kriteria AHP")

    bobot_df = pd.DataFrame({
        "Kriteria": kriteria,
        "Bobot": bobot
    })

    st.dataframe(
        bobot_df.style.format({
            "Bobot": "{:.2f}"
        }),
        use_container_width=True
    )

    st.subheader("📌 Hasil Ranking AHP")

    hasil_ahp = pd.DataFrame({
        "Alternatif": [
            "ChatGPT",
            "Claude",
            "Gemini",
            "Perplexity AI",
            "Microsoft Copilot"
        ],
        "Nilai": [
            0.2754,
            0.2374,
            0.1938,
            0.1598,
            0.1337
        ],
        "Ranking": [1, 2, 3, 4, 5]
    })

    st.dataframe(
        hasil_ahp.style.format({
            "Nilai": "{:.4f}"
        }),
        use_container_width=True
    )

# ======================================================
# PERHITUNGAN TOPSIS
# ======================================================

elif menu == "Perhitungan TOPSIS":

    st.header("🧮 Perhitungan TOPSIS")

    data_nilai = data_awal.iloc[:, 1:].values.astype(float)

    # ==================================================
    # NORMALISASI
    # ==================================================

    pembagi = np.sqrt(np.sum(data_nilai**2, axis=0))

    normalisasi = data_nilai / pembagi

    normalisasi_df = pd.DataFrame(
        normalisasi,
        columns=kriteria,
        index=alternatif
    )

    st.subheader("1️⃣ Matriks Normalisasi")

    st.dataframe(
        normalisasi_df.style.format("{:.4f}"),
        use_container_width=True
    )

    # ==================================================
    # NORMALISASI TERBOBOT
    # ==================================================

    terbobot = normalisasi * bobot

    terbobot_df = pd.DataFrame(
        terbobot,
        columns=kriteria,
        index=alternatif
    )

    st.subheader("2️⃣ Matriks Ternormalisasi Terbobot")

    st.dataframe(
        terbobot_df.style.format("{:.4f}"),
        use_container_width=True
    )

    # ==================================================
    # SOLUSI IDEAL
    # ==================================================

    ideal_positif = np.max(terbobot, axis=0)
    ideal_negatif = np.min(terbobot, axis=0)

    solusi_df = pd.DataFrame({
        "Kriteria": kriteria,
        "Ideal Positif": ideal_positif,
        "Ideal Negatif": ideal_negatif
    })

    st.subheader("3️⃣ Solusi Ideal")

    st.dataframe(
        solusi_df.style.format({
            "Ideal Positif": "{:.4f}",
            "Ideal Negatif": "{:.4f}"
        }),
        use_container_width=True
    )

# ======================================================
# HASIL RANKING TOPSIS
# ======================================================

elif menu == "Hasil Ranking":

    st.header("🏆 Hasil Ranking TOPSIS")

    data_nilai = data_awal.iloc[:, 1:].values.astype(float)

    # ==================================================
    # NORMALISASI
    # ==================================================

    pembagi = np.sqrt(np.sum(data_nilai**2, axis=0))
    normalisasi = data_nilai / pembagi

    # ==================================================
    # TERBOBOT
    # ==================================================

    terbobot = normalisasi * bobot

    # ==================================================
    # SOLUSI IDEAL
    # ==================================================

    ideal_positif = np.max(terbobot, axis=0)
    ideal_negatif = np.min(terbobot, axis=0)

    # ==================================================
    # JARAK SOLUSI
    # ==================================================

    d_positif = np.sqrt(
        np.sum((terbobot - ideal_positif)**2, axis=1)
    )

    d_negatif = np.sqrt(
        np.sum((terbobot - ideal_negatif)**2, axis=1)
    )

    # ==================================================
    # NILAI PREFERENSI
    # ==================================================

    preferensi = d_negatif / (d_positif + d_negatif)

    hasil = pd.DataFrame({
        "Alternatif": alternatif,
        "Nilai Preferensi": preferensi
    })

    hasil["Ranking"] = hasil["Nilai Preferensi"].rank(
        ascending=False,
        method="min"
    ).astype(int)

    hasil = hasil.sort_values(
        by="Nilai Preferensi",
        ascending=False
    )

    # ==================================================
    # TABEL HASIL
    # ==================================================

    st.dataframe(
        hasil.style.format({
            "Nilai Preferensi": "{:.4f}"
        }),
        use_container_width=True
    )

    # ==================================================
    # GRAFIK
    # ==================================================

    st.subheader("📈 Grafik Ranking")

    st.bar_chart(
        hasil.set_index("Alternatif")["Nilai Preferensi"]
    )

    # ==================================================
    # REKOMENDASI
    # ==================================================

    terbaik = hasil.iloc[0]

    st.success(
        f"""
        Rekomendasi Platform AI Terbaik adalah 
        {terbaik['Alternatif']} 
        dengan nilai preferensi sebesar 
        {terbaik['Nilai Preferensi']:.4f}
        """
    )
