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
        # Kvaser CANlib SDK required manually for `canlib` module:
        # https://www.kvaser.com/downloads/
        
        "numpy==1.26.4", # Between 1.18.5 and <2.0. To increase version consider using newer Yolo model
        "transformers[torch]>=4.0.0",
        "tornado==4.5.3", # DEPENDENCY HELL. 4.5.3
        "backports.ssl_match_hostname",
        
        "opencv-python",
        "matplotlib>=3.2.2",
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
        # "python-can", # Incompatible with mspack dependency needed by the fsds simulator
        
        # was not necessary before
        # "msgpack==0.5.6", # Doesn't seem to be needed, maybe included by msgpack-rpc-python. But the version installed is 0.5.6
        "msgpack-rpc-python==0.4.1",
        
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
