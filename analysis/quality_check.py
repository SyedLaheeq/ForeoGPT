def calculate_zone_quality(features):

    brightness = features["brightness"]


    if brightness < 40:
        lighting = "too_dark"

    elif brightness > 230:
        lighting = "overexposed"

    else:
        lighting = "acceptable"


    return {

        "lighting": lighting,

        "feature_available": True

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