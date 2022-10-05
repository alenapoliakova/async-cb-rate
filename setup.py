from setuptools import setup, find_packages

with open("requirements.txt") as file:
    required = file.read().splitlines()


with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="async-cb-rate",
    version="1.0.0",
    python_requires=">=3.6",
    description="Package for async parsing CB rates",
    long_description=long_description,
    author="Alena Polyakova",
    author_email="alenapoliakova2003@gmail.com",
    packages=find_packages(),
    install_requires=required,
    include_package_data=True,
    url="https://github.com/alenapoliakova/async-cb-rate",
)
