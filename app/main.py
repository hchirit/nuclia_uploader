import base64
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import httpx
from config import settings

app = FastAPI(title="Nuclia File Uploader")


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), prompt: str = Form(...)):
    # 1. Lecture du contenu
    content = await file.read()
    # Encodage en base64 si l’API l’exige
    encoded = base64.b64encode(content).decode()

    # 2. Préparation du payload JSON selon l’OpenAPI Nuclia
    payload = {
        "filefield": {
            "uploadfile": {
                "data": encoded,
                "filename": file.filename
            }
        },
        "textfield": {
            "prompt": prompt
        }
        # Optionnel : ajouter "uuid", "kbid", etc.
    }

    headers = {
        "Authorization": f"Bearer {settings.nuclia_api_token}",
         "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(base_url=settings.nuclia_base_url) as client:
        try:
            # 3. Push des données à traiter
            resp = await client.post("/processing/push", headers=headers, json=payload)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Échec du push vers Nuclia: {e}")

        push_result = resp.json()

        # 4. (Optionnel) Récupération immédiate du résultat
        # Si tu veux directement obtenir le résultat, tu peux appeler /processing/requests
        try:
            cursor = push_result.get("cursor")
            pull_resp = await client.get("/processing/requests", headers=headers, params={"cursor": cursor})
            pull_resp.raise_for_status()
        except httpx.HTTPError as e:
            # On renvoie malgré tout le résultat du push
            return JSONResponse(status_code=200, content={"push": push_result, "warning": f"Push OK, pull KO: {e}"})

    return {"push": push_result, "result": pull_resp.json()}



