#!/usr/bin/python3
'''
Setup
'''
from setuptools import setup, find_packages

setup(
    name="Router-Exploit-Shovel",
    version="1.0",
    urls="https://github.com/arthastang/Router-Exploit-Shovel",
    author="MarvelTeam",
    description="Automated Application Generation for Stack Overflow Types on Wireless Routers",
    packages=find_packages(),
    scripts=["Router_Exploit_Shovel.py"],
    url=['https://github.com/yaml','https://github.com/lxml/lxml'],
    install_requires=["optparse","pyyaml"],
    python_requires=">=3.5"

)