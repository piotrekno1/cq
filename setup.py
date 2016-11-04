from setuptools import setup
import os
import os.path


def get_packages(top):
    packages = []
    for dirname, subdirs, filenames in os.walk(top):
        initpy = os.path.join(dirname, '__init__.py')
        is_python_package = os.path.isfile(initpy)
        if is_python_package:
            packages.append(dirname)
    return packages


setup(
    name='ses',
    version='0.8',
    url='https://github.com/lukaszb/ses',
    license='MIT',
    description='simple event sourcing implementation',
    author='Lukasz Balcerzak',
    author_email='lukaszbalcerzak@gmail.com',
    zip_safe=False,
    packages=get_packages('ses'),
    include_package_data=True,
    install_requires=[
        'jsonfield',
    ],
)