from pathlib import Path

import numpy as np
import onnxruntime as ort
import cv2

from visualization import draw_results


def make_session(path: str, providers):
    session_options = ort.SessionOptions()
    session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    return ort.InferenceSession(
        path,
        sess_options=session_options,
        providers=list(providers),
    )


def nms_xyxy(boxes: np.ndarray, scores: np.ndarray, iou_thr: float):
    if boxes.size == 0:
        return np.empty((0,), dtype=np.int64)

    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    areas = np.maximum(0.0, x2 - x1) * np.maximum(0.0, y2 - y1)
    order = scores.argsort()[::-1]
    keep = []

    while order.size:
        index = order[0]
        keep.append(index)
        if order.size == 1:
            break
        rest = order[1:]
        xx1 = np.maximum(x1[index], x1[rest])
        yy1 = np.maximum(y1[index], y1[rest])
        xx2 = np.minimum(x2[index], x2[rest])
        yy2 = np.minimum(y2[index], y2[rest])
        inter = np.maximum(0.0, xx2 - xx1) * np.maximum(0.0, yy2 - yy1)
        iou = inter / (areas[index] + areas[rest] - inter + 1e-6)
        order = rest[iou <= iou_thr]

    return np.array(keep, dtype=np.int64)


def preprocess_detector(frame: np.ndarray, det_size):
    det_w, det_h = det_size
    resized = cv2.resize(frame, (det_w, det_h), interpolation=cv2.INTER_LINEAR)
    tensor = resized.astype(np.float32) / 255.0
    tensor = np.transpose(tensor, (2, 0, 1))[None]
    return tensor, frame.shape[:2]


def run_detector(session, frame: np.ndarray, det_cfg):
    tensor, (orig_h, orig_w) = preprocess_detector(frame, tuple(det_cfg.input_size))
    feeds = {det_cfg.input_name: tensor}
    det_in_orig = str(det_cfg.orig_size_input_name).strip()
    if det_in_orig:
        feeds[det_in_orig] = np.array([[orig_w, orig_h]], dtype=np.int64)

    labels, boxes, scores = session.run(None, feeds)[:3]
    labels = labels[0]
    boxes = boxes[0].astype(np.float32)
    scores = scores[0].astype(np.float32)

    keep = (labels == det_cfg.person_label) & (scores >= det_cfg.conf_threshold)
    boxes = boxes[keep]
    scores = scores[keep]
    if boxes.size == 0:
        return np.empty((0, 4), dtype=np.float32)

    boxes[:, [0, 2]] = np.clip(boxes[:, [0, 2]], 0, orig_w - 1)
    boxes[:, [1, 3]] = np.clip(boxes[:, [1, 3]], 0, orig_h - 1)
    return boxes[nms_xyxy(boxes, scores, det_cfg.iou_threshold)]


def bbox_center_wh(box: np.ndarray, padding: float):
    x1, y1, x2, y2 = box.astype(np.float32)
    center = np.array([(x1 + x2) * 0.5, (y1 + y2) * 0.5], dtype=np.float32)
    wh = np.array(
        [max((x2 - x1) * padding, 1.0), max((y2 - y1) * padding, 1.0)],
        dtype=np.float32,
    )
    return center, wh


def pose_affine(center: np.ndarray, wh: np.ndarray, pose_cfg):
    input_w, input_h = tuple(pose_cfg.input_size)
    scale = min(input_w / wh[0], input_h / wh[1])
    tx = input_w * 0.5 - scale * center[0]
    ty = input_h * 0.5 - scale * center[1]
    matrix = np.array([[scale, 0.0, tx], [0.0, scale, ty]], dtype=np.float32)
    return matrix, cv2.invertAffineTransform(matrix).astype(np.float32)


