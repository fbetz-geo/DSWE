rom setuptools import setup
import os
import ee

ee.Initialize()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

exec(read('cloudDSWE/__version__.py'))

setup(
    name = 'cloudDSWE',
    version = __version__,
    packages = ['cloudDSWE',],
    license = 'MIT',
    long_description = read('README.md'),
    long_description_content_type='text/markdown',
    install_requires = [
        'earthengine_api',
        'httplib2shim'
        ],
    author = 'Florian Betz',
    author_email = 'fbetz.geo@gmail.com',
    url = 'https://github.com/fbetz-geo/DSWE'
)