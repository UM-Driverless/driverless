# Contents <!-- omit in toc -->
- [Setup](#setup)
    - [To install latest CUDA on Ubuntu 24.04:](#to-install-latest-cuda-on-ubuntu-2404)
        - [Check this if you have problems](#check-this-if-you-have-problems)
    - [Then install the necessary packages that utilize CUDA, with matching version (12.6 should be backwards compatible up to 12.0):](#then-install-the-necessary-packages-that-utilize-cuda-with-matching-version-126-should-be-backwards-compatible-up-to-120)
    - [Install the simulator](#install-the-simulator)
    - [Use the code](#use-the-code)
- [To-Do](#to-do)
- [Notes](#notes)
- [NVIDIA JETSON XAVIER NX SETUP](#nvidia-jetson-xavier-nx-setup)
- [KVASER Setup in Ubuntu](#kvaser-setup-in-ubuntu)
- [conda](#conda)
- [Cliente para realizar la detección de conos en el simulador](#cliente-para-realizar-la-detección-de-conos-en-el-simulador)
    - [To test](#to-test)
    - [To install any driver (canlib and kvcommon must be installed first):](#to-install-any-driver-canlib-and-kvcommon-must-be-installed-first)
- [Old stuff](#old-stuff)

# Setup
[Here](https://youtu.be/wZSFr2eYE4M?si=7AaXeB594v13ZJVm) you have a tutorial in Spanish about the installation process.

First of all clone this repo
```bash
git clone https://github.com/UM-Driverless/driverless.git ~/driverless
```

We will use pyenv to install python without permission problems, a python virtual environment called .venv, within the root of the project, then use a pip editable install based on our setup.py, which will install all the requirements and allow code changes to be reflected immediately. This also helps manage the paths correctly without having to explictly add them to the PYTHONPATH.

```bash
cd ~
sudo apt-get update
sudo apt-get install -y \
  make build-essential libssl-dev zlib1g-dev libbz2-dev \
  libreadline-dev libsqlite3-dev wget curl llvm \
  libncurses5-dev xz-utils tk-dev libxml2-dev \
  libxmlsec1-dev libffi-dev liblzma-dev

# 2. Install pyenv (if not already installed):
git clone https://github.com/pyenv/pyenv.git ~/.pyenv

# 3. Set up pyenv in your shell (add these lines to your ~/.bashrc and reload):
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc

# 4. Install the desired Python version (you can have multiple versions installed)
pyenv install 3.12.3

# 5. In your project root (e.g. ~/driverless), set the local Python version:
cd ~/driverless
pyenv local 3.12.3
# This creates a .python-version file specifying Python 3.12.3 for this project.

# 6. Create a new isolated virtual environment using the local Python:
#    This ensures you're using the Python from your project rather than the pyenv shim.
python -m venv .venv
# (If that fails, try: ~/.pyenv/versions/3.12.3/bin/python -m venv .venv)

# 7. Activate your virtual environment:
source .venv/bin/activate

# 8. Verify that the virtual environment is active and using the local Python:
which python
# Expected output: ~/driverless/.venv/bin/python

# 9. Upgrade pip inside the venv:
python -m ensurepip --upgrade
python -m pip install --upgrade pip
which pip
# Expected output: ~/driverless/.venv/bin/pip

# 10. Install your project in editable mode:
pip install -e .
# If that fails, try:
# python -m pip install --isolated --force-reinstall -e .
```

## To install latest CUDA on Ubuntu 24.04:
```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
sudo apt install ./cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install cuda-toolkit
```

### Check this if you have problems
https://developer.nvidia.com/cuda-12-6-0-download-archive?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=24.04&target_type=deb_network

The previous codeblock worked for me. If you have problems, follow this. It should include everything necessary:
- Install NVIDIA drivers
- Install NVIDIA driver utils
- Install general drivers: ubuntu-drivers autoinstall
- Install CUDA with: apt install nvidia-cuda-toolkit
- (skipping steps like GDS and Mellanox here)
- Install GCC to compile c++ code and as requirement from nvidia website (see)
- Install cuDNN as a requirement for Tensorflow see cuDNN:
- wget https://developer.download.nvidia.com/compute/cudnn/9.1.1/local_installers/cudnn-local-repo-ubuntu2204-9.1.1_1.0-1_amd64.deb
- sudo dpkg -i cudnn-local-repo-ubuntu2204-9.1.1_1.0-1_amd64.deb
- sudo cp /var/cudnn-local-repo-ubuntu2204-9.1.1/cudnn-*-keyring.gpg /usr/share/keyrings/
- sudo apt-get update
- sudo apt-get -y install cudnn-cuda-12
- If these are the steps that you followed to install CUDA, tell me how you went about the Tensorflow installation.

## Then install the necessary packages that utilize CUDA, with matching version (12.6 should be backwards compatible up to 12.0):
Yolov5 model is a bit outdated, so it needs to run with PyTorch 2.5.1. You can install those with this command. It's designed for CUDA 12.1, but CUDA 12.6 is backwards compatible, so newer versions should work as well. It should just lose the newer features after CUDA 12.1:
```bash
pip install torch==2.5.1+cu121 torchvision==0.20.1+cu121 torchaudio==2.5.1+cu121 --extra-index-url https://download.pytorch.org/whl/cu121
```

## Install the simulator
Go to [https://github.com/FS-Driverless/Formula-Student-Driverless-Simulator/releases](https://github.com/FS-Driverless/Formula-Student-Driverless-Simulator/releases) and download the latest version. This is an executable file that will run the simulator. It can be stored and run from anywhere.
To connect to the Python code, clone the repo in the same folder as Deteccion_conos. [Here](https://github.com/FS-Driverless/Formula-Student-Driverless-Simulator/tree/master/python/examples) you can see Python examples.

<details>
    <summary>Test program</summary>

```python
# This code adds the fsds package to the pyhthon path.
# It assumes the fsds repo is cloned in the home directory.
# Replace fsds_lib_path with a path to wherever the python directory is located.
import sys, os
# fsds_lib_path = os.path.join(os.path.expanduser("~"), "Formula-Student-Driverless-Simulator", "python")
fsds_lib_path = os.path.join(os.getcwd(),"python")
print('CARPETA:',fsds_lib_path)
sys.path.insert(0, fsds_lib_path)

import time

import fsds

# connect to the AirSim simulator 
client = fsds.FSDSClient()

# Check network connection
client.confirmConnection()

# After enabling api controll only the api can controll the car. 
# Direct keyboard and joystick into the simulator are disabled.
# If you want to still be able to drive with the keyboard while also 
# controll the car using the api, call client.enableApiControl(False)
client.enableApiControl(True)

# Instruct the car to go full-speed forward
car_controls = fsds.CarControls()
car_controls.throttle = 1
client.setCarControls(car_controls)

time.sleep(5)

# Places the vehicle back at it's original position
client.reset()
```
</details>

To use, first run the fsds-... file, click "Run simulation", then run the python code

## Use the code
Check `~/driverless/src/driverless/config.yaml` for the configuration of the simulator.
The easiest setup is with `CAMERA_MODE: image` and `COMM_MODE: off`.
To take the image from the simulator use `CAMERA_MODE: sim`. To also control the simulator, use `COMM_MODE: sim`.

The main script that should be run is `~/driverless/src/driverless/main.py`

# To-Do
- use default logger python library
- Use sampling profiler?
- the agent should have all the conditionals and control the vehicle when in a mission. Should have the while True loop?
- rename github project from Deteccion_conos to ``um_driverless``
- check delays between simulator and processed image, response time
- knowing the pickling error, try to visualize to a thread
- TODO with open to camera and threads, simulator control? So it can close when stopped.
- SEND CAN HEARTBEAT
- MAKE ZED WORK AGAIN
- RESTORE GENERIC AGENT CLASS FOR NO SPECIFIC TEST. THEN THE TESTS INHERIT FROM IT. COMMENTED.
- PUT GLOBAL VARS AS ATTRIBUTE OF CAR OBJECT?
- Initialize trackbars of ConeProcessing. Why?
- Only import used libraries from activations with global config constants
- SET SPEED ACCORDING TO CAN PROTOCOL, and the rest of state variables (SEN BOARD)
- check edgeimpulse
- Print number of cones detected per color
- Xavier why network takes 3s to execute. How to make it use GPU?
- Make net faster. Remove cone types that we don't use? Reduce resolution of yolov5?
- Move threads to different files to make main.py shorter
- Check NVPMODEL with high power during xavier installation
- find todos and fix them
- TODO with open to camera and threads, simulator control? So it can close when stopped.
- SEND CAN HEARTBEAT
- MAKE ZED WORK AGAIN
- RESTORE GENERIC AGENT CLASS FOR NO SPECIFIC TEST. THEN THE TESTS INHERIT FROM IT. COMMENTED.
- PUT GLOBAL VARS AS ATTRIBUTE OF CAR OBJECT?
- Initialize trackbars of ConeProcessing. Why?
- Only import used libraries from activations with global config constants
- SET SPEED ACCORDING TO CAN PROTOCOL, and the rest of state variables (SEN BOARD)
- check edgeimpulse
- Print number of cones detected per color
- Xavier why network takes 3s to execute. How to make it use GPU?
- Make net faster. Remove cone types that we don't use? Reduce resolution of yolov5?
- Move threads to different files to make main.py shorter
- Check NVPMODEL with high power during xavier installation
- find todos and fix them


-------------------------------
We won't use Conda since it's not necessary, and the several python versions have caused problems. Also conda can't install all the packages we need, so there would be some packages installed with pip and others with conda. It also caused problems with docker.

- First apt installs
    ```bash
    sudo apt update && sudo apt upgrade -y #; spd-say "I finished the update"
    sudo apt install curl nano git pip python3 zstd #zstd is zed dependency
    pip install --upgrade pip; #spd-say "Finished the installs"
    ```
- Clone the GitHub directory:
    ```bash
    git clone https://github.com/UM-Driverless/Deteccion_conos.git
    ```
- Install the requirements (for yolo network and for our scripts)
    ```bash
    cd ~/Deteccion_conos
    pip install -r {requirements_file_name}.txt #yolo_requirements.txt requirements.txt
    ```
- [OPTIONAL] If you want to modify the weights, include the [weights folder](https://urjc-my.sharepoint.com/:f:/g/personal/r_jimenezm_2017_alumnos_urjc_es/EittFtAd_YFBqP0bHJOU4JQBtuxJvhdr0-u1zLMW49b1og?e=DW3dwM) in: `"yolov5/weights/yolov5_models"`

- ZED Camera Installation.
    1. Download the SDK according to desired CUDA version and system (Ubuntu, Nvidia jetson xavier jetpack, ...). If it doesn't find the matching CUDA version of the SDK, it will install it. When detected, it will continue with the installation.
        - https://www.stereolabs.com/developers/release/
        - [ZED SDK for JetPack 5.1.1 (L4T 35.3)](https://download.stereolabs.com/zedsdk/4.0/l4t35.3/jetsons) o [ZED SDK for Ubuntu 22](https://download.stereolabs.com/zedsdk/4.0/cu118/ubuntu22)
    2. Add permits:
        ```bash
        sudo chmod 777 {FILENAME}
        ```
    3. Run it without sudo (You can copy the file and Ctrl+Shift+V into the terminal. Don't know why tab doesn't complete the filename):
        ```bash
        sh {FILENAME}.run
        ```
    4. By default accept to install cuda, static version of SDK, AI module, samples and **Python API**. Diagnostic not required.
    5. Now it should be installed in the deault installation path: `/usr/local/zed`
    6. To get the Python API (Otherwise pyzed won't be installed and will throw an error):
        ```bash
        python3 /usr/local/zed/get_python_api.py
        ```
- To make sure you are using the GPU (Get IS CUDA AVAILABLE? : True)
    - Check what GPU driver you should install: https://www.nvidia.co.uk/Download/index.aspx?lang=en-uk
    - Check what GPU driver you have. X.Org -> nvidia-driver-515. In Software and Updates.
    - If errors, reinstall the driver from scratch:
        ```bash
        sudo apt-get remove --purge nvidia-* -y
        sudo apt autoremove
        sudo ubuntu-drivers autoinstall
        sudo service lightdm restart
        sudo apt install nvidia-driver-525 nvidia-dkms-525
        sudo reboot
        ```
- To check all cuda versions installed `dpkg -l | grep -i cuda`
- You can the cuda version compatible with the graphics driver using `nvidia-smi` or the built-in app in xavier o orin modules.
- To check the cuda version of the installed compiler, use `/usr/local/cuda/bin/nvcc --version`
- Now pytorch should use the same CUDA version as the ZED camera. Check this: https://www.stereolabs.com/docs/pytorch/
- You should be able to run:
    ```bash
    python3 main.py
    ```

* To explore if something fails:
    * `sudo apt-get install python3-tk`
- To install cuda manually: https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=deb_network

# Notes
- To use CAN comm with the Nvidia Jetson Orin, the can bus has to be working properly and connected when the Orin turns on. There has to be at least another device to acknowledge messages.
- For CAN to work first run setup_can0.sh
    - To run on startup, add to /etc/profile.d/
- For CAN to work first run setup_can0.sh
    - To run on startup, add to /etc/profile.d/

# NVIDIA JETSON XAVIER NX SETUP
TODO Testing with Jetpack 5.1
- Start here to install the OS: [https://developer.nvidia.com/embedded/learn/get-started-jetson-xavier-nx-devkit](https://developer.nvidia.com/embedded/learn/get-started-jetson-xavier-nx-devkit)
    - Takes about 1h.
    - Prepare SD card with >=32GB, a way to connect it to a computer (sd to usb adapter), fast internet, 
    - First download the [Jetson Xavier NX Developer Kit SD Card Image](https://developer.nvidia.com/embedded/jetpack). Older versions [here](https://developer.nvidia.com/embedded/jetpack-archive).
        - JetPack 5.1 is the latest version. JetPack 5.0.2 is the latest with docker pytorch installation available, and it's the one we've used.
        - JetPack 4.5.1 works with Pytorch 1.8 according to https://cognitivexr.at/blog/2021/03/11/installing-pytorch-and-yolov5-on-an-nvidia-jetson-xavier-nx.html
    - Then you'll be asked to install "SD Card formatter" and "Etcher"
    - Follow the tutorial for the rest
- Set power mode (up right in task bar) to max
- First apt installs
    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install curl nano git zstd #zstd is zed dependency
    ```
- Clone the GitHub directory:
    ```bash
    git clone https://github.com/UM-Driverless/Deteccion_conos.git; #spd-say "Done cloning the repository"
    ```
- To make bluetooth work [link](https://forums.developer.nvidia.com/t/bt-cant-work-after-flash-jetson-tx2-with-jetpacke4-3-no-bt-speaker-and-keyboard/112098/4):
    1. Navigate to the following file:
    $ sudo vim /lib/systemd/system/bluetooth.service.d/nv-bluetooth-service.conf
    2. Search for below line:
    ExecStart=/usr/lib/bluetooth/bluetoothd -d --noplugin=audio,a2dp,avrcp
    3. Remove all options for no plugin. It should look like below:
    ExecStart=/usr/# KVASER Setup in Ubuntu
- Follow the tutorial: https://cognitivexr.at/blog/2021/03/11/installing-pytorch-and-yolov5-on-an-nvidia-jetson-xavier-nx.html
    - Script that automatically installs everything
        ```bash
        curl https://raw.githubusercontent.com/cognitivexr/edge-node/main/scripts/setup-xavier.sh | bash
        ```
    - It will have Jetpack 4.5.1, Pytorch 1.8, TensorRT 7.1.3, Cuda 10.2
    - To solve `Illegal instruction (core dumped)`, issue with numpy and openblas:
        ```bash
        pip3 install -U "numpy==1.19.4"
        ```


- Install ZED camera drivers
    - [ZED SDK for L4T 35.1 (Jetpack 5.0)](https://download.stereolabs.com/zedsdk/3.8/l4t35.1/jetsons)
    - (https://www.stereolabs.com/developers/release/)
    - [Python API](https://www.stereolabs.com/docs/app-development/python/install/)
    - (Test Record: https://github.com/SusanaPineda/utils_zed/blob/master/capture_loop.py)
    - If shared library error:
        ```bash
        sudo apt install libturbojpeg0-dev
        ```
- Startup script (Setup all the programs on startup)
    - Add in Startup Applications: "python3 startup_script.py"
- (CAN: https://medium.com/@ramin.nabati/enabling-can-on-nvidia-jetson-xavier-developer-kit-aaaa3c4d99c9)

- To use:
    - First plug power, then the HDMI port, because otherwise it doesn't turn on
    - Don't use the upper left USB-A port for high speed (ZED camera). It's 2.0 while the others are 3.1


# KVASER Setup in Ubuntu
- Reference: https://www.kvaser.com/linux-drivers-and-sdk/
- Video: https://www.youtube.com/watch?v=Gz-lIVIU7ys
- SDK: https://www.kvaser.com/downloads-kvaser/?utm_source=software&utm_ean=7330130980754&utm_status=latest

```bash
tar -xvzf linuxcan.tar.gz
sudo apt-get install build-essential
sudo apt-get install linux-headers-`uname -r`
```
In linuxcan, and linuxcan/canlib, run:
```bash
make
sudo make install
```
In linuxcan/common, run:
```bash
make
sudo ./installscript.sh
```
To have the python API:
```bash
pip3 install canlib
```
To DEBUG:
```bash
make KV_Debug_ON=1
```

# conda
- https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html
- Create a conda environment:
    ```bash
    conda create -n formula -y
    
    # To remove it:
    # conda env remove -n formula
    ```
- Activate the environment
    ```bash
    conda activate formula
    ```
- Update the compiler
    ```bash
    conda install -c conda-forge gcc=12.1.0 # Otherwise zed library throws error: version `GLIBCXX_3.4.30' not found
    ```

# Cliente para realizar la detección de conos en el simulador

Este cliente funciona en conjunto con el simulador desarrollado en https://github.com/AlbaranezJavier/UnityTrainerPy. Para hacerlo funcionar solo será necesario seguir las instrucciones del repositorio indicado para arrancar el simulador y posteriormente ejecutar el cliente que podemos encontrar en el archivo /PyUMotorsport/main_cone_detection.py

Los pesos de la red neuronal para el main.py se encuentran en el siguiente enlace: https://drive.google.com/file/d/1H-KOYKMu6KM3g8ENCnYPSPTvb6zVnnFX/view?usp=sharing
Se debe descomprimir el archivo dentro de la carpeta: /PyUMotorsport/cone_detection/saved_models/

Los pesos de la red neuronal para el main_2.py se encuentran en el siguiente enlace: https://drive.google.com/file/d/1NFDBKxpRcfPs8PV3oftLya_M9GxW8O5h/view?usp=sharing
Se debe descomprimir el archivo dentro de la carpeta: /PyUMotorsport_v2/ObjectDetectionSegmentation/DetectionData/

## To test
Go to canlib/examples
```bash
./listChannels
./canmonitor 0
```

## To install any driver (canlib and kvcommon must be installed first):
```bash
make
sudo ./installscript.sh
```

---
# Old stuff

Crea tu entorno virtual en python 3.8 y activalo
```bash
conda create -n formula python=3.8
conda activate formula
#conda install tensorflow-gpu
```

[comment]: <> (&#40;pip install -r requeriments.txt&#41;)

A continuación vamos a installar el Model Zoo de detección de Tensorflow

Si no tienes todavía la carpeta models/research/
```bash
git clone --depth 1 https://github.com/tensorflow/models
```

Una vez dispones de la carpeta models/research/

```bash
cd models/research/
protoc object_detection/protos/*.proto --python_out=.
cp object_detection/packages/tf2/setup.py .
python -m pip install .
```

Actualizar Xavier para ejecutar YOLOv5 (06/2022)
```bash
git clone https://github.com/UM-Driverless/Deteccion_conos.git
cd Deteccion_conos
pip3 install -r yolov5/yolo_requeriments.txt
sh can_scripts/enable_CAN.sh
python3 car_actuator_testing_zed_conect_yolo.py
```

- Try to use a preconfigured JetPack 5.0.2 PyTorch Docker container, with all the dependencies and versiones solved: https://blog.roboflow.com/deploy-yolov5-to-jetson-nx/
    - Register in docker website
    - Login. If it doesn't work, reboot and try again.
        ```bash
        docker login
        ```
    - Take the tag of a container from here: https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-pytorch . For example, for JetPack 5.0.2 (L4T R35.1.0) it's `l4t-pytorch:r35.1.0-pth1.13-py3`
    - Pull container
        ```bash
        # l4t-pytorch:r35.1.0-pth1.13-py3 ->
        sudo docker pull nvcr.io/nvidia/l4t-pytorch:r35.1.0-pth1.13-py3
        ```
    - Run container
        ```bash
        # Will download about 10GB of stuff
        sudo docker run -it --rm --runtime nvidia --network host nvcr.io/nvidia/l4t-pytorch:r35.1.0-pth1.13-py3
        ```
    - TODO FINISH


(Install visual studio, pycharm, telegram, ...)
