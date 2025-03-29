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
        # Core
        "opencv-python",
        "matplotlib>=3.2.2",
        "numpy>=1.18.5",
        "Pillow>=7.1.2",
        "PyYAML>=5.3.1",
        "requests>=2.23.0",
        "scipy>=1.4.1",
        "torch>=2.0.0+nv23.05",
        "torchvision>=0.15.1",
        "tqdm>=4.41.0",
        "tensorboard>=2.4.1",
        "pandas>=1.1.4",
        "seaborn>=0.11.0",
        "thop",
        "ipywidgets",
        "ipywebrtc",

        # Your project-specific
        "python-can",
        "simple-pid",
        "cython",
        "pyopengl",
        "tornado",
        "scikit-image",
        "psutil",
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
