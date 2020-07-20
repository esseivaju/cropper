from setuptools import setup, find_packages

setup(
    name="photoworkshop_cropper",
    author="Julien Esseiva",
    description="Find a filename in image files in the input directory and rename each image file with the filename found",
    version="0.1",
    packages=find_packages(),
    scripts=["bin/photoworkshop_cropper"],
    install_requires=[
        "opencv-python>=4.3.0"
    ]
)