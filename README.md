---
title: Adult Image Detector
emoji: 🚨
colorFrom: yellow
colorTo: green
sdk: gradio
sdk_version: 4.42.0
app_file: app.py
pinned: false
license: mit
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# Adult Image Detector

## Model Description

This model is a custom-trained version of YOLOv9-e, pre-trained on a custom dataset. YOLOv9 (You Only Look Once version 9) is a state-of-the-art object detection model known for its speed and accuracy.

## Model Details

- **Model Architecture:** YOLOv9-e
- **Number of Layers:** 1,119
- **Number of Parameters:** 69,366,830
- **GFLOPs:** 243.4

## Training

The model was trained for 10 epochs on a custom dataset. The training process showed consistent improvement in performance metrics.

### Training Hyperparameters

- **Initial Learning Rate (lr0):** 0.070011
- **Final Learning Rate (lr1, lr2):** 0.00208

### Training Results

| Metric | Initial Value (Epoch 0) | Final Value (Epoch 9) |
|--------|-------------------------|------------------------|
| train/box_loss | 1.8995 | 1.4264 |
| train/cls_loss | 2.644 | 1.1627 |
| train/dfl_loss | 1.9846 | 1.6321 |
| metrics/precision | 0.70196 | 0.69025 |
| metrics/recall | 0.44274 | 0.69178 |
| metrics/mAP_0.5 | 0.45088 | 0.7167 |
| metrics/mAP_0.5:0.95 | 0.27358 | 0.47964 |

## Performance

The model showed significant improvement over the course of training:

- **mAP@0.5:** Increased from 0.45088 to 0.7167
- **mAP@0.5:0.95:** Improved from 0.27358 to 0.47964
- **Precision:** Maintained around 0.69-0.70
- **Recall:** Substantially improved from 0.44274 to 0.69178

## Usage

This model can be loaded and used with YOLOv5 compatible frameworks. Here's an example of how to load the model:

```python
from ultralytics import YOLO

model = YOLO('path/to/your/model.pt')
results = model('path/to/image.jpg')
```

## Limitations and Biases

As this model was trained on a custom dataset, it may have biases or limitations specific to that dataset. Users should evaluate the model's performance on their specific use case before deployment.

## Additional Information

For more details on the YOLOv9 architecture and its capabilities, please refer to the official YOLOv9 documentation and research paper.