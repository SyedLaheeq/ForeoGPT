import cv2
import requests
import numpy as np

SERVER_URL = "https://chowder-groove-irritable.ngrok-free.dev/frame"

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Could not open local webcam.")

print("Local webcam started.")
print("Press Q to quit.")

try:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame.")
            break

        # Local preprocessing
        norm_frame = cv2.convertScaleAbs(
            frame,
            alpha=1.2,
            beta=15
        )

        # Display the local frame immediately
        cv2.imshow("Skin-GPT | Local Camera", norm_frame)

        # Send frame to Colab
        success, encoded = cv2.imencode(
            ".jpg",
            norm_frame,
            [cv2.IMWRITE_JPEG_QUALITY, 80]
        )

        if success:
            try:
                response = requests.post(
                    SERVER_URL,
                    files={
                        "file": (
                            "frame.jpg",
                            encoded.tobytes(),
                            "image/jpeg"
                        )
                    },
                    timeout=2
                )

                if response.status_code == 200:
                    processed = cv2.imdecode(
                        np.frombuffer(
                            response.content,
                            dtype=np.uint8
                        ),
                        cv2.IMREAD_COLOR
                    )

                    if processed is not None:
                        cv2.imshow(
                            "Skin-GPT | Colab T4",
                            processed
                        )

                else:
                    print(
                        f"Server error: {response.status_code}"
                    )

            except requests.exceptions.RequestException as e:
                print(f"Connection error: {e}")

        # IMPORTANT: check keyboard every frame
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            print("Q pressed. Stopping camera...")
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Camera stopped.")