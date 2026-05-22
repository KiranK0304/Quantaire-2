from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# Load model
model = YOLO("stockmarket-pattern-detection-yolov8/model.pt")

# Print class names
print("\nClasses:")
print(model.names)

# Image path
image_path = "zz.png"

# Run inference
results = model(image_path, conf=0.2)

# Read image
img = cv2.imread(image_path)

if results and len(results[0].boxes) > 0:

    boxes = results[0].boxes

    # Select rightmost/latest box
    latest_box = max(
        boxes,
        key=lambda b: b.xyxy[0][2].item()
    )

    cls_id = int(latest_box.cls[0])
    conf = float(latest_box.conf[0])

    label = model.names[cls_id]

    # Box coordinates
    x1, y1, x2, y2 = map(
        int,
        latest_box.xyxy[0]
    )

    # ----------------------------
    # TERMINAL OUTPUT
    # ----------------------------

    print("\n==============================")
    print(f"Latest Pattern : {label}")
    print(f"Confidence     : {conf:.2f}")
    print(f"Top Left       : ({x1}, {y1})")
    print(f"Bottom Right   : ({x2}, {y2})")
    print(f"Width          : {x2 - x1}")
    print(f"Height         : {y2 - y1}")
    print("==============================\n")

    # ----------------------------
    # DRAW BIG RECTANGLE
    # ----------------------------

    cv2.rectangle(
        img,
        (x1, y1),
        (x2, y2),
        (255, 0, 255),
        4
    )

    # ----------------------------
    # DRAW CORNER CIRCLES
    # ----------------------------

    cv2.circle(img, (x1, y1), 8, (0, 255, 0), -1)
    cv2.circle(img, (x2, y2), 8, (0, 0, 255), -1)

    # ----------------------------
    # LABEL TEXT
    # ----------------------------

    text = f"{label} ({conf:.2f})"

    cv2.putText(
        img,
        text,
        (x1, y1 - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 0, 255),
        3
    )

    # ----------------------------
    # COORDINATE TEXT
    # ----------------------------

    coord_text_1 = f"({x1}, {y1})"
    coord_text_2 = f"({x2}, {y2})"

    cv2.putText(
        img,
        coord_text_1,
        (x1 + 10, y1 + 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.putText(
        img,
        coord_text_2,
        (x2 - 140, y2 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

else:
    print("\nNo pattern detected\n")

# Convert BGR → RGB
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Show image BIGGER
plt.figure(figsize=(16, 10))

plt.imshow(img)

plt.title(
    "YOLO Pattern Detection",
    fontsize=20
)

plt.axis("off")

plt.show()