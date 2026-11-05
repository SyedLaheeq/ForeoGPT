
from rag.skin_context import build_skin_context
from rag.llm_input import build_llm_input
from rag.gemini_client import generate_with_gemini


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


def test_gemini_connection():
    context = build_skin_context(sample_profile)
    llm_input = build_llm_input(context)

    result = generate_with_gemini(llm_input)

    assert result["mode"] == "gemini"
    assert isinstance(result["zone_results"], list)

    print("Gemini API call succeeded.")
    print(result)


if __name__ == "__main__":
    test_gemini_connection()
