from pathlib import Path
from setuptools import find_packages, setup

this_dir = Path(__file__).parent
long_description = ""
try:
    long_description = (this_dir / "README.md").read_text(encoding="utf-8")
except Exception:
    long_description = "Plot VRP routes"

setup(
    name='vrplot',
    packages=find_packages(),
    version='0.1.0',
    description='Plot VRP routes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Breno A. Beirigo',
    license='MIT',
    install_requires=['numpy', 'matplotlib'],
    extras_require={'mip': ['gurobipy']},
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)