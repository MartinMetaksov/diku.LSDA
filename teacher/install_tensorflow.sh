#!/bin/bash

# INSTALLATION INSTRUCTIONS
#
# You need to download the file 'cudnn-8.0-linux-x64-v5.1.tgz' manually from
# https://developer.nvidia.com/cudnn
# -> Download cuDNN v5.1 (Jan 20, 2017), for CUDA 8.0
# -> cuDNN v5.1 Library for Linux
# -> cudnn-8.0-linux-x64-v5.1.tgz 
#
# - Copy file to your server (e.g., via WinSCP)
# - Copy this script to your server
# - Log in to server via ssh
# - Execute this script via 'sh install_tensorflow.sh'

# https://www.tensorflow.org/install/install_linux

# (1) Install gcc and other tools
sudo apt-get --assume-yes install build-essential linux-headers-$(uname -r) python-pip python-dev python-virtualenv python3-pip

# (2) Install CUDA (see http://docs.nvidia.com/cuda/cuda-installation-guide-linux/#ubuntu-installation)
wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_8.0.61-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1604_8.0.61-1_amd64.deb
sudo apt-get update
sudo apt-get --assume-yes install cuda
echo "export PATH=/usr/local/cuda-8.0.61/bin${PATH:+:${PATH}}" >> ~/.bashrc
echo "export LD_LIBRARY_PATH=/usr/local/cuda-8.0.61/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}" >> ~/.bashrc
echo "export CUDA_HOME=/usr/local/cuda" >> ~/.bashrc
echo "export LC_ALL=C" >> ~/.bashrc

# (3) Install CUDNN
tar xvzf cudnn-8.0-linux-x64-v5.1.tgz
sudo cp -P cuda/include/cudnn.h /usr/local/cuda/include
sudo cp -P cuda/lib64/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
echo "export LD_LIBRARY_PATH='$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64'" >> ~/.bashrc

# (4) Install TensorFlow and Jupyter
export LC_ALL=C
sudo apt-get --assume-yes install libcupti-dev
virtualenv --system-site-packages -p python3 tensorflow_venv
. ~/tensorflow_venv/bin/activate
pip3 install --upgrade tensorflow 
pip3 install --upgrade tensorflow-gpu
pip3 install jupyter

# (5) Finally, restart machine ...
sudo shutdown -r now

