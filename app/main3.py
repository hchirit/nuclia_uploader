from fastapi import FastAPI, UploadFile, File, Form
from nuclia import sdk
from config import settings
import tempfile
import os

app = FastAPI()

# 1. Authentification avec la KB et la clé API
sdk.NucliaAuth().kb(
    url=settings.nuclia_url,
    token=settings.nuclia_api_token
)  # :contentReference[oaicite:2]{index=2}:contentReference[oaicite:3]{index=3}

# Instanciation des helpers SDK
uploader = sdk.NucliaUpload()
searcher = sdk.NucliaSearch()

@app.post("/ask")
async def ask(
    file: UploadFile = File(...),
    prompt: str = Form(...)
):
    # 2. Sauvegarde temporaire du fichier reçu
    suffix = os.path.splitext(file.filename)[1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(await file.read())
    tmp.flush()
    tmp.close()

    try:
        # 3. Upload du fichier dans la KB active
        upload_result = uploader.file(path=tmp.name)
        # (upload_result contient notamment upload_result.rid ou resource id) :contentReference[oaicite:4]{index=4}:contentReference[oaicite:5]{index=5}

        # 4. Pose de la question sur l’ensemble des ressources de la KB
        answer = searcher.ask(query=prompt)
        # (pour plus de contrôle, on peut utiliser AskRequest pour ajouter filtres, citations, etc.) :contentReference[oaicite:6]{index=6}:contentReference[oaicite:7]{index=7}

        return {"answer": answer}
    finally:
        # Nettoyage du fichier temporaire
        os.unlink(tmp.name)
