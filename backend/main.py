import os
import base64
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
import uvicorn

app = FastAPI()

# CORS configuration: Allow all origins so frontend connects smoothly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini Client - Render will inject GOOGLE_API_KEY from Settings
# Ensure you have added GOOGLE_API_KEY in Render Environment variables
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

@app.post("/api/digitalize-register")
async def digitalize(file: UploadFile = File(...)):
    # 1. Read bytes from uploaded image
    image_bytes = await file.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    # 2. Call Gemini
    # Ensure you are using the correct model version
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=[
            "Extract inventory data from this PHC register photo. Return ONLY a valid JSON object matching this schema: {'entries': [{'drug_name': '', 'quantity': '', 'date': ''}], 'confidence': 'high/medium/low'}",
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
    
    return {"status": "success", "data": response.text}

if __name__ == "__main__":
    # Render uses port 10000 by default, fallback to 8000
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
