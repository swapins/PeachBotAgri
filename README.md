# PeachBot Agri

PeachBot Agri is an AI-driven, edge-first platform for precision agriculture. It combines sensor telemetry, computer vision, and historical meteorological data to provide field-level diagnostics, pest/disease alerts, and simple remediation guidance.

**Developer:** Swapin Vidya

This repository provides the reference implementation and integration utilities to run PeachBot Agri on small edge devices (8" touchscreen kiosks, Jetson family, Raspberry Pi) or on-prem servers.

---

**Core Features**
- Modular crop modules (`crops/`) implementing `CropModule`.
- Vision utilities in `vision/detector.py` (YOLOv8-compatible helpers, foliage density, blossom/cherry counting, pathology heuristics).
- Historical weather retrieval via `services/weather_service.py` (Visual Crossing timeline API).
- Touch-optimized local UI (`ui/`) for 8" displays.
- Export/edge helpers: `vision/export_onnx.py`, `vision/training/` templates, `docker/Dockerfile`.

---

**Important**: PeachBot Agri is a decision-support tool. It is not a substitute for professional agronomic advice. Users must comply with local laws and regulations before acting on recommendations.

## Quickstart (Development)
1. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. (Optional) Create a `.env` with API keys:

```
VISUAL_CROSSING_KEY=your_api_key_here
MODEL_PATH=vision/models/your_model.pt
```

3. Run the demo engine (uses default `coffee` crop):

```powershell
python main.py
```

4. Start the touchscreen UI (kiosk mode recommended in production):

```powershell
python ui/app.py
```

Open the device browser at `http://localhost:8080` or the IP shown in the server log.

---

## Production Deployment
Below are recommended, lightweight production options for edge or on-prem deployments.

- Docker (CPU):

```bash
docker build -t peachbotagri:latest -f docker/Dockerfile .
docker run --rm -p 8080:8080 --env-file .env peachbotagri:latest
```

- Docker (GPU): use an NVIDIA CUDA base image and a matching `torch` wheel. Replace the base image in `docker/Dockerfile` and install CUDA-enabled `torch`.

- Systemd (example) for Linux kiosk boot (adapt paths):

```ini
[Unit]
Description=PeachBot Agri UI
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/PeachBotAgri
ExecStart=/home/pi/PeachBotAgri/.venv/bin/python ui/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

- Use a WSGI server (Gunicorn/uvicorn) and a reverse proxy (nginx) for hardened deployments.

---

## Edge Optimization Tips
- Prefer `yolov8n` or quantized/ONNX models on resource-constrained hardware.
- Export to ONNX with `vision/export_onnx.py` and run with ONNX Runtime / TensorRT / OpenVINO.
- Use hardware-accelerated runtimes on Jetson (TensorRT) or Intel devices (OpenVINO).

---

## Data Handling & Privacy
- Collected imagery and telemetry may contain sensitive information. Configure local storage retention and anonymization before sharing data externally.
- If transmitting imagery to cloud services, use TLS and restrict API keys to minimal privileges.

---

## Citation & Attribution
If you use PeachBot Agri in publications or public demonstrations, please cite the project and acknowledge the developer:

Suggested citation:

```
PeachBot Agri — Swapin Vidya (2026). PeachBot Agri: an edge-first precision agriculture toolkit. https://github.com/your-username/PeachBotAgri
```

For formal publications, include this developer attribution:

```
Developer: Swapin Vidya — contact: swapin@peachbot.in — LinkedIn: https://www.linkedin.com/in/swapin-vidya
```

---

## Troubleshooting
- Missing packages: run `pip install -r requirements.txt` inside the repository venv.
- Vision model errors: ensure `MODEL_PATH` in `.env` points to a compatible YOLOv8 `.pt` and that your `torch` installation matches the platform/GPU.
- Weather API: if `VISUAL_CROSSING_KEY` is missing, the engine will run but skip weather-based analysis.

---

## Contribution & Development
- Add crops: create a new file in `crops/` implementing `CropModule` (`analyze_health(sensor_data, weather_data=None)` and `get_pest_remedy(detection)`).
- Add tests: include simple unit tests under `tests/` that simulate sensor payloads and expected outputs.
- Model training: use `vision/training/data.yaml` and the `ultralytics` training CLI (see `vision/training/README.md`).

---

## License
MIT License — see `LICENSE`.

## Contact
- Developer: Swapin Vidya
- Email: swapin@peachbot.in
- LinkedIn: https://www.linkedin.com/in/swapin-vidya

Thank you for using PeachBot Agri. 

