from setuptools import setup, find_packages

setup(
    name="tsm project",
    version="1.0",
    author="Nguyen Khoa Truong",
    author_email="nguyenkhoatruong231199@gmail.com",
    description="A machine learning project for regression",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TruongNguyen-23/tms-auto-plan",
    packages=find_packages(where="Src"),  
    package_dir={"": "Src"},
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "matplotlib",
        "tensorflow",
        # ... file requirements.txt
    ],
    python_requires=">=3.8",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
