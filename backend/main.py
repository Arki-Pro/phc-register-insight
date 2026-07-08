from google import genai
from google.genai import types
import base64

# 1. Initialize the official new client
client = genai.Client()

# 2. Read the register image file safely
try:
    with open("register_photo.jpg", "rb") as f:
        image_bytes = f.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
except FileNotFoundError:
    print("Error: 'register_photo.jpg' file not found in this directory!")
    exit(1)

# 3. Execute the standard multimodal generation call
# Fixed: Changed 'input=' to 'contents=' and completed line 9 method
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
    # Guardrail: Forces Gemini to output pure JSON without backtick syntax errors
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
)

# 4. Print the clean output payload
print(response.text)
