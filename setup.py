from setuptools import setup, find_packages
from setuptools.command.install import install
import os

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        os.system("python -m spacy download en_core_web_lg")
        os.system("sudo apt-get install tesseract-ocr")

setup(
    name="iris",                    
    version="0.1.0",                     
    author="Christopher Le",                  
    author_email="locvicvn1234@gmail.com",
    description="Detecting and remove PII from video with BabitMF",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chrislevn/Iris_BabitMF", 
    packages=find_packages(),            
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",             
)
