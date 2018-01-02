from setuptools import setup
from bitfinex import __version__

# Runtime dependencies. See requirements.txt for development dependencies.
dependencies = [
    'requests',
    'httpretty'
]

version = __version__

setup(
    name='python-bitfinex',
    version=version,
    description='Python client for the Bitfinex API',
    author='Peter Matev',
    author_email='peter@matev.co.uk',
    url='https://github.com/pmatev/python-bitfinex',
    license='MIT',
    packages=['bitfinex'],
    scripts=[],
    install_requires=dependencies,
    download_url='https://github.com/pmatev/python-bitfinex/tarball/%s' % version,
    keywords=['bitcoin', 'btc', 'bitfinex'],
    classifiers=[],
    zip_safe=True
)
