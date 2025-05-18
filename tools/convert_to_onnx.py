#!/usr/bin/env python3
"""
convert_to_onnx.py: Convert YOLOv5 .pt model to ONNX using DetectMultiBackend.

Requires: models.common.DetectMultiBackend from ultralytics/yolov5
"""

import torch
from pathlib import Path
import sys

# ---------- Paths ----------
script_dir = Path(__file__).resolve().parent              # ~/repos/driverless/tools
project_root = script_dir.parent                         # ~/repos/driverless
yolov5_dir = project_root / "src" / "driverless" / "yolov5"
pt_path = yolov5_dir / "weights" / "yolov5_models" / "best_adri.pt"
onnx_path = pt_path.with_suffix(".onnx")

# ---------- Add YOLOv5 repo to path ----------
sys.path.insert(0, str(yolov5_dir))

# ---------- Import after sys.path update ----------
from models.common import DetectMultiBackend

_real_load = torch.load
def unsafe_load(*args, **kwargs):
    kwargs["weights_only"] = False
    return _real_load(*args, **kwargs)
torch.load = unsafe_load

# ---------- Load model ----------
model = DetectMultiBackend(str(pt_path), device=torch.device("cpu"))
model.model.eval()

# ---------- Dummy input ----------
dummy_input = torch.randn(1, 3, 640, 640)  # Change if your model uses a different input size

# ---------- Export ----------
torch.onnx.export(
    model.model,
    dummy_input,
    onnx_path,
    export_params=True,
    opset_version=12,
    do_constant_folding=True,
    input_names=["images"],
    output_names=["output"],
    dynamic_axes={"images": {0: "batch"}, "output": {0: "batch"}},
)

print(f"✅ Exported to {onnx_path}")
