import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="devappscraper",
    version="0.0.1",
    author="Matthew Auld",
    author_email="matthew@matthewauld.ca",
    description="package used to scrape development application from City of Ottawa's development search tools, and convert it into geoJSON data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matthewauld/devappscraper",
    packages=['devappscraper'],
    install_requires=[
    'bs4==0.0.1',
    'certifi==2018.8.24',
    'chardet==3.0.4',
    'Click==7.0',
    'decorator==4.3.0',
    'future==0.16.0',
    'geocoder==1.38.1',
    'idna==2.7',
    'ratelim==0.1.6',
    'requests==2.19.1',
    'six==1.11.0',
    'urllib3==1.23',
      ],

    classifiers=[],
)
