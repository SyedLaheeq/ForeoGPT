
import cv2
from pathlib import Path
from vision.sam3_client import send_image_to_sam3

PROJECT_DIR = Path(__file__).resolve().parent.parent

CAPTURE_PATH = PROJECT_DIR / "output" / "webcam_capture.jpg"
OUTPUT_PATH = PROJECT_DIR / "output" / "webcam_segmented.jpg"


def main():
    CAPTURE_PATH.parent.mkdir(parents=True, exist_ok=True)

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError("Could not open webcam.")

    print("\nSkin-GPT Camera")
    print("-----------------------------")
    print("SPACE : Capture and analyse")
    print("ESC   : Exit")
    print("-----------------------------\n")

    captured = False

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Unable to read webcam frame.")
                break

            cv2.imshow("Skin-GPT | Camera Preview", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == 32:  # SPACE
                cv2.imwrite(str(CAPTURE_PATH), frame)
                captured = True
                print("Image captured.")
                break

            if key == 27:  # ESC
                print("Camera cancelled.")
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()

    if not captured:
        return

    print("\nUploading image to SAM3...")
    print("Processing forehead, nose and chin...")

    result_path = send_image_to_sam3(
        CAPTURE_PATH,
        OUTPUT_PATH
    )

    print("\nSegmentation successful!")
    print(f"Saved result: {result_path}")

    result = cv2.imread(str(result_path))

    if result is not None:
        cv2.imshow("Skin-GPT | Segmentation Result", result)
        print("Press any key to close.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
