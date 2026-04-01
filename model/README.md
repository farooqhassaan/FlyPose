# FlyPose Model and Inference Code

This directory contains the runnable inference code and local FlyPose ONNX checkpoints. 

## Code Layout

The `model/` directory is organized as follows:

```text
model/
├── checkpoints/    # Detector and pose model files
├── configs/        # runtime configuration files
├── input_examples/ # Example input images
├── outputs/        # Saved visualization results
└── src/flypose/    # Inference and visualization source code
```

## Model Checkpoints

The FlyPose model checkpoints can be downloaded ([link](../README.md)) and the `model/checkpoints/` directory is to be organized by detector and pose model variants:

```text
model/checkpoints/
├── detector/
│   └── flyposeDetector.onnx
└── pose/
    ├── flypose_s/
    │   ├── end2end.onnx
    └── flypose_h/
        ├── end2end.onnx
        ├── ...
```

The default FlyPose detector path is `model/checkpoints/detector/flyposeDetector.onnx`.  
The default FlyPose pose model path is `model/checkpoints/pose/flypose_s/end2end.onnx`.  
The FlyPose model path based on ViTPose-H is `model/checkpoints/pose/flypose_h/end2end.onnx`.

**Note:** ONNX models are provided for ease of use and straightforward testing. 
For optimized deployment on your own target hardware, they should be converted to TensorRT engines.

## Configs

Configuration files are used for paths, model parameters and runtime settings.

- `model/configs/default_config.py` provides the standard FlyPose configuration using the ViTPose-S pose model.
- `model/configs/flypose_h_config.py` switches to the larger ViTPose-H based pose model for more accurate pose estimation.

Some input samples are in `model/input_examples/` and rendered results are written to `model/outputs/`.

## Environment Setup

Clone the repository, enter the project directory, and create a conda environment with the Python dependencies from [`model/requirements.txt`](requirements.txt):

```bash
git clone https://github.com/farooqhassaan/FlyPose.git
cd FlyPose

conda create -n flypose python=3.11 pip -y
conda activate flypose
pip install -r model/requirements.txt
```

Depending on your CUDA and cuDNN installation, GPU execution may also require extending `LD_LIBRARY_PATH` so the cuDNN shared libraries are visible at runtime. For example:

```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/your/site-packages/nvidia/cudnn/lib
```

## Run Inference

```bash
python model/src/flypose/run_image_inference.py --config model/configs/default_config.py
```

### Arguments

- `--config`     : Path to the config file. Defaults to `model/configs/default_config.py`.
- `--input`      : Path to the input image.
- `--output-dir` : Directory where the rendered result should be saved.
- `--det-onnx`   : Path to the detector ONNX file.
- `--pose-onnx`  : Path to the pose ONNX file.

For example you can also provide the image path directly at runtime:

```bash
python model/src/flypose/run_image_inference.py \
  --config model/configs/default_config.py \
  --input model/input_examples/sample2.jpg
```

To run the larger pose model:

```bash
python model/src/flypose/run_image_inference.py --config model/configs/flypose_h_config.py
```
