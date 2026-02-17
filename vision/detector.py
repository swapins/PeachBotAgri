import logging
from typing import List, Dict, Optional

try:
    import cv2
    import numpy as np
except Exception:
    cv2 = None
    np = None

try:
    from ultralytics import YOLO
except Exception:
    YOLO = None


log = logging.getLogger(__name__)


class AgriVision:
    def __init__(self, model_path: str = "vision/models/coffee_rust_yolo.pt"):
        self.model = None
        if YOLO is None:
            log.warning("ultralytics YOLO not available in the environment")
            return

        try:
            self.model = YOLO(model_path)
        except Exception as e:
            log.exception("Failed to load YOLO model: %s", e)
            self.model = None

    def detect_objects(self, image_path: str, conf_thresh: float = 0.3) -> List[Dict]:
        """Run model inference and return a list of detections with label, conf and box.

        Each detection is a dict: {"label": str, "conf": float, "box": [x1,y1,x2,y2]}
        """
        if self.model is None:
            return []

        detections: List[Dict] = []
        try:
            results = self.model(image_path)
            for r in results:
                boxes = getattr(r, "boxes", [])
                for box in boxes:
                    try:
                        cls_idx = int(box.cls[0]) if hasattr(box, "cls") else None
                        label = self.model.names[cls_idx] if (cls_idx is not None and hasattr(self.model, "names")) else None
                        conf = float(box.conf[0]) if hasattr(box, "conf") else 0.0
                        xyxy = None
                        if hasattr(box, "xyxy"):
                            try:
                                xy = box.xyxy[0]
                                xyxy = [float(xy[0]), float(xy[1]), float(xy[2]), float(xy[3])]
                            except Exception:
                                xyxy = None

                        if label and conf >= conf_thresh:
                            detections.append({"label": label, "conf": conf, "box": xyxy})
                    except Exception:
                        continue
        except Exception:
            return []

        return detections

    def scan_leaf(self, image_path: str) -> List[str]:
        dets = self.detect_objects(image_path, conf_thresh=0.5)
        if not dets:
            return ["Healthy"]
        labels = [d["label"] for d in dets]
        return list(set(labels)) if labels else ["Healthy"]

    def foliage_density(self, image_path: str, roi: Optional[List[int]] = None) -> Optional[float]:
        """Estimate foliage density as fraction of green pixels in the image or ROI.

        Returns a float in [0..1] or None if OpenCV/NumPy are unavailable.
        """
        if cv2 is None or np is None:
            log.warning("cv2/numpy not available - cannot compute foliage density")
            return None

        img = cv2.imread(image_path)
        if img is None:
            return None

        if roi and len(roi) == 4:
            x1, y1, x2, y2 = roi
            img = img[y1:y2, x1:x2]

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Broad green range in HSV; may need tuning per crop/lighting
        lower_green = np.array([25, 30, 20])
        upper_green = np.array([100, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)

        green_pixels = int(np.count_nonzero(mask))
        total_pixels = mask.size
        density = green_pixels / total_pixels if total_pixels > 0 else 0.0
        return float(density)

    def count_targets(self, image_path: str, target_labels: List[str] = None, conf_thresh: float = 0.3) -> Dict[str, int]:
        """Count occurrences of target labels (e.g., blossoms, cherries) in the image.

        Matching is case-insensitive and based on substring matching of labels provided by the model.
        """
        if target_labels is None:
            target_labels = ["blossom", "cherry", "flower"]

        dets = self.detect_objects(image_path, conf_thresh=conf_thresh)
        counts: Dict[str, int] = {t: 0 for t in target_labels}
        for d in dets:
            lbl = d.get("label", "").lower()
            for t in target_labels:
                if t.lower() in lbl or lbl in t.lower():
                    counts[t] += 1

        return counts

    def detect_pathology(self, image_path: str, conf_thresh: float = 0.3) -> List[str]:
        """Return disease/pathology labels found in the image (if model supports it)."""
        dets = self.detect_objects(image_path, conf_thresh=conf_thresh)
        disease_labels = []
        for d in dets:
            lbl = d.get("label", "")
            # simple heuristic: many models label diseases with words like 'rust', 'mildew', 'blotch'
            if any(x in lbl.lower() for x in ["rust", "mildew", "blotch", "spot", "blight"]):
                disease_labels.append(lbl)
        return list(set(disease_labels))


# Simple test for the vision script
if __name__ == "__main__":
    det = AgriVision()
    found = det.scan_leaf("data/sample_coffee_leaf.jpg")
    density = det.foliage_density("data/sample_coffee_leaf.jpg")
    counts = det.count_targets("data/sample_coffee_leaf.jpg")
    pathos = det.detect_pathology("data/sample_coffee_leaf.jpg")
    print(f"Vision System Detected: {found}")
    print(f"Foliage density: {density}")
    print(f"Counts: {counts}")
    print(f"Pathologies: {pathos}")
