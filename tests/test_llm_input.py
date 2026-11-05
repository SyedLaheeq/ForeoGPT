
import json

from rag.skin_context import build_skin_context
from rag.llm_input import build_llm_input


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


def test_structured_input():
    context = build_skin_context(sample_profile)
    result = build_llm_input(context)

    assert result["schema_version"] == "1.0"
    assert len(result["evidence"]) > 0

    forehead = next(
        zone for zone in result["zones"]
        if zone["zone"] == "forehead"
    )
    assert forehead["features"]["brightness"] == 153.0
    assert forehead["features"]["redness"] == 0.385

    cheek = next(
        zone for zone in result["zones"]
        if zone["zone"] == "left cheek"
    )
    assert cheek["status"] == "skipped"

    # Confirm JSON serialization works.
    json.dumps(result, allow_nan=False)

    print("Structured LLM input test passed.")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    test_structured_input()
