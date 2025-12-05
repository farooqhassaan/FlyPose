---
layout: default
title: FlyPose
---


# 🕊️ FlyPose: Towards Robust Human Pose Estimation From Aerial Views

[📦 Download Dataset](https://your-dataset-link){: .btn .btn-primary }
[🎥 Project Video](https://youtu.be/ryGP033J_Mo){: .btn }


<p align="center">
<strong>Hassaan Farooq, Marvin Brenner, Peter Stütz </strong>
</p>
<p align="center">
Universität der Bundeswehr München
</p>
<p align="center">
<a href="">
    <img src="http://img.shields.io/badge/FlyPose Paper-coming soon-B31B1B.svg"
         alt="arXiv Logo"
         height="20"
         style="position:relative; top:3px; margin-right:6px;">
</a> 
<sup>| 
<a href="https://youtu.be/ryGP033J_Mo"><strong> 🎥 Project Video</strong></a> |
  <a href="https://docs.google.com/forms/d/e/1FAIpQLSdu98Ukj6---OFhHWNGc5_PLH8L0RcikVS1voJ7vZNdORFnwg/viewform?usp=header"><strong> 📦 Download Dataset</strong></a>
  </sup>
</p>

<p align="center">
  <img src="assets/demo.gif" alt="Demo" 
       style="border: 1px solid #ddd; border-radius: 10px; padding: 6px; max-width: 90%;">
</p>

---

## 📢 News

- **Nov 2025** – Our paper has been accepted to **WACV 2026!** 🎉  
<br>

---

## 📘 Abstract

Unmanned Aerial Vehicles (UAVs) are increasingly deployed in close proximity to humans for applications such as parcel delivery, 
traffic monitoring, disaster response and infrastructure inspections. Ensuring safe and reliable operation in these human-populated
environments demands accurate perception of human poses and actions from an aerial viewpoint.  This perspective challenges existing 
methods with low resolution, steep viewing angles and (self-)occlusion, especially if the application demands realtime-feasible models. 
We train and deploy _FlyPose_, a lightweight top-down human pose estimation pipeline for aerial imagery. Through multi-dataset training, 
we achieve an average improvement of 6.8 mAP in person detection across the test-sets of Manipal-UAV, VisDrone, HIT-UAV as well as
our custom dataset. For 2D human pose estimation we report an improvement of 16.3 mAP on the challenging UAV-Human dataset. 
FlyPose runs with an inference latency of ~20 milliseconds on a Jetson Orin AGX Developer Kit and 
is deployed onboard a quadrotor UAV during flight experiments. 
We also publish _FlyPose-104_, a small but challenging aerial human pose estimation dataset, that includes manual annotations 
from difficult aerial perspectives.

---

## <img src="assets/drone.png" alt="dataset logo" height="25" style="vertical-align:middle; margin-right:3px; margin-bottom:3px;"/> FlyPose-104 Dataset

The **FlyPose-104** dataset contains human pose annotations under diverse aerial conditions. 
The dataset is available for research purposes and can be accessed via the link below.

<p align="center">
  <a href="https://docs.google.com/forms/d/e/1FAIpQLSdu98Ukj6---OFhHWNGc5_PLH8L0RcikVS1voJ7vZNdORFnwg/viewform?usp=header">
  <img src="https://img.shields.io/badge/Download-FlyPose--104-blue?style=for-the-badge&logo=google-drive" alt="Download Dataset">
  </a>
</p>

---

## 📝 Citation

If you find our work useful for your research, please cite our paper:

```bibtex
@inproceedings{flypose2026,
  title={FlyPose: Towards Robust Human Pose Estimation From Aerial Views},
  author={Hassaan Farooq, Marvin Brenner, Peter Stütz},
  booktitle={Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)},
  year={2026}
}
```

