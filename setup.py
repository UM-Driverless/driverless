from setuptools import setup, find_packages

setup(
    name="dv-umotorsport",
    version="1.0.0",
    author="Rubén Jiménez Mejías",
    description="An autonomous driving software for the U-Motorsport team",
    license="Apache-2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "numpy<2", # To increase version consider using newer Yolo model
        
        # CUDA 12.1 cause torch not made for 12.6, should work with 12.6 in system
        "torch==2.2.0+cu121",
        "torchvision==0.17.0+cu121",
        "torchaudio==2.2.0+cu121",
        "transformers[torch]>=4.0.0",
        "tornado==4.5.3", # DEPENDENCY HELL
        "backports.ssl_match_hostname",
        
        "opencv-python",
        "matplotlib>=3.2.2",
        "numpy>=1.18.5",
        "Pillow>=7.1.2",
        "PyYAML>=5.3.1",
        "scipy>=1.4.1",
        "tqdm>=4.41.0",
        "tensorboard>=2.4.1",
        "pandas>=1.1.4",
        "seaborn>=0.11.0",
        "thop",
        "ipywidgets",
        "ipywebrtc",
        "openpyxl",
        "webdriver_manager",
        "pyserial",
        "msgpack-rpc-python",
        
        "python-can",
        "simple-pid",
        "cython",
        "pyopengl",
        "scikit-image",
        "psutil",
        
        # Maybe not necessary
        "gitpython",
        "ipython",
        # "thop",
        # "ipywidgets",
        # "ipywebrtc",
        # "serial",
        
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
