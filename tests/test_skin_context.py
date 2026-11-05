
from rag.skin_context import build_skin_context

sample_profile = {
    "forehead": {
        "status": "analyzed",
        "features": {
            "brightness": 153.0,
            "redness": 0.385,
            "color_statistics": {
                "mean_r": 177.6,
                "mean_g": 142.3,
                "mean_b": 143.2
            },
            "hsv_statistics": {
                "mean_hue": 97.0,
                "mean_saturation": 56.1,
                "mean_value": 177.6
            }
        }
    },
    "left cheek": {
        "status": "missing"
    }
}

result = build_skin_context(sample_profile)

for zone, data in result["zones"].items():
    print(f"\n--- {zone} ---")
    print("Status:", data["status"])

    if data["status"] == "retrieved":
        print("Query:", data["query"])
        print("Documents retrieved:", len(data["documents"]))

        for document in data["documents"]:
            print(document[:200])