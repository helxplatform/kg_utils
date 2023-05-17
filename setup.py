"""Setup reasoner-transpiler package."""
from setuptools import setup

setup(
    name="kg-utils",
    version="0.0.1",
    author="Evan Morris",
    author_email="",
    url="https://github.com/helxplatform/kg_utils",
    description="Merge KGX json objects",
    packages=["kg_utils"],
    install_requires=[
        "orjson==3.8.10",
        "xxhash==3.2.0",
        "jsonlines==3.1.0"
    ],
    zip_safe=False,
    license="MIT",
    python_requires=">=3.6",
)
