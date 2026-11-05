import numpy as np
import cv2


def extract_region_pixels(image, mask):
    """
    Extract RGB pixels from an image using a binary mask.

    Parameters
    ----------
    image : np.ndarray
        RGB image with shape (H, W, 3).

    mask : np.ndarray
        Binary mask with shape (H, W).

    Returns
    -------
    np.ndarray
        Pixels inside the mask with shape (N, 3).
    """

    mask = mask.astype(bool)

    pixels = image[mask]

    return pixels


def calculate_brightness(image, mask):
    """
    Calculate mean brightness within a facial region.
    """

    pixels = extract_region_pixels(
        image,
        mask
    )

    if len(pixels) == 0:
        return None

    gray = cv2.cvtColor(
        pixels.reshape(-1, 1, 3).astype(np.uint8),
        cv2.COLOR_RGB2GRAY
    )

    return float(np.mean(gray))


def calculate_redness(image, mask):
    """
    Calculate a simple image-derived redness index.

    This is an image feature, NOT a clinical diagnosis.
    """

    pixels = extract_region_pixels(
        image,
        mask
    )

    if len(pixels) == 0:
        return None

    pixels = pixels.astype(np.float32)

    r = pixels[:, 0]
    g = pixels[:, 1]
    b = pixels[:, 2]

    denominator = r + g + b + 1e-6

    redness = r / denominator

    return float(np.mean(redness))


def calculate_color_statistics(image, mask):
    """
    Calculate basic RGB statistics for a facial region.
    """

    pixels = extract_region_pixels(
        image,
        mask
    )

    if len(pixels) == 0:
        return None

    pixels = pixels.astype(np.float32)

    return {
        "mean_r": float(np.mean(pixels[:, 0])),
        "mean_g": float(np.mean(pixels[:, 1])),
        "mean_b": float(np.mean(pixels[:, 2])),
        "std_r": float(np.std(pixels[:, 0])),
        "std_g": float(np.std(pixels[:, 1])),
        "std_b": float(np.std(pixels[:, 2]))
    }


def analyze_region(image, mask):

    return {
        "brightness": calculate_brightness(
            image,
            mask
        ),

        "redness": calculate_redness(
            image,
            mask
        ),

        "color_statistics": calculate_color_statistics(
            image,
            mask
        ),

        "hsv_statistics": calculate_hsv_statistics(
            image,
            mask
        )
    }
    
def calculate_hsv_statistics(image, mask):
    pixels = extract_region_pixels(
        image,
        mask
    )

    if len(pixels) == 0:
        return None

    pixels = pixels.astype(np.uint8)

    hsv = cv2.cvtColor(
        pixels.reshape(-1, 1, 3),
        cv2.COLOR_RGB2HSV
    ).reshape(-1, 3)

    return {
        "mean_hue": float(np.mean(hsv[:, 0])),
        "mean_saturation": float(np.mean(hsv[:, 1])),
        "mean_value": float(np.mean(hsv[:, 2])),

        "std_hue": float(np.std(hsv[:, 0])),
        "std_saturation": float(np.std(hsv[:, 1])),
        "std_value": float(np.std(hsv[:, 2]))
    }
