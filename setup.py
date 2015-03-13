try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'jgram',
    description = 'Given a japanese text, returns the sentences tagged with the grammar rules that each one complies with.',
    author = 'Pablo Vázquez Rodríguez',
    author_email = '',
    url = '',
    license = '',
    version = '0.1',
    install_requires = '',
    packages = ['jgram', 'jgram.tools', 'jgram.conf'],
    include_package_data=True,
)
