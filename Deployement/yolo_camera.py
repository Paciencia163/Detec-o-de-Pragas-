import cv2
from ultralytics import YOLO

# Charger le modèle YOLOv8 (exemple avec le modèle léger)
#model = YOLO("C:\Users\21624\Desktop\yolo v8\best.pt")  # Remplace par le chemin de ton propre modèle si tu en as un

model = YOLO(r"C:\Users\21624\Desktop\yolo v8\best.pt")

# Accès à la webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erreur: Impossible d'accéder à la caméra.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Faire la détection
    results = model(frame)

    # Afficher le résultat avec les annotations
    annotated_frame = results[0].plot()

    cv2.imshow("YOLOv8 - WebCam", annotated_frame)

    # Appuyer sur 'q' pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Nettoyage
cap.release()
cv2.destroyAllWindows()
