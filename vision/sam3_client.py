import requests
import base64
import json


SAM3_URL = "https://chowder-groove-irritable.ngrok-free.dev"


def send_image_to_sam3(image_path):

    """
    Send image to Colab SAM3 server
    """

    with open(image_path, "rb") as f:

        response = requests.post(
            f"{SAM3_URL}/frame",
            files={
                "image": f
            },
            timeout=60
        )


    response.raise_for_status()

    return response.json()