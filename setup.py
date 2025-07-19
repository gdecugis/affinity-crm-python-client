from setuptools import setup, find_packages

setup(
    name="affinity-crm-python-client",
    version="0.1.0",
    description="Unofficial Python client for the Affinity CRM v1 API",
    author="Guillaume Decugis",
    author_email="your.email@example.com",  # optional
    url="https://github.com/yourusername/affinity-crm-python-client",  # update after push
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "requests",
    ],
    extras_require={
        "dev": [
            "pytest",
            "responses",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)