from setuptools import setup, find_packages

setup(name='pytools',
      version='0.1',
      description='Various useful python tools',
      url='https://github.com/DrGFreeman/PyTools',
      author='Julien de la Bruère-Terreault',
      author_email='drgfreeman@tuta.io',
      licence='MIT',
      packages=find_packages(exclude=('tests',)),
      python_requires='>=3.4.0',
      install_requires=['numpy', 'pytest'])
