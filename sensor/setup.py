from setuptools import setup, find_packages

#https://docs.python-guide.org/writing/structure/

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='BME680 air quality',
    version='0.1.0',
    description='Application to calculate indoor air quality data using Adafruite BME680.',
    long_description=readme,
    author='Nuno Cruz',
    url='https://github.com/nunocruz/home_air_quality',
    license=license,
    packages=find_packages(exclude=('tests'))
)