# Project Specification: Study Distraction Detector (CV & AI)

## 1. Context & Overview
Proyek ini adalah sistem pengawasan produktivitas pribadi berbasis *Computer Vision* (CV). Sistem ini dirancang untuk mendeteksi *distraksi belajar*, khususnya saat pengguna memegang atau meletakkan smartphone di dekat buku/laptop selama jam kerja/belajar.

Sistem tidak hanya mendeteksi keberadaan (*existence*) smartphone, tetapi juga menganalisis interaksi (*active usage*) dengan mengukur *spatial overlap* antara tangan pengguna dan smartphone selama durasi tertentu.

---

## 2. Tech Stack & Algoritma Utama

### A. Core Detection: YOLOv8 / YOLOv11 (Nano Version)
* **Model:** `yolov8n.pt` atau `yolov11n.pt` (Pre-trained COCO dataset).
* **Target Classes:**
  * `cell phone` (COCO Class ID: 67)
  * `book` (COCO Class ID: 73) / `laptop` (COCO Class ID: 63)
* **Fungsi:** Deteksi *bounding box* objek di atas meja secara real-time melalui *webcam*.

### B. Interaction Detection: MediaPipe Hands
* **Framework:** Google MediaPipe Solutions (`mediapipe.solutions.hands`).
* **Fungsi:** Ekstraksi 21 *hand landmarks* ($(x, y)$ coordinates) untuk memverifikasi apakah tangan pengguna sedang memegang/menyentuh ponsel.

### C. Core Logic & Thresholds
1. **Bounding Box vs. Hand Landmark Overlap:** 
   * Hitung apakah titik ujung jari (`INDEX_FINGER_TIP`, `THUMB_TIP`) atau *bounding box* tangan bertampalan (*overlap*) dengan *bounding box* smartphone.
2. **Temporal Threshold:** 
   * Jika *overlap* terjadi secara kontinu selama **> 3 detik**, sistem akan memicu *Punishment Trigger*.
3. **Prevention of False Alarm:** Jika smartphone hanya diletakkan diam di meja tanpa tersentuh tangan, alarm/hukuman **tidak akan dipicu**.

---

## 3. Fitur Punishment & Alert Mechanism

Sistem ini dilengkapi dengan efek *punishment* (hukuman visual dan audio) saat distraksi terdeteksi melebihi batas waktu:

### A. Audio Penalty
* **Audio Player:** Menggunakan `pygame.mixer` (non-blocking thread).
* **Pilihan Sound FX:**
  * Sound effect meme / voice clip (misal: "HIDUP JOKOWI", alarm viral, atau suara teguran TTS).
  * Efek suara *jumpscare* / horror untuk *shock therapy*.

### B. Visual Overlay (Screen Penalty)
* **Red Screen Tint:** *Blending* overlay warna merah transparan ($\alpha = 0.4$) pada tampilan webcam via OpenCV `cv2.addWeighted`.
* **Warning Text:** Menampilkan pesan besar di layar (misal: `"PUNISHMENT: JAUHKAN HP!"`).
* **Optional:** Pop-up gambar meme atau *glitch effect* pada layar OpenCV.

### C. Productivity Logging (Optional Extension)
* Mengambil *snapshot/screenshot* pengguna yang sedang terdistraksi ke folder `logs/distractions/` beserta *timestamp*.
* Pencatatan total durasi distraksi harian.

---

## 4. Arsitektur Performa & Optimasi Kode

* **Threading / Multiprocessing:** Pisahkan *Frame Capture*, inferensi YOLO, dan inferensi MediaPipe untuk mencegah *bottleneck* / dropped frame pada CPU laptop.
* **Inference Frequency:** Run YOLO setiap 2-3 frame sekali jika posisi HP tidak berubah drastis untuk menghemat penggunaan resource.

---

## 5. Quick Setup & Dependencies

```bash
pip install opencv-python ultralytics mediapipe pygame numpy
```

---

## 6. Target Flowchart Logika Program

1. Read Frame dari Webcam via OpenCV.
2. Deteksi smartphone & buku menggunakan YOLO.
3. Deteksi hand landmarks menggunakan MediaPipe.
4. Cek apakah koordinat hand landmarks berada di dalam Bounding Box `cell phone`.
5. Jika **Ya**:
   * Mulai/lanjutkan timer (`start_distraction_time`).
   * Jika `elapsed_time > 3.0` detik $\rightarrow$ **Trigger Punishment (Play Audio + Red Overlay)**.
6. Jika **Tidak**:
   * Reset timer & matikan status alarm.
7. Tampilkan frame ke layar (GUI OpenCV).