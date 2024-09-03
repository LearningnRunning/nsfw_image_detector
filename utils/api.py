from fastapi import File, UploadFile, Form
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
import torch

from .general import non_max_suppression, scale_boxes
from models.common import DetectMultiBackend
from .torch_utils import select_device

# 모델 로드
device = select_device('')
model = DetectMultiBackend('weights/nsfw_detector_e_rok.pt', device=device, dnn=False, data='data/coco128.yaml', fp16=False)
names = model.names
imgsz = (640, 640)

async def process_image_api(
    file: UploadFile = File(None),
    url: str = Form(None),
    conf_threshold: float = Form(0.25),
    iou_threshold: float = Form(0.45),
    label_mode: str = Form("Draw Confidence")
):
    # Check if either a file or a URL is provided
    if file is not None:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
    elif url is not None:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Ensure the request was successful
            image = Image.open(io.BytesIO(response.content))
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=400, detail=f"Error fetching image from URL: {e}")
    else:
        raise HTTPException(status_code=400, detail="No image file or URL provided")

    image_np = np.array(image)
    
    # Assuming process_image is your custom function that processes the image
    result = process_image(image_np, conf_threshold, iou_threshold, label_mode)
    
    return JSONResponse(content={"result": result.result, "annotations": result.annotations})

def process_image(image, conf_threshold, iou_threshold, label_mode):
    # 이미지 전처리
    im = torch.from_numpy(image).to(device).permute(2, 0, 1)  # HWC to CHW
    im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
    im /= 255  # 0 - 255 to 0.0 - 1.0
    if len(im.shape) == 3:
        im = im[None]  # expand for batch dim
    
    # 이미지 크기 조정
    im = torch.nn.functional.interpolate(im, size=imgsz, mode='bilinear', align_corners=False)
    
    # 추론
    pred = model(im, augment=False, visualize=False)
    if isinstance(pred, list):
        pred = pred[0]  # 첫 번째 요소 선택 (일반적으로 단일 이미지 추론의 경우)
        
    # NMS
    pred = non_max_suppression(pred, conf_threshold, iou_threshold, None, False, max_det=1000)

    # 결과 처리
    img = image.copy()
    
    harmful_label_list = []
    annotations = []
    
    for i, det in enumerate(pred):  # per image
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], img.shape).round()
            
            # Write results
            for *xyxy, conf, cls in reversed(det):
                c = int(cls)  # integer class
                if c != 6:
                    harmful_label_list.append(c)
                
                annotation = {
                    'xyxy': xyxy,
                    'conf': float(conf),
                    'cls': c,
                    'label': f"{names[c]} {conf:.2f}" if label_mode == "Draw Confidence" else f"{names[c]}"
                }
                annotations.append(annotation)
    
    result = 'nsfw' if harmful_label_list else 'nomal'
    return ProcessResponse(result=result, annotations=annotations)

class ProcessResponse:
    def __init__(self, result: int, annotations: list):
        self.result = result
        self.annotations = annotations