import requests
import json


API_KEY = "ba76807d1b7242e6af2e6747c40741ca"


url = "https://toscrape.com"

if __name__ == "__main__":
    print("🚀 Starting Zyte demo")


payload = {

    "url": url,

    "browserHtml": True,

    "screenshot": True

}


print("🚀 Sending request to Zyte API...")


response = requests.post(

    "https://api.zyte.com/v1/extract",

    auth=(API_KEY, ""),

    json=payload

)


if response.status_code == 200:

    data = response.json()


    print("\n✅ Zyte request successful")


    print("\nHTML preview:")
    print(
        data["browserHtml"][:500]
    )


    if "screenshot" in data:

        print(
            "\n✅ Screenshot successfully received"
        )


else:

    print(
        "Error:",
        response.status_code
    )