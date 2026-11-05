from vision.sam3_client import send_image_to_sam3


result = send_image_to_sam3(
    "test_image.jpg"
)


print(result)