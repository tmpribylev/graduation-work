from setuptools import setup, find_packages

install_requires = [
    'thespian==3.10.5',
    'python-dotenv==0.19.2',
    'psycopg2==2.9.2',

    'anyio==3.4.0',
    'fastapi==0.70.1' ,
    'idna==3.3',
    'sniffio==1.2.0',
    'starlette==0.16.0'

]

setup(
    name='first Actor',
    version='0.0.0',
    description='Actor prototype',
    packages=find_packages(),
    install_requires=install_requires
)