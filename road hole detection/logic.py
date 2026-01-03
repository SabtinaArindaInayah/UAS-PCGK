
import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
import os
import streamlit as st

# ==========================================
# 1. FUNGSI LOAD MODEL (CACHE DI SINI)
# ==========================================
@st.cache_resource
def load_model():
    if os.path.exists('best.pt'):
        try:
            return YOLO('best.pt'), "Model Utama (v1.0)"
        except Exception as e:
            return None, f"Error load best.pt: {e}"
    elif os.path.exists('best_backup_old.pt'):
        try:
            return YOLO('best_backup_old.pt'), "Model Backup (Legacy)"
        except Exception as e:
            return None, f"Error load backup: {e}"
    else:
        return None, "File Model Tidak Ditemukan!"

# ==========================================
# 2.IMAGE ENHANCEMENT
# ==========================================
def apply_clahe(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

# ==========================================
# 3. CORE LOGIC PROCESSING
# ==========================================
def process_analysis(model, input_file, conf_threshold, use_clahe, aspect_ratio_limit):
    file_bytes = np.asarray(bytearray(input_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    
    if image is None: return None

    # Auto-Resize
    h, w = image.shape[:2]
    max_dim = 1000
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        new_w, new_h = int(w * scale), int(h * scale)
        image = cv2.resize(image, (new_w, new_h))

    if use_clahe: image = apply_clahe(image)

    h_img, w_img = image.shape[:2]
    img_area = h_img * w_img
    
    results = model.predict(image, conf=conf_threshold)
    res_plotted = image.copy()
    
    detection_data = []
    crop_list = []
    raw_data = []
    debug_list = [] 
    filtered_boxes = []
    total_area_lubang = 0
    
    COLOR_BOX = (0, 0, 255)       
    COLOR_CONTOUR = (0, 255, 255) 
    
    kecil, sedang, besar = 0, 0, 0

    if len(results) > 0:
        result = results[0]
        
        for i, box in enumerate(result.boxes):
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            w_box = x2 - x1
            h_box = y2 - y1
            conf = box.conf[0].item()
            
            # Filter
            box_area = w_box * h_box
            if box_area > (img_area * 0.90): continue 
            ratio = w_box / h_box
            if ratio > aspect_ratio_limit or ratio < 0.10: continue 
            
            x_int, y_int = max(0, int(x1)), max(0, int(y1))
            w_int, h_int = int(w_box), int(h_box)
            
            roi = res_plotted[y_int:y_int+h_int, x_int:x_int+w_int]
            
            if roi.size > 0:
                crop_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                crop_list.append(crop_rgb)
                
                # ---PROSES OPENCV---
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                blurred_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)
                _, thresh_roi = cv2.threshold(blurred_roi, 85, 255, cv2.THRESH_BINARY_INV)
                
                # ========================================================
                mask_visual = cv2.cvtColor(thresh_roi, cv2.COLOR_GRAY2RGB)
                debug_list.append(mask_visual) # Masukkan gambar ke wadah
                # ========================================================

                contours, _ = cv2.findContours(thresh_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(roi, contours, -1, COLOR_CONTOUR, 2)
            
            cv2.rectangle(res_plotted, (int(x1), int(y1)), (int(x2), int(y2)), COLOR_BOX, 3)
            
            label_id = f"ID:{i+1}"
            cv2.putText(res_plotted, label_id, (int(x1), int(y1)-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_BOX, 2)
            
            area_px = w_box * h_box
            if area_px < 3000: kecil += 1; sev="Kecil"
            elif area_px < 11000: sedang += 1; sev="Sedang"
            else: besar += 1; sev="Besar"
            
            detection_data.append({
                "ID Lubang": i+1,
                "Posisi X": int(x1), "Posisi Y": int(y1),
                "Lebar (px)": int(w_box), "Tinggi (px)": int(h_box),
                "Akurasi AI": f"{conf:.2%}", "Tingkat Keparahan": sev
            })
            
            raw_data.append({
                "ID": i+1, "Dimensi": f"{int(w_box)} x {int(h_box)} px",
                "Confidence": f"{conf:.2%}", "Severity": sev
            })

            total_area_lubang += box_area
            filtered_boxes.append(box)

    jumlah_lubang = len(filtered_boxes)
    if img_area > 0:
        persen_kerusakan = min((total_area_lubang / img_area) * 100, 100.0)
    else:
        persen_kerusakan = 0
    
    if jumlah_lubang == 0: kondisi = "Mulus"; status_code = "SAFE"
    elif persen_kerusakan < 3.0: kondisi = "Rusak Ringan"; status_code = "WARN"
    elif persen_kerusakan < 15.0: kondisi = "Rusak Sedang"; status_code = "MEDIUM"
    else: kondisi = "Rusak Parah"; status_code = "CRITICAL"

    return {
        "img": cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB),
        "total": jumlah_lubang,
        "pct": persen_kerusakan,
        "kondisi": kondisi,
        "code": status_code,
        "df": pd.DataFrame(detection_data),
        "crops": crop_list,
        "masks": debug_list, 
        "raw": raw_data,
        "stats": {"kecil": kecil, "sedang": sedang, "besar": besar}
    }
