
from rag.query_builder import build_skin_query

features = {
    "brightness": 153.0,
    "redness": 0.385,
    "color_statistics": {
        "mean_r": 177.6,
        "mean_g": 142.3,
        "mean_b": 143.2,
    },
    "hsv_statistics": {
        "mean_hue": 97.0,
        "mean_saturation": 56.1,
        "mean_value": 177.6,
    },
}

query = build_skin_query("forehead", features)

print("Generated RAG query:")
print(query)