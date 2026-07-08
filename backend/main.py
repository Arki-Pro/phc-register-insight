import base64
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types

# Initialize App & Gemini Client
app = FastAPI()
client = genai.Client()

# CORS for Frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/digitalize-register")
async def digitalize(file: UploadFile = File(...)):
    # Read file content from the upload
    image_bytes = await file.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    # Gemini API Call
    response = client.models.generate_content(
        model="gemini-2.5-flash",
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
    
    # Return the text response directly
    return {"status": "success", "data": response.text}

if __name__ == "__main__":
    import uvicorn
    # Host 0.0.0.0 is required for Codespaces port forwarding
    uvicorn.run(app, host="0.0.0.0", port=8000)
