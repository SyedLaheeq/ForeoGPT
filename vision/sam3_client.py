# import requests
# import base64
# import json


# SAM3_URL = "https://chowder-groove-irritable.ngrok-free.dev"


# def send_image_to_sam3(image_path):

#     """
#     Send image to Colab SAM3 server
#     """

#     with open(image_path, "rb") as f:

#         response = requests.post(
#             f"{SAM3_URL}/frame",
#             files={
#                 "image": f
#             },
#             timeout=60
#         )


#     response.raise_for_status()

#     return response.json()

import requests
from pathlib import Path

SAM3_URL = "https://chowder-groove-irritable.ngrok-free.dev"

def send_image_to_sam3(image_path, output_path="output/forehead_segmented.jpg"):
    image_path = Path(image_path)
    output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with image_path.open("rb") as image_file:
        response = requests.post(
            f"{SAM3_URL}/frame",
            files={
                "file": (
                    image_path.name,
                    image_file,
                    "image/jpeg"
                )
            },
            timeout=120
        )

    response.raise_for_status()

    if "image/jpeg" not in response.headers.get("Content-Type", ""):
        raise ValueError(
            f"Expected JPEG, received: {response.headers.get('Content-Type')}"
        )

    output_path.write_bytes(response.content)

    print(f"Annotated image saved to: {output_path.resolve()}")
    return output_path
