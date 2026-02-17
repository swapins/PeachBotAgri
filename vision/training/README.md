YOLOv8 Training Template

Place your dataset under `vision/datasets/` with `train/images`, `train/labels`, `val/images`, `val/labels`.

Use the `data.yaml` in this folder as the dataset config for `ultralytics` training CLI:

```bash
# example
python -m ultralytics train data=vision/training/data.yaml model=yolov8n.pt imgsz=640 epochs=50
```

Notes:
- Labels must follow YOLO format (class x_center y_center w h) normalized.
- Start with `yolov8n.pt` (nano) for edge training; increase model size if you have more compute.
