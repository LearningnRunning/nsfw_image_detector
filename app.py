from fastapi import FastAPI, File, UploadFile, Form
from utils.api import process_image_api

app = FastAPI()

@app.post("/process_image/")
async def process_image_endpoint(
    file: UploadFile = File(...),
    conf_threshold: float = Form(0.25),
    iou_threshold: float = Form(0.45),
    label_mode: str = Form("Draw Confidence")
):
    return await process_image_api(file, conf_threshold, iou_threshold, label_mode)

# Gunicorn용 app 변수
application = app