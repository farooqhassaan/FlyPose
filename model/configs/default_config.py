from pathlib import Path

from easydict import EasyDict


MODEL_DIR = Path(__file__).resolve().parents[1]

cfg = EasyDict(
    io=EasyDict(
        input_path=str(MODEL_DIR / "input_examples" / "sample.jpg"),
        input_examples_dir=str(MODEL_DIR / "input_examples"),
        output_dir=str(MODEL_DIR / "outputs"),
        output_suffix="_flypose",
    ),
    models=EasyDict(
        detector=EasyDict(
            onnx_path=str(MODEL_DIR / "checkpoints" / "detector" / "flyposeDetector.onnx"),
            input_size=(1280, 1280),
            input_name="images",
            orig_size_input_name="orig_target_sizes",
            person_label=0,
            conf_threshold=0.7,
            iou_threshold=0.3,
        ),
        pose=EasyDict(
            onnx_path=str(MODEL_DIR / "checkpoints" / "pose" / "flypose_s" / "end2end.onnx"),
            input_size=(192, 256),
            padding=1.1,
            to_rgb=True,
            mean=[123.675, 116.28, 103.53],
            std=[58.395, 57.12, 57.375],
            keypoint_threshold=0.2,
        ),
    ),
    runtime=EasyDict(
        providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
    ),
    visualization=EasyDict(
        draw_bbox=True,
        skeleton=[
            (0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 6), (5, 7), (7, 9),
            (6, 8), (8, 10), (5, 11), (6, 12), (11, 12), (11, 13), (13, 15),
            (12, 14), (14, 16),
        ],
        link_colors=[
            (255, 153, 51), (255, 153, 51), (255, 153, 51), (255, 153, 51),
            (255, 153, 51), (255, 153, 51), (255, 153, 51), (0, 255, 0), (0, 255, 0),
            (0, 128, 255), (0, 128, 255), (255, 153, 51), (255, 153, 51),
            (255, 153, 51), (0, 255, 0), (0, 255, 0), (0, 128, 255), (0, 128, 255),
        ],
    ),
)
