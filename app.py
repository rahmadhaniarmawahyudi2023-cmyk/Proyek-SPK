import streamlit as st
import pandas as pd
import numpy as np

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="SPK Platform AI",
    page_icon="🤖",
    layout="wide"
)

# =========================================================
# JUDUL
# =========================================================

st.title("🤖 Sistem Pendukung Keputusan Pemilihan Platform AI")
st.subheader("Metode AHP - TOPSIS")

st.markdown("""
Sistem ini digunakan untuk membantu mahasiswa menentukan 
platform AI terbaik berdasarkan beberapa kriteria 
menggunakan metode AHP-TOPSIS.
""")

# =========================================================
# KRITERIA DAN BOBOT AHP
# =========================================================

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

# =========================================================
# SIDEBAR MENU
# =========================================================

st.sidebar.title("📋 Menu Dashboard")

menu = st.sidebar.radio(
    "Pilih Menu",
    [
        "Dashboard",
        "Bobot AHP",
        "Input Alternatif",
        "Perhitungan TOPSIS",
        "Hasil Ranking"
    ]
)

# =========================================================
# DASHBOARD
# =========================================================

if menu == "Dashboard":

    st.header("📌 Dashboard")

    st.write("""
    Sistem Pendukung Keputusan ini digunakan untuk membantu 
    mahasiswa memilih platform AI terbaik menggunakan 
    metode AHP-TOPSIS.
    """)

    st.subheader("🎯 Tujuan Sistem")

    st.write("""
    Membantu proses pengambilan keputusan dalam pemilihan 
    platform AI terbaik untuk menunjang aktivitas akademik mahasiswa.
    """)

    st.subheader("📊 Kriteria")

    for i, k in enumerate(kriteria):
        st.write(f"C{i+1} : {k}")

# =========================================================
# BOBOT AHP
# =========================================================

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

    st.success("✅ Bobot diperoleh dari hasil perhitungan metode AHP.")

# =========================================================
# INPUT ALTERNATIF
# =========================================================

elif menu == "Input Alternatif":

    st.header("📥 Input Data Alternatif")

    st.write("""
    Tambahkan alternatif dan masukkan nilai untuk setiap kriteria.
    """)

    # =====================================================
    # DEFAULT DATA
    # =====================================================

    default_data = pd.DataFrame({
        "Alternatif": [
            "ChatGPT",
            "Gemini",
            "Claude",
            "Microsoft Copilot",
            "Perplexity AI"
        ],

        "Akurasi Jawaban": [0.34, 0.13, 0.34, 0.06, 0.13],

        "Kemudahan Penggunaan": [0.44, 0.17, 0.17, 0.17, 0.06],

        "Kecepatan Respon": [0.23, 0.23, 0.08, 0.23, 0.23],

        "Kelengkapan Fitur Gratis": [0.13, 0.34, 0.06, 0.13, 0.34],

        "Kemampuan Membantu Akademik": [0.34, 0.13, 0.34, 0.06, 0.13],

        "Keamanan Data dan Privasi": [0.17, 0.17, 0.44, 0.17, 0.06]
    })

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "data_alternatif" not in st.session_state:
        st.session_state["data_alternatif"] = default_data

    # =====================================================
    # DATA EDITOR
    # =====================================================

    edited_df = st.data_editor(
        st.session_state["data_alternatif"],
        use_container_width=True,
        num_rows="dynamic"
    )

    st.session_state["data_alternatif"] = edited_df

    st.success("✅ Data alternatif berhasil disimpan.")

# =========================================================
# PERHITUNGAN TOPSIS
# =========================================================

elif menu == "Perhitungan TOPSIS":

    st.header("🧮 Perhitungan TOPSIS")

    if "data_alternatif" not in st.session_state:

        st.warning("⚠️ Silakan input data alternatif terlebih dahulu.")

    else:

        data_awal = st.session_state["data_alternatif"]

        alternatif = data_awal["Alternatif"]

        data_nilai = data_awal.iloc[:, 1:].values.astype(float)

        # =================================================
        # NORMALISASI
        # =================================================

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

        # =================================================
        # NORMALISASI TERBOBOT
        # =================================================

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

        # =================================================
        # SOLUSI IDEAL
        # =================================================

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

# =========================================================
# HASIL RANKING
# =========================================================

elif menu == "Hasil Ranking":

    st.header("🏆 Hasil Ranking TOPSIS")

    if "data_alternatif" not in st.session_state:

        st.warning("⚠️ Silakan input data alternatif terlebih dahulu.")

    else:

        data_awal = st.session_state["data_alternatif"]

        alternatif = data_awal["Alternatif"]

        data_nilai = data_awal.iloc[:, 1:].values.astype(float)

        # =================================================
        # NORMALISASI
        # =================================================

        pembagi = np.sqrt(np.sum(data_nilai**2, axis=0))

        normalisasi = data_nilai / pembagi

        # =================================================
        # NORMALISASI TERBOBOT
        # =================================================

        terbobot = normalisasi * bobot

        # =================================================
        # SOLUSI IDEAL
        # =================================================

        ideal_positif = np.max(terbobot, axis=0)

        ideal_negatif = np.min(terbobot, axis=0)

        # =================================================
        # JARAK SOLUSI IDEAL
        # =================================================

        d_positif = np.sqrt(
            np.sum((terbobot - ideal_positif)**2, axis=1)
        )

        d_negatif = np.sqrt(
            np.sum((terbobot - ideal_negatif)**2, axis=1)
        )

        # =================================================
        # NILAI PREFERENSI
        # =================================================

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

        # =================================================
        # OUTPUT TABEL
        # =================================================

        st.dataframe(
            hasil.style.format({
                "Nilai Preferensi": "{:.4f}"
            }),
            use_container_width=True
        )

        # =================================================
        # GRAFIK
        # =================================================

        st.subheader("📈 Grafik Ranking")

        st.bar_chart(
            hasil.set_index("Alternatif")["Nilai Preferensi"]
        )

        # =================================================
        # REKOMENDASI
        # =================================================

        terbaik = hasil.iloc[0]

        st.success(
            f"""
            Rekomendasi Platform AI Terbaik adalah 
            {terbaik['Alternatif']} 
            dengan nilai preferensi sebesar 
            {terbaik['Nilai Preferensi']:.4f}
            """
        )

        # =================================================
        # DOWNLOAD CSV
        # =================================================

        csv = hasil.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="⬇️ Download Hasil Ranking",
            data=csv,
            file_name='hasil_ranking_topsis.csv',
            mime='text/csv'
        )
