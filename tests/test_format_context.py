
from rag.skin_context import build_skin_context
from rag.format_context import format_context_for_llm

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
            }
        }
    },
    "left cheek": {
        "status": "missing"
    }
}

context = build_skin_context(sample_profile)
prompt_context = format_context_for_llm(context)

print(prompt_context)