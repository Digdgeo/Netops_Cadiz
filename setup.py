import os
from setuptools import setup, find_packages

# read README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

classifiers = [
	'Intended Audience :: Proximal Sensing & Remote Sensing Technicians',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Operating System :: OS Independent'
]

setup(
	name='netops_cadiz',
	version='0.1.0',
	description='Python package to retrieve spectral values for satellite bands from field Spectroradiometers data',
	long_description=long_description,
    long_description_content_type="text/markdown",
	url='https://github.com/Digdgeo/Netops_Cadiz',
	python_requires='>=3.8',
	author='Diego Garcia Diaz, Maria Dolores Raya-Sereno',
	author_email='digd.geografo@gmail.com, mdolores.raya@cchs.csic.es',
	license='MIT',
	install_requires=['numpy', 'pandas', 'matplotlib', 'scipy', 'specdal >= 0.2.1', 'openpyxl >= 3.1.4'],
	packages=find_packages(include=['netops_cadiz', 'netops_cadiz.*']),
	zip_safe=False
)
