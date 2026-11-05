def normalize_value(value, min_val=0, max_val=255):

    if value is None:
        return None

    return round(
        (value-min_val)/(max_val-min_val),
        4
    )


def normalize_features(features):

    normalized = {}

    normalized["brightness"] = normalize_value(
        features["brightness"]
    )


    normalized["redness"] = round(
        features["redness"],
        4
    )


    rgb = features["color_statistics"]

    normalized["rgb"] = {

        "r": normalize_value(rgb["mean_r"]),
        "g": normalize_value(rgb["mean_g"]),
        "b": normalize_value(rgb["mean_b"])

    }


    hsv = features["hsv_statistics"]

    normalized["hsv"] = {

        "hue": round(
            hsv["mean_hue"]/180,
            4
        ),

        "saturation": normalize_value(
            hsv["mean_saturation"]
        ),

        "value": normalize_value(
            hsv["mean_value"]
        )

    }


    return normalized