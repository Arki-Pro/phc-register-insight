from google import genai
from google.genai import types
import base64


client = genai.Client()


try:
    with open("register_photo.jpg", "rb") as f:
        image_bytes = f.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
except FileNotFoundError:
    print("Error: 'register_photo.jpg' file not found in this directory!")
    exit(1)


response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        "Extract inventory data from this PHC register photo. Return ONLY a valid JSON object matching the schema below. Do not wrap the response in markdown backticks or markdown formatting.",
        {
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": image_b64
            }
        }
    ],
    
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
)


print(response.text)
