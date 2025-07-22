from setuptools import setup, find_packages

setup(
    name="affinity-crm-python-client",
    version="0.1.0",
    description="Unofficial Python client for the Affinity CRM v1 API",
    author="Guillaume Decugis",
    url="https://github.com/gdecugis/affinity-crm-python-client",  
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
        "pydantic[email]>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "responses>=0.13.0",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)