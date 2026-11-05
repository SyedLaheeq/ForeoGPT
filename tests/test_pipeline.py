import numpy as np

from analysis.mvp_pipeline import run_color_analysis


# fake image (camera-like)
image = np.zeros(
    (480,640,3),
    dtype=np.uint8
)


# fake SAM3 result
zone_results = {

    "forehead":{
        "masks": np.array([])
    }

}


print("Pipeline loaded:")
print(run_color_analysis)