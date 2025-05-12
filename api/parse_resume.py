import os
import requests
import pdfplumber
from io import BytesIO

def handler(request):
    if request.method != "POST":
        return {"error": "Only POST supported"}
    
    file = request.files["file"]
    with pdfplumber.open(BytesIO(file.read())) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return {"summary": "Demo: John Doe, AI engineer with Python skills."}

    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "Summarize this resume and extract skills."},
                {"role": "user", "content": text}
            ]
        },
    )
    return {"summary": response.json()["choices"][0]["message"]["content"]}
