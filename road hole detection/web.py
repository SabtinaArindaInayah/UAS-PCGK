import streamlit as st
import logic
import pandas as pd

# ==========================================
# 1. SETUP HALAMAN
# ==========================================
st.set_page_config(page_title="Road Hole Detection - Kelompok 3", page_icon="🛣️", layout="wide")

# ==========================================
# 2. CSS CUSTOM (FIX UI & WARNA)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    :root {
        --aspal-dark: #1A1A1A;
        --marka-yellow: #FFD700;
        --text-main: #333333;
        --bg-white: #FFFFFF;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-white);
        color: var(--text-main);
    }

    /* HEADER */
    .header-box {
        background: linear-gradient(135deg, #1A1A1A 0%, #333333 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border-bottom: 4px solid var(--marka-yellow);
    }
    .header-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 2px;
        text-transform: uppercase;
    }
    .header-subtitle {
        font-size: 0.9rem;
        color: #DDDDDD;
        font-weight: 300;
    }

    /* KARTU STATISTIK */
    .stat-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #EEEEEE;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        height: 100%;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: transform 0.2s;
    }
    .stat-card:hover {
        transform: translateY(-3px);
        border-color: var(--aspal-dark);
    }
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        margin-top: 5px;
        line-height: 1.2;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #666;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* RINCIAN LUBANG */
    .detail-box {
        width: 100%;
        text-align: left;
        padding-left: 10px;
    }
    .detail-row {
        display: flex;
        justify-content: space-between;
        padding: 6px 0;
        border-bottom: 1px solid #F0F0F0;
        font-size: 0.85rem;
        color: #000000 !important;
    }
    .detail-row span {
        font-weight: 600;
        color: #333333 !important;
    }
    .detail-row b {
        font-weight: 800;
    }

    /* TOMBOL */
    .stButton>button {
        background-color: var(--aspal-dark);
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 8px;
        font-weight: 700;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #333;
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3.LOAD MODEL
# ==========================================
model, status_msg = logic.load_model()

# ==========================================
# 4. HEADER UI
# ==========================================
st.markdown("""
<div class="header-box">
    <div class="header-title">🛣️ ROAD HOLE DETECTION</div>
    <div class="header-subtitle">Analisis Kerusakan Infrastruktur Berbasis Yolov8 dan OpenCV</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. SIDEBAR 
# ==========================================
with st.sidebar:
    # LABEL KELOMPOK 3 DI PALING ATAS
    st.markdown("""
    <div style="text-align: center; background: #2c3e50; padding: 10px; border-radius: 8px; color: white; margin-bottom: 20px;">
        <h2 style="margin:0; font-size:1.5rem;">🏢 KELOMPOK 3</h2>
        <small>Mekatronika dan Kecerdasan Buatan</small>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙️ SETTING")
    if model: st.success(f"Status: {status_msg}")
    else: st.error("Status: Model Hilang")
    
    st.divider()
    conf = st.slider("Akurasi Deteksi", 0.0, 1.0, 0.25, 0.05)
    ratio = st.slider("Filter Jarak (Rasio)", 5.0, 20.0, 12.0)
    clahe = st.checkbox("Mode Penajam (CLAHE)")


    
    st.markdown("---")
    with st.expander("ANGGOTA KELOMPOK 3"):
        st.markdown("""
        1. **Andre Saputra**        
        2. **Khairunnisa Labibah**      
        3. **Sabtina Arinda Inayah**
        4. **Adzka Dzikri**
        5. **M. Farid Febriansyah**
        6. **Primanda Suryawan**
        7. **Andhika Pratama**
        8. **Hafizh 'Abid Khalish**
        9. **Dewi Siti Jamilah**
        10. **Faiz Lintang Prawira**
        11. **Sunan Maulana**
        12. **Rifki Destrizal Nugraha**
        """)

# ==========================================
# 6. INPUT SECTION
# ==========================================
input_mode = st.radio(
    "Sumber Gambar:",
    ("📁 Upload File", "📸 Kamera"),
    horizontal=True,
    label_visibility="collapsed"
)

input_src = None

if input_mode == "📁 Upload File":
    uploaded = st.file_uploader("Pilih gambar jalan rusak...", type=["jpg","png","jpeg"])
    if uploaded: input_src = uploaded

elif input_mode == "📸 Kamera":
    cam = st.camera_input("Ambil foto...")
    if cam: input_src = cam

    # ==========================================
    # 7. LOGIKA UTAMA & VISUALISASI
    # ==========================================
    if input_src:
        start = True
        if input_mode == "📁 Upload File":
            start = st.button("🔍 MULAI ANALISIS", type="primary")
    
        if start and model:
            input_src.seek(0)
            with st.spinner("Memproses data visual..."):
                
                # PANGGIL FUNGSI LOGIC
                data = logic.process_analysis(model, input_src, conf, clahe, ratio)
                
                if data:
                    st.divider()
                    
                    # --- VISUALISASI GAMBAR ---
                    st.markdown("##### 🖼️ Visualisasi")
                    col_res1, col_res2 = st.columns(2)
                    with col_res1:
                        st.image(input_src, caption="Asli", use_container_width=True)
                    with col_res2:
                        st.image(data['img'], caption="Deteksi AI", use_container_width=True)
    
                    st.markdown("<br>", unsafe_allow_html=True)
    
                    # --- 4 KARTU STATISTIK (WARNA SERAGAM) ---
                    st.markdown("##### 📊 Laporan")
                    c1, c2, c3, c4 = st.columns(4)
                    
                    # Logic Warna Status
                    warna_status = "#2E7D32" # Hijau (Default/Aman)
                    
                    if data['code'] == "WARN" or data['code'] == "MEDIUM":
                         warna_status = "#F9A825" # Kuning (Waspada)
                    
                    if data['code'] == "CRITICAL":
                         warna_status = "#C62828" # Merah (Bahaya)
    
                    # Kartu 1: Kondisi
                    with c1:
                        st.markdown(f"""
                        <div class="stat-card" style="border-top: 5px solid {warna_status};">
                            <div class="stat-label">Kondisi</div>
                            <div class="stat-value" style="color:{warna_status};">{data['kondisi']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Kartu 2: Kerusakan
                    with c2:
                        st.markdown(f"""
                        <div class="stat-card" style="border-top: 5px solid {warna_status};">
                            <div class="stat-label">Kerusakan</div>
                            <div class="stat-value" style="color:{warna_status};">{data['pct']:.2f}%</div>
                        </div>
                        """, unsafe_allow_html=True)
    
                    # Kartu 3: Total Titik
                    with c3:
                        st.markdown(f"""
                        <div class="stat-card" style="border-top: 5px solid {warna_status};">
                            <div class="stat-label">Jumlah Titik</div>
                            <div class="stat-value" style="color:{warna_status};">{data['total']}</div>
                        </div>
                        """, unsafe_allow_html=True)
    
                    # Kartu 4: Rincian
                    with c4:
                        stats = data['stats']
                        st.markdown(f"""
                        <div class="stat-card" style="align-items: flex-start; border-top: 5px solid {warna_status};">
                            <div class="detail-box">
                                <div class="detail-row">
                                    <span>🔴 Besar</span> <b style="color:{warna_status}">{stats['besar']}</b>
                                </div>
                                <div class="detail-row">
                                    <span>🟡 Sedang</span> <b style="color:{warna_status}">{stats['sedang']}</b>
                                </div>
                                <div class="detail-row">
                                    <span>🟢 Kecil</span> <b style="color:{warna_status}">{stats['kecil']}</b>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)


                # --- DATA TEKNIS ---
                with st.expander("📄 Data Teknis Lengkap"):
                    st.dataframe(data['df'], use_container_width=True)
                    csv = data['df'].to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Download CSV", csv, "laporan.csv", "text/csv")

                # --- VISUALISASI PROSES COMPUTER VISION (TAB MODEL) ---
                if data['total'] > 0:
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander("🛠️ LIHAT PROSES COMPUTER VISION (DEBUG)"):
                        st.info(f"AI mendeteksi {data['total']} lubang. Klik tab di bawah untuk melihat analisis per lubang.")
                        
                        # Buat Tab sesuai jumlah lubang
                        tab_labels = [f"Lubang #{i+1}" for i in range(len(data['crops']))]
                        tabs = st.tabs(tab_labels)

                        # Isi setiap tab
                        for i, tab in enumerate(tabs):
                            with tab:
                                c_debug1, c_debug2, c_debug3 = st.columns(3)
                                
                                # Ambil data
                                crop = data['crops'][i]
                                mask = data['masks'][i]
                                info = data['raw'][i]

                                with c_debug1:
                                    st.image(crop, caption="1. Potongan Asli (RGB)", use_container_width=True)
                                with c_debug2:
                                    st.image(mask, caption="2. Segmentasi (Binary Mask)", use_container_width=True)
                                with c_debug3:
                                    st.markdown(f"""
                                    **Analisis Teknis ID-{info['ID']}:**
                                    - 📐 **Dimensi:** `{info['Dimensi']}`
                                    - 🎯 **Akurasi AI:** `{info['Confidence']}`
                                    - ⚠️ **Kategori:** `{info['Severity']}`
                                    
                                    *Proses: YOLOv8 mendeteksi lokasi -> Gaussian Blur menghaluskan aspal -> Thresholding memisahkan lubang gelap.*
                                    """)
# ==========================================
#END OF FILE
