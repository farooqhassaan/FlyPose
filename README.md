<div align="center">
<h1 align="center">🕊️ FlyPose: Towards Robust Human Pose Estimation From Aerial Views</h1>
</div>
<p align="center">
<strong>Hassaan Farooq, Marvin Brenner, Peter Stütz </strong>
</p>
<p align="center">
Universität der Bundeswehr München
</p>

<p align="center">

  <a href="https://openaccess.thecvf.com/content/WACV2026/papers/Farooq_FlyPose_Towards_Robust_Human_Pose_Estimation_From_Aerial_Views_WACV_2026_paper.pdf">
    <img src="https://img.shields.io/badge/FlyPose Paper-📜-red?labelColor=1f5e96&color=c5d6c6"
         alt="FlyPose Paper"
         height="30"
         style="position:relative; top:3px; margin-right:6px;">
  </a>

  <!-- Project Video badge -->
  <a href="https://youtu.be/ryGP033J_Mo">
    <img src="https://img.shields.io/badge/Project%20Video-%F0%9F%8E%A5-red?labelColor=b31b1b&color=c5d6c6"
         alt="Project Video"
         height="30"
         style="position:relative; top:3px; margin-right:6px;">
  </a>

  <!-- Download Dataset badge -->
  <a href="https://docs.google.com/forms/d/e/1FAIpQLSdu98Ukj6---OFhHWNGc5_PLH8L0RcikVS1voJ7vZNdORFnwg/viewform?usp=header">
    <img src="https://img.shields.io/badge/Download%20Dataset-%F0%9F%93%A6-red?labelColor=c4d82e&color=c5d6c6"
         alt="Download Dataset"
         height="30"
         style="position:relative; top:3px;">
  </a>

  <!-- GitHub Repo badge -->
  <a href="https://farooqhassaan.github.io/FlyPose/">
    <img src="https://img.shields.io/badge/Project Page-%F0%9F%92%BB-red?labelColor=2b3137&color=c5d6c6"
         alt="GitHub Repo"
         height="30"
         style="position:relative; top:3px;">
  </a>
</p>


<p align="center">
  <img src="assets/demo.gif" alt="Demo" 
       style="border: 1px solid #ddd; border-radius: 10px; padding: 6px; max-width: 90%;">
</p>

---

## 📢 News

- **March 2026** – The FlyPose weights and inference code have been released. 💻🥳
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

## 🤖 Model Code And Weights

We have released the FlyPose models together with the corresponding inference code.

Detailed instructions on how to set up the environment and run the code are provided in [`model/README.md`](model/README.md).
You can download the FlyPose model weights from the link below.

<p align="center">
  <a href="https://docs.google.com/forms/d/e/1FAIpQLSeod94pdwgIum41gbu3f7Q43nv7E2BLDq43WMYY4Fd20gYmVQ/viewform?usp=header">
    <img src="/assets/confetti_git.gif" width="550" alt="Download FlyPose Weights">
  </a>
</p>

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

If you find our work useful for your research, please use the following BibTeX entry:

```bibtex
@InProceedings{Farooq_2026_WACV,
    author    = {Farooq, Hassaan and Brenner, Marvin and St\"utz, Peter},
    title     = {FlyPose: Towards Robust Human Pose Estimation From Aerial Views},
    booktitle = {Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)},
    month     = {March},
    year      = {2026},
    pages     = {8617-8627}
}
```
