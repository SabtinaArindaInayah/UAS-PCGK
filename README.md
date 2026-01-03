# 🛣️ Aplikasi Deteksi Jalan Berlubang  
**Ujian Akhir Semester – Pengolahan Citra Digital**

Aplikasi ini merupakan proyek UAS mata kuliah **Pengolahan Citra Digital (PCGK)** yang bertujuan untuk mendeteksi dan menganalisis kondisi jalan berlubang.

---

## 🎯 Tujuan Proyek

* **Mendeteksi** keberadaan lubang pada permukaan jalan secara otomatis dari citra digital.
* **Menghitung** tingkat kerusakan jalan berdasarkan persentase luas area lubang terhadap jalan.
* **Mengklasifikasikan** kondisi jalan menjadi:
    * 🟢 **Sangat Baik / Aman** (< 3% kerusakan)
    * 🟡 **Rusak Sedang / Waspada** (3-15% kerusakan)
    * 🔴 **Rusak Parah / Kritis** (> 15% kerusakan)
* **Menampilkan** hasil analisis secara visual, informatif, dan *real-time* melalui antarmuka web modern.

---

## 🧠 Metode Pengolahan Citra (Hybrid Pipeline)

Aplikasi ini menerapkan tahapan pengolahan citra digital yang telah dimodernisasi:

1.  **Auto-Resize** – Standarisasi ukuran citra (Max dimensi 1000px) untuk performa optimal.
2.  **CLAHE (Preprocessing)** – Meningkatkan kontras area gelap agar tekstur aspal lebih jelas.
3.  **YOLOv8 Inference (AI)** – Mendeteksi *Region of Interest (ROI)* atau lokasi keberadaan lubang.
4.  **Gaussian Blur** – Menghilangkan *noise* (bintik halus/kerikil) pada area aspal.
5.  **Inverse Thresholding** – Segmentasi memisahkan lubang (gelap) dari aspal (terang).
6.  **Deteksi Kontur** – Menggambar garis tepi lubang secara presisi.
7.  **Aspect Ratio Filter** – Mengeliminasi deteksi palsu (bukan lubang) berdasarkan rasio dimensi.
8.  **Scoring Kondisi** – Perhitungan statistik total untuk penentuan status jalan.

---

## 🖥️ Fitur Aplikasi

✨ **Modern & Responsive UI**
* Upload citra jalan dengan drag-and-drop atau input Kamera langsung.
* Desain **"Safety Theme"** (Black & Yellow) yang profesional sesuai standar industri.
* Antarmuka *user-friendly* berbasis Streamlit.

📊 **Analisis Komprehensif**
* Status kondisi jalan (Aman/Waspada/Bahaya).
* Persentase kerusakan presisi hingga dua desimal.
* Statistik jumlah lubang per kategori (Kecil/Sedang/Besar).

🔬 **Visualisasi Proses (Debugging)**
* Melihat proses di balik layar ("Dapur" Computer Vision).
* Visualisasi layer: *Crop RGB*, *Binary Mask*, dan *Contour Detection*.

📥 **Export Data**
* Unduh hasil analisis dalam format CSV untuk pelaporan.

---

## ⚡ Tech Stack

* **Backend & Frontend:** Python (Streamlit)
* **Deep Learning:** Ultralytics YOLOv8 (Custom Trained)
* **Image Processing:** OpenCV, NumPy
* **Data Handling:** Pandas

---

## 💡 Tips Penggunaan

* Gunakan gambar jalan yang jelas untuk hasil terbaik.
* Pastikan pencahayaan cukup; bayangan pohon yang terlalu gelap dapat mempengaruhi akurasi pengukuran area.
* Foto tegak lurus ke permukaan jalan memberikan hasil perhitungan dimensi yang lebih akurat.
* Gunakan resolusi minimal 640x480 pixel.

---

## 👥 Tim Pengembang (Kelompok 3)

Proyek ini dikerjakan oleh 12 anggota dengan pembagian tugas spesifik pada modul *Deep Learning*, *Computer Vision Logic*, *Frontend Interface*, dan *Data Reporting*.

1. Andre Saputra
2. Khairunnisa Labibah
3. Sabtina Arinda Inayah
4. Adzka Dzikri imanullah
5. M. Farid Febriansyah
6. Primanda Suryawan
7. Andhika Pratama
8. Hafizh 'Abid Khalish
9. Dewi Siti Jamilah
10. Faiz Lintang Prawira
11. Sunan Maulana
12. Rifki Destrizal Nugraha
