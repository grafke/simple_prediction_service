import logging.config

import joblib
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from app.backend.config import LOGGING, TRAINED_FEATURES, TRAINED_MODEL
from app.backend.file_storage import LocalFileStorage
from app.backend.tools import video_type_prediction

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('app')

app = FastAPI()

trained_features = joblib.load(TRAINED_FEATURES)
trained_model = joblib.load(TRAINED_MODEL)


class PredictionResponse(BaseModel):
    p_real: float
    p_fake: float


@app.post("/uploadfile/", response_model=PredictionResponse)
async def create_upload_file(file: UploadFile = File(...)):
    file_storage = LocalFileStorage(file)
    result = video_type_prediction(file_storage, trained_model, trained_features)
    return result


@app.get("/")
async def main():
    content = """
            <body>
            <form action="/uploadfile/" enctype="multipart/form-data" method="post">
            <input name="file" type="file">
            <input type="submit">
            </form>
            </body>
            """
    return HTMLResponse(content=content)
