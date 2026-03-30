import cv2
import numpy as np


def draw_results(frame: np.ndarray, detections, viz_cfg, kp_thr: float):
    skeleton = viz_cfg.skeleton
    link_colors = viz_cfg.link_colors

    for person in detections:
        if getattr(viz_cfg, "draw_bbox", True):
            x1, y1, x2, y2 = np.round(person["bbox"]).astype(int)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        keypoints = person["keypoints"]
        scores = person["scores"]
        for link_index, (a, b) in enumerate(skeleton):
            if scores[a] < kp_thr or scores[b] < kp_thr:
                continue
            p1 = tuple(np.round(keypoints[a]).astype(int))
            p2 = tuple(np.round(keypoints[b]).astype(int))
            cv2.line(frame, p1, p2, tuple(link_colors[link_index]), 2, cv2.LINE_AA)

    return frame
