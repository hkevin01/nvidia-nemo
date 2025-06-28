from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="nvidia-nemo-guardrails",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive implementation of Nvidia NeMo Guardrails for AI safety",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nvidia-nemo-guardrails",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.3.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.2.0",
            "mkdocstrings>=0.22.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "nemo-guardrails-cli=nemo_guardrails.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "nemo_guardrails": ["*.yaml", "*.yml", "*.json"],
    },
) 