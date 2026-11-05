from .skin_profile import build_skin_profile
from .quality_check import calculate_profile_quality



def run_color_analysis(image, zone_results):


    profile = build_skin_profile(
        zone_results,
        image
    )


    quality = calculate_profile_quality(
        profile
    )


    return {

        "status": "success",

        "analysis_type": "skin_profile",

        "zones": profile,

        "quality": quality

    }