
import os
import urllib.request

os.makedirs("models", exist_ok=True)

url = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/"
    "hand_landmarker.task"
)

output_path = "models/hand_landmarker.task"

if not os.path.exists(output_path):
    print("Mengunduh model HandLandmarker...")
    urllib.request.urlretrieve(url, output_path)
    print("Download berhasil!")
else:
    print("Model sudah tersedia.")

print("Lokasi:", os.path.abspath(output_path))
print("Ukuran:", os.path.getsize(output_path), "bytes")
