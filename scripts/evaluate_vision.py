"""Small evaluation helper to run the vision utilities against sample images.

Usage:
    python scripts/evaluate_vision.py data/sample_image.jpg

This script will print detections, foliage density, counts for blossoms/cherries and detected pathologies.
"""
import sys
from pathlib import Path
from vision.detector import AgriVision


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/evaluate_vision.py <image_path>")
        return

    img = sys.argv[1]
    p = Path(img)
    if not p.exists():
        print(f"Image not found: {img}")
        return

    det = AgriVision()
    objects = det.detect_objects(img)
    labels = det.scan_leaf(img)
    density = det.foliage_density(img)
    counts = det.count_targets(img, target_labels=["blossom", "cherry"]) 
    pathos = det.detect_pathology(img)

    print("Detections:")
    for d in objects:
        print(f" - {d.get('label')} (conf={d.get('conf'):.2f}) box={d.get('box')}")

    print(f"Unique labels: {labels}")
    print(f"Foliage density: {density}")
    print(f"Counts: {counts}")
    print(f"Pathologies: {pathos}")


if __name__ == "__main__":
    main()
