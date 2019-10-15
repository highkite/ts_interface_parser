import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ts_interface_parser",
    version="0.0.1",
    author="Thomas Osterland",
    author_email="highway.ita07@web.de",
    description="The typescript interface parser parses interfaces defined in typescript and outputs a JSON object describing the interfaces.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/highkite/ts_interface_parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
