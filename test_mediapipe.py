
import mediapipe as mp

print("MediaPipe version:", mp.__version__)

print("Has solutions:", hasattr(mp, "solutions"))
print("Has tasks:", hasattr(mp, "tasks"))

try:
    from mediapipe.tasks.python import vision
    print("HandLandmarker tersedia:",
          hasattr(vision, "HandLandmarker"))
except Exception as e:
    print("Tasks API error:", e)
