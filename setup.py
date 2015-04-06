"""
setup
~~~~~

Setup configuration file to manage the jgrampro project

    :Copyright: (c)2015 by Pablo Vázquez Rodríguez
                <pablo.vazquez.dev@gmail.com>. See AUTHORS for details
    :License: GPLv3, see LICENSE or http://www.gnu.org/licenses/gpl-3.0.html
              for more details
    :Version: 0.1(alpha)
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='jgrampro',
    description=('Given a japanese text, returns the sentences tagged with '
                 'the grammar rules that each one complies with.'),
    author='Pablo Vázquez Rodríguez',
    author_email='',
    url='',
    license='',
    version='0.1(alpha)',
    install_requires='',
    packages=['jgrampro', 'jgrampro.tools', 'jgrampro.conf'],
    include_package_data=True,
)
