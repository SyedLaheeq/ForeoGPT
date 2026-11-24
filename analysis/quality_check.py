def calculate_zone_quality(features):

    brightness = features.get("brightness")

    if brightness is None:
        lighting = "unavailable"
        feature_available = False

    elif brightness < 40:
        lighting = "too_dark"
        feature_available = True

    elif brightness > 230:
        lighting = "overexposed"
        feature_available = True

    else:
        lighting = "acceptable"
        feature_available = True

    return {
        "lighting": lighting,
        "feature_available": feature_available
    }



def calculate_profile_quality(profile):

    total = len(profile)


    detected = sum(
        1
        for zone in profile.values()
        if zone["status"]=="analyzed"
    )


    return {

        "zones_detected": detected,

        "total_zones": total,

        "coverage":
            round(detected/total,2)

    }