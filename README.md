# py_verifier



python版本重构智能分析系统



## Requirements for Linux

* CUDA >= 10.2
* python >=3.7
* torch >= 1.8
* numpy == 1.17
* opencv-python >= 4.1
* tensorboard >= 1.14





```yaml
numpy>=1.17.3
torch==1.8.0
torchvision==0.9.0
torchaudio==0.8.0
pandas
matplotlib
tqdm
seaborn
```





```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```







## Thirdparty

* YOLOV4

PyTorch-YOLOV4:https://github.com/WongKinYiu/PyTorch_YOLOv4.git

pytorch-yolov4的mish-cuda依赖:https://github.com/thomasbrandon/mish-cuda.git

requirements:

```yaml
numpy == 1.17
opencv-python >= 4.1
torch==1.8.0
torchvision==0.9.0
torchaudio==0.8.0
matplotlib
pycocotools
tqdm
pillow
tensorboard >= 1.14
pyyaml
```



* Helmet

requirements:

```yaml
numpy>=1.17.3
torch==1.8.0
torchvision==0.9.0
torchaudio==0.8.0
pandas
matplotlib
tqdm
seaborn
```





* Pose 

Install :

```yaml
#Install mmpose
conda create -n env_name python=3.7
conda install conda install pytorch==1.8.0 torchvision==0.9.0 cudatoolkit=10.2 -c pytorch
pip install mmcv-full -f https://download.openmmlab.com/mmcv/dist/cu102/torch1.8.0/index.html
git clone git@github.com:open-mmlab/mmpose.git
cd mmpose
pip install -r requirements.txt
python setup.py develop
```







* Smoke Phone



