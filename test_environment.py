
import sys

print("=" * 45)
print("PEMERIKSAAN ENVIRONMENT")
print("=" * 45)

print("Python:", sys.version)

libraries = [
    ("NumPy", "numpy"),
    ("OpenCV", "cv2"),
    ("MediaPipe", "mediapipe"),
    ("PyTorch", "torch"),
    ("Ultralytics", "ultralytics"),
    ("Pygame", "pygame"),
]

for name, module in libraries:
    try:
        imported = __import__(module)
        version = getattr(imported, "__version__", "Version tidak tersedia")
        print(f"[OK] {name}: {version}")
    except Exception as e:
        print(f"[ERROR] {name}: {e}")

print("\n" + "=" * 45)
print("PEMERIKSAAN MEDIAPIPE")
print("=" * 45)

try:
    import mediapipe as mp
    print("MediaPipe Solutions:", hasattr(mp, "solutions"))
except Exception as e:
    print("Error:", e)

print("\n" + "=" * 45)
print("PEMERIKSAAN YOLO")
print("=" * 45)

try:
    from ultralytics import YOLO

    model = YOLO("yolov8n.pt")
    print("YOLO berhasil dimuat!")
    print("Class smartphone:", model.names[67])

except Exception as e:
    print("YOLO ERROR:", e)
