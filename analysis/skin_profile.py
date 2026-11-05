from .skin_features import analyze_region
from .normalization import normalize_features
from .quality_check import calculate_zone_quality



def build_skin_profile(zone_results, image):

    profile = {}


    for zone, results in zone_results.items():


        # No SAM mask found
        if len(results["masks"]) == 0:

            profile[zone] = {
                "status": "missing"
            }

            continue



        # Combine masks if multiple exist
        masks = results["masks"].cpu().numpy()

        combined_mask = masks.any(axis=0)



        # Extract raw pixel features
        raw_features = analyze_region(
            image,
            combined_mask
        )


        # Normalize features
        normalized_features = normalize_features(
            raw_features
        )


        # Calculate quality
        quality = calculate_zone_quality(
            raw_features
        )



        profile[zone] = {

            "status": "analyzed",

            "raw_features": raw_features,

            "normalized_features": normalized_features,

            "quality": quality

        }


    return profile