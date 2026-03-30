import argparse
import importlib.util
import sys
from pathlib import Path

import cv2

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from inference import build_output_path, run_pipeline

PROJECT_MODEL_DIR = Path(__file__).resolve().parents[2]


def load_config(config_path):
    config_path = Path(config_path).resolve()
    spec = importlib.util.spec_from_file_location("flypose_config", config_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load config module from {config_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "cfg"):
        raise AttributeError(f"Config file {config_path} must define `cfg`")
    return module.cfg


def parse_args():
    parser = argparse.ArgumentParser(description="Run FlyPose detector + pose ONNX inference on one image.")
    parser.add_argument(
        "--config",
        default=str(PROJECT_MODEL_DIR / "configs" / "default_config.py"),
        help="Path to EasyDict config file.",
    )
    parser.add_argument("--input", help="Optional input image override.")
    parser.add_argument("--output-dir", help="Optional output directory override.")
    parser.add_argument("--det-onnx", help="Optional detector ONNX override.")
    parser.add_argument("--pose-onnx", help="Optional pose ONNX override.")
    return parser.parse_args()


def main():
    args = parse_args()
    cfg = load_config(args.config)

    if args.input:
        cfg.io.input_path = args.input
    if args.output_dir:
        cfg.io.output_dir = args.output_dir
    if args.det_onnx:
        cfg.models.detector.onnx_path = args.det_onnx
    if args.pose_onnx:
        cfg.models.pose.onnx_path = args.pose_onnx

    if not cfg.io.input_path:
        raise ValueError("Set cfg.io.input_path in the config or pass --input.")

    frame = cv2.imread(cfg.io.input_path, cv2.IMREAD_COLOR)
    if frame is None:
        raise FileNotFoundError(f"Could not read image: {cfg.io.input_path}")

    result = run_pipeline(frame, cfg)
    output_path = build_output_path(cfg.io.input_path, cfg)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), result["frame"])
    print(f"[OK] saved {output_path} | persons={result['num_persons']}")


if __name__ == "__main__":
    main()
