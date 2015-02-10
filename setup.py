from setuptools import setup, find_packages

setup(
    name='django-sphinx-that',
    version='0.0.1',
    description='sphinxit integration django',
    long_description=open('README.md').read(),
    author='Alexey Gromov',
    author_email='alxgrmv@gmail.com',
    packages=find_packages(),
    install_requires=["Django >= 1.4"],
)
