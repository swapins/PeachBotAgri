"""Export a YOLO model to ONNX for edge deployment.

Usage:
    python vision/export_onnx.py path/to/model.pt path/to/output.onnx

This uses `ultralytics` model export when available.
"""
import sys
from pathlib import Path

try:
    from ultralytics import YOLO
except Exception:
    YOLO = None


def main():
    if len(sys.argv) < 3:
        print("Usage: python vision/export_onnx.py <model.pt> <out.onnx>")
        return

    model_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    if YOLO is None:
        print("ultralytics not installed; cannot export model")
        return

    if not model_path.exists():
        print(f"Model not found: {model_path}")
        return

    model = YOLO(str(model_path))
    # use built-in export helper
    model.export(format="onnx", imgsz=640, simplify=True, output=str(out_path))
    print(f"Exported ONNX to {out_path}")


if __name__ == "__main__":
    main()
