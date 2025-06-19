from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

app = FastAPI()
ollama_url = "http://127.0.0.1:11434/api/generate"
model = "auryn"


# Define a Pydantic model for the request body
class ChatRequest(BaseModel):
    prompt: str


@app.post("/chat")
async def generate_response(chat_request: ChatRequest):
    data = {"model": model, "prompt": chat_request.prompt}
    try:
        # Send request to Ollama API
        response = requests.post(ollama_url, json=data, stream=True)

        # Check if the request was successful
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error from Ollama API")

        # Process streaming response
        full_response = ""
        for line in response.iter_lines():
            if line:
                # Decode each line and parse as JSON
                json_line = json.loads(line.decode('utf-8'))
                # Extract the response field (adjust based on Ollama's response format)
                if "response" in json_line:
                    full_response += json_line["response"]
                if json_line.get("done", False):
                    break

        return {"response": full_response}

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Unable to connect to Ollama server")
