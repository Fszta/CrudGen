from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='crudgen',
    version='0.1',
    description='FastApi CRUD generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Fszta/CrudGen',
    author='Fszta',
    author_email='antoinefer@hotmail.com',
    license='GPLv3',
    packages=find_packages(),
    install_requires=['fastapi==0.62.0',
                      'uvicorn==0.13.0',
                      'SQLAlchemy==1.3.20'
                      ],
    entry_points={
        'console_scripts': [
            'crudgen = crudgen.__main__:main'
        ]
    }
)