def preprocess_pose_crop(frame: np.ndarray, box: np.ndarray, pose_cfg):
    input_w, input_h = tuple(pose_cfg.input_size)
    mean = np.array(pose_cfg.mean, dtype=np.float32)
    std = np.array(pose_cfg.std, dtype=np.float32)
    center, wh = bbox_center_wh(box, pose_cfg.padding)
    matrix, inv_matrix = pose_affine(center, wh, pose_cfg)
    warped = cv2.warpAffine(
        frame,
        matrix,
        (input_w, input_h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )
    tensor = warped.astype(np.float32)
    if pose_cfg.to_rgb:
        tensor = tensor[:, :, ::-1]
    tensor = (tensor - mean) / std
    tensor = np.transpose(tensor, (2, 0, 1))[None]
    return tensor, inv_matrix


def refine_peak(heatmap: np.ndarray, x: float, y: float):
    height, width = heatmap.shape
    ix, iy = int(x), int(y)
    if 1 <= ix < width - 1 and 1 <= iy < height - 1:
        x += 0.25 * np.sign(heatmap[iy, ix + 1] - heatmap[iy, ix - 1])
        y += 0.25 * np.sign(heatmap[iy + 1, ix] - heatmap[iy - 1, ix])
    return x, y


def decode_pose(heatmaps: np.ndarray, inv_matrix: np.ndarray, pose_cfg):
    input_w, input_h = tuple(pose_cfg.input_size)
    num_keypoints, hm_h, hm_w = heatmaps.shape
    scale_x = input_w / hm_w
    scale_y = input_h / hm_h
    keypoints = np.empty((num_keypoints, 2), dtype=np.float32)
    scores = np.empty((num_keypoints,), dtype=np.float32)

    for index in range(num_keypoints):
        heatmap = heatmaps[index]
        flat_index = int(heatmap.argmax())
        y = flat_index // hm_w
        x = flat_index % hm_w
        x, y = refine_peak(heatmap, float(x), float(y))
        px = x * scale_x
        py = y * scale_y
        score_x = int(np.clip(round(x), 0, hm_w - 1))
        score_y = int(np.clip(round(y), 0, hm_h - 1))
        keypoints[index, 0] = inv_matrix[0, 0] * px + inv_matrix[0, 1] * py + inv_matrix[0, 2]
        keypoints[index, 1] = inv_matrix[1, 0] * px + inv_matrix[1, 1] * py + inv_matrix[1, 2]
        scores[index] = float(heatmap[score_y, score_x])

    return keypoints, scores


def run_pose(session, frame: np.ndarray, boxes: np.ndarray, pose_cfg):
    if len(boxes) == 0:
        return []

    input_name = session.get_inputs()[0].name
    results = []

    for box in boxes:
        pose_input, inv_matrix = preprocess_pose_crop(frame, box, pose_cfg)
        heatmaps = session.run(None, {input_name: pose_input})[0]
        if heatmaps.ndim == 4:
            heatmap = heatmaps[0]
        elif heatmaps.ndim == 3:
            heatmap = heatmaps
        else:
            raise RuntimeError(f"Unexpected pose output shape: {heatmaps.shape}")
        keypoints, scores = decode_pose(heatmap.astype(np.float32), inv_matrix, pose_cfg)
        results.append({"bbox": box, "keypoints": keypoints, "scores": scores})

    return results


def run_pipeline(frame: np.ndarray, cfg):
    det_session = make_session(cfg.models.detector.onnx_path, cfg.runtime.providers)
    pose_session = make_session(cfg.models.pose.onnx_path, cfg.runtime.providers)

    boxes = run_detector(det_session, frame, cfg.models.detector)
    detections = run_pose(pose_session, frame, boxes, cfg.models.pose)
    rendered_frame = draw_results(frame.copy(), detections, cfg.visualization, cfg.models.pose.keypoint_threshold)

    return {
        "num_persons": len(detections),
        "detections": detections,
        "frame": rendered_frame,
    }


def build_output_path(input_path, cfg):
    input_path = Path(input_path)
    output_dir = Path(cfg.io.output_dir)
    output_name = f"{input_path.stem}{cfg.io.output_suffix}{input_path.suffix}"
    return output_dir / output_name
