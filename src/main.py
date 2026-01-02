import cv2
import numpy as np
import base64

# ===============================
# Helper: OpenCV image -> Base64
# ===============================
def cv2_to_base64(img):
    _, buffer = cv2.imencode(".jpg", img)
    return base64.b64encode(buffer).decode("utf-8")

# ===============================
# MAIN FUNCTION
# ===============================
def analyze_road(image):
    # 1. Resize standar
    img = cv2.resize(image, (800, 600))
    h, w, _ = img.shape
    
    # 2. ROI (Hanya ambil aspal, buang langit dan motor di atas)
    roi_top = int(h * 0.45) 
    roi = img[roi_top:h, 0:w]

    # 3. Kualitas: Bilateral Filter (Menghilangkan bayangan halus tapi jaga tepi lubang)
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    smooth = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # 4. CLAHE (Mempertegas lubang di area aspal yang gelap)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    contrast = clahe.apply(smooth)

    # 5. Thresholding: Adaptive (Sangat bagus untuk lubang sedang/dangkal)
    thresh = cv2.adaptiveThreshold(contrast, 255, 
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)
    
    # 6. Morfologi: Menyambung kontur lubang yang terpecah
    kernel = np.ones((5, 5), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    # 7. Deteksi Kontur dengan Filter Kepadatan (Solidity)
    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    result_img = img.copy()
    total_area = 0
    kecil = sedang = besar = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 400: continue # Buang noise

        # Filter Rasio (Jangan deteksi marka jalan yang sangat panjang)
        x, y, bw, bh = cv2.boundingRect(cnt)
        aspect_ratio = float(bw)/bh
        if aspect_ratio < 0.2 or aspect_ratio > 4.0: continue

        # Filter Solidity: Lubang asli biasanya padat/solid
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        solidity = float(area)/hull_area if hull_area > 0 else 0
        if solidity < 0.3: continue

        total_area += area
        
        # Klasifikasi Ukuran yang lebih peka
        if area < 3000:
            kecil += 1; color = (0, 255, 0) # Hijau
        elif area < 11000:
            sedang += 1; color = (0, 255, 255) # Kuning
        else:
            besar += 1; color = (0, 0, 255) # Merah

        # Gambar kontur di gambar hasil (tambah offset ROI)
        cv2.drawContours(result_img[roi_top:h, 0:w], [cnt], -1, color, 3)

    # 8. Skor Kondisi
    roi_area_total = roi.shape[0] * roi.shape[1]
    # Faktor 2.5 agar persentase lebih realistis
    persen = min((total_area / roi_area_total) * 100 * 2.5, 100.0)
    
    if persen < 3: kondisi = "Sangat Baik"
    elif persen < 15: kondisi = "Rusak Sedang"
    else: kondisi = "Rusak Parah"

    vis_size = (400, 250)
    
    # ===============================
    # RETURN DATA UNTUK WEB
    # ===============================
    return {
        "kondisi": kondisi,
        "kerusakan": round(persen, 2),
        "lubang_kecil": kecil,
        "lubang_sedang": sedang,
        "lubang_besar": besar,
        "total_lubang": kecil + sedang + besar,
        # Gambar untuk ditampilkan di HTML (Base64)
        "roi": cv2_to_base64(cv2.resize(roi, vis_size)),
        "gray": cv2_to_base64(cv2.resize(contrast, vis_size)),
        "thresh": cv2_to_base64(cv2.resize(thresh, vis_size)),
        "morph": cv2_to_base64(cv2.resize(morph, vis_size)),
        "result": cv2_to_base64(result_img)
    }
