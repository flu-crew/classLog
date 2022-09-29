from setuptools import setup

from classlog.version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="classlog",
    version=__version__,
    description="Implementation of logistic regression for classification of sequences based on a reference set",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flu-crew/classLog",
    author=["Michael Zeller", "Zebulun Arendsee"],
    author_email="mazeller@iasate.edu",
    packages=["classlog"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["classlog=classlog.ui:main"]},
    py_modules=["classlog"],
    install_requires=[
        'click',
        'rpalign',
        'scikit-learn>=0.24.1',
    ],
    zip_safe=False,
    include_package_data=True,
)
