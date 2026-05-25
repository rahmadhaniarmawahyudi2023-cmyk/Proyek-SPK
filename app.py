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
# JUDUL DASHBOARD
# =========================================================

st.title("🤖 Sistem Pendukung Keputusan Pemilihan Platform AI")
st.subheader("Metode AHP - TOPSIS")

st.markdown("""
Sistem ini digunakan untuk membantu mahasiswa menentukan 
platform AI terbaik untuk menunjang produktivitas akademik 
berdasarkan beberapa kriteria menggunakan metode AHP-TOPSIS.
""")

# =========================================================
# DATA KRITERIA
# =========================================================

kriteria = [
    "Akurasi Jawaban",
    "Kemudahan Penggunaan",
    "Kecepatan Respon",
    "Kelengkapan Fitur Gratis",
    "Kemampuan Membantu Akademik",
    "Keamanan Data dan Privasi"
]

# =========================================================
# SIDEBAR MENU
# =========================================================

st.sidebar.title("📋 Menu Dashboard")

menu = st.sidebar.radio(
    "Pilih Menu",
    [
        "Dashboard",
        "Input Bobot AHP",
        "Input Data Alternatif",
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
    Dashboard ini digunakan untuk membantu proses pengambilan keputusan 
    dalam pemilihan platform AI terbaik untuk mahasiswa.
    """)

    st.subheader("🎯 Tujuan Sistem")

    st.write("""
    Membantu mahasiswa memilih platform AI terbaik 
    berdasarkan beberapa kriteria menggunakan metode AHP-TOPSIS.
    """)

    st.subheader("📊 Kriteria")

    for i, k in enumerate(kriteria):
        st.write(f"C{i+1} : {k}")

    st.subheader("🤖 Alternatif")

    alternatif_dashboard = [
        "ChatGPT",
        "Gemini",
        "Claude",
        "Microsoft Copilot",
        "Perplexity AI"
    ]

    for alt in alternatif_dashboard:
        st.write(f"- {alt}")

# =========================================================
# INPUT BOBOT AHP
# =========================================================

elif menu == "Input Bobot AHP":

    st.header("⚖️ Input Bobot Kriteria AHP")

    st.write("""
    Masukkan bobot hasil perhitungan AHP untuk masing-masing kriteria.
    """)

    c1 = st.number_input(
        "Bobot Akurasi Jawaban",
        min_value=0.0,
        max_value=1.0,
        value=0.46,
        step=0.01
    )

    c2 = st.number_input(
        "Bobot Kemudahan Penggunaan",
        min_value=0.0,
        max_value=1.0,
        value=0.18,
        step=0.01
    )

    c3 = st.number_input(
        "Bobot Kecepatan Respon",
        min_value=0.0,
        max_value=1.0,
        value=0.10,
        step=0.01
    )

    c4 = st.number_input(
        "Bobot Kelengkapan Fitur Gratis",
        min_value=0.0,
        max_value=1.0,
        value=0.04,
        step=0.01
    )

    c5 = st.number_input(
        "Bobot Kemampuan Membantu Akademik",
        min_value=0.0,
        max_value=1.0,
        value=0.15,
        step=0.01
    )

    c6 = st.number_input(
        "Bobot Keamanan Data dan Privasi",
        min_value=0.0,
        max_value=1.0,
        value=0.07,
        step=0.01
    )

    bobot = np.array([c1, c2, c3, c4, c5, c6])

    total_bobot = np.sum(bobot)

    st.write(f"### Total Bobot = {total_bobot:.2f}")

    if total_bobot != 1:
        st.warning("⚠️ Total bobot sebaiknya bernilai 1.")
    else:
        st.success("✅ Total bobot sudah sesuai.")

# =========================================================
# INPUT DATA ALTERNATIF
# =========================================================

elif menu == "Input Data Alternatif":

    st.header("📥 Input Data Alternatif")

    st.write("""
    Masukkan nilai alternatif terhadap masing-masing kriteria.
    """)

    alternatif = [
        "ChatGPT",
        "Gemini",
        "Claude",
        "Microsoft Copilot",
        "Perplexity AI"
    ]

    default_data = pd.DataFrame({
        "Alternatif": alternatif,
        "Akurasi Jawaban": [0.34, 0.13, 0.34, 0.06, 0.13],
        "Kemudahan Penggunaan": [0.44, 0.17, 0.17, 0.17, 0.06],
        "Kecepatan Respon": [0.23, 0.23, 0.08, 0.23, 0.23],
        "Kelengkapan Fitur Gratis": [0.13, 0.34, 0.06, 0.13, 0.34],
        "Kemampuan Membantu Akademik": [0.34, 0.13, 0.34, 0.06, 0.13],
        "Keamanan Data dan Privasi": [0.17, 0.17, 0.44, 0.17, 0.06]
    })

    edited_df = st.data_editor(
        default_data,
        use_container_width=True,
        num_rows="fixed"
    )

    st.session_state["data_alternatif"] = edited_df

    st.success("✅ Data alternatif berhasil disimpan.")

# =========================================================
# PERHITUNGAN TOPSIS
# =========================================================

elif menu == "Perhitungan TOPSIS":

    st.header("🧮 Perhitungan TOPSIS")

    # ============================================
    # AMBIL DATA
    # ============================================

    if "data_alternatif" not in st.session_state:

        st.warning("⚠️ Silakan input data alternatif terlebih dahulu.")

    else:

        data_awal = st.session_state["data_alternatif"]

        # ========================================
        # BOBOT
        # ========================================

        bobot = np.array([0.46, 0.18, 0.10, 0.04, 0.15, 0.07])

        alternatif = data_awal["Alternatif"]

        data_nilai = data_awal.iloc[:, 1:].values.astype(float)

        # ========================================
        # NORMALISASI
        # ========================================

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

        # ========================================
        # NORMALISASI TERBOBOT
        # ========================================

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

        # ========================================
        # SOLUSI IDEAL
        # ========================================

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

        bobot = np.array([0.46, 0.18, 0.10, 0.04, 0.15, 0.07])

        alternatif = data_awal["Alternatif"]

        data_nilai = data_awal.iloc[:, 1:].values.astype(float)

        # ========================================
        # NORMALISASI
        # ========================================

        pembagi = np.sqrt(np.sum(data_nilai**2, axis=0))

        normalisasi = data_nilai / pembagi

        # ========================================
        # TERBOBOT
        # ========================================

        terbobot = normalisasi * bobot

        # ========================================
        # SOLUSI IDEAL
        # ========================================

        ideal_positif = np.max(terbobot, axis=0)

        ideal_negatif = np.min(terbobot, axis=0)

        # ========================================
        # JARAK SOLUSI
        # ========================================

        d_positif = np.sqrt(
            np.sum((terbobot - ideal_positif)**2, axis=1)
        )

        d_negatif = np.sqrt(
            np.sum((terbobot - ideal_negatif)**2, axis=1)
        )

        # ========================================
        # NILAI PREFERENSI
        # ========================================

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

        # ========================================
        # OUTPUT HASIL
        # ========================================

        st.dataframe(
            hasil.style.format({
                "Nilai Preferensi": "{:.4f}"
            }),
            use_container_width=True
        )

        # ========================================
        # VISUALISASI
        # ========================================

        st.subheader("📈 Grafik Ranking")

        st.bar_chart(
            hasil.set_index("Alternatif")["Nilai Preferensi"]
        )

        # ========================================
        # REKOMENDASI
        # ========================================

        terbaik = hasil.iloc[0]

        st.success(
            f"""
            Rekomendasi Platform AI Terbaik adalah 
            {terbaik['Alternatif']} 
            dengan nilai preferensi sebesar 
            {terbaik['Nilai Preferensi']:.4f}
            """
        )

        # ========================================
        # DOWNLOAD CSV
        # ========================================

        csv = hasil.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="⬇️ Download Hasil Ranking",
            data=csv,
            file_name='hasil_ranking_topsis.csv',
            mime='text/csv'
        )
