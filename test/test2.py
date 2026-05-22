from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# Load trained model
model = YOLO("stockmarket-pattern-detection-yolov8/model.pt")

# Image path
image_path = "vcp.jpg"

# Run inference
results = model(image_path)

# Print detections
for box in results[0].boxes:
    cls_id = int(box.cls[0])
    conf = float(box.conf[0])

    print(
        f"Detected: {model.names[cls_id]} | "
        f"Confidence: {conf:.2f}"
    )

# Draw detections
annotated = results[0].plot()

# Convert color for matplotlib
annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

# Display
plt.imshow(annotated)
plt.axis("off")
plt.show()