import os
from setuptools import setup, find_packages

cur_dir = os.path.realpath(os.path.dirname(__file__))

setup(
    name='syncheck',
    packages=find_packages(),
    version='0.0.1',
    author='Synthesis Project Team',
    author_email='olgakononova@lbl.gov',
    description='Synthesis Check Project (GENESIS-Ceder Group)',
    zip_safe=False,
    install_requires=open(os.path.join(cur_dir, './requirements.txt')).readlines(),
    include_package_data=True
)
