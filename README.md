# AI-Audio-Stem-Separation

A personal project where I deployed a pretrained hybrid U-net model for music source separation by Meta. 

Music stem separation is a machine learning process of isolating instruments or "stems" from an original audio mix. The purpose of this project was to develop an online deployment of a model for music stem separation in a cost-effective manner. The solution for this was to identify a lightweight pretrained model and deploy it to a distributed network of GCP cloud run instances to achieve "pay per compute" deployment while still maintaining good latency. 

Information on the model deployed (used Hdemucs v3): https://github.com/facebookresearch/demucs

Deployment link: https://autoboom-430119.uc.r.appspot.com/

Video Presentation: https://youtu.be/zVlwmV_lMZM
