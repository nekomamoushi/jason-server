
import os
import io

from setuptools import find_packages, setup

# Needed for the following functions
HERE = os.path.abspath(os.path.dirname(__file__))


# Load the package's __init__.py module as a dictionary.
ABOUT = {}
with io.open(os.path.join(HERE, 'src/jason_server', '__init__.py')) as f:
    exec(f.read(), ABOUT)


# Get the long description from the README file
def get_long_description():
    with io.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


PACKAGE_NAME = ABOUT['__title__']
VERSION = ABOUT['__version__']
DESCRIPTION = ABOUT['__description__']
URL = ABOUT['__url__']
AUTHOR = ABOUT['__author__']
AUTHOR_EMAIL = ABOUT['__author_email__']
LICENSE = ABOUT['__license__']
PACKAGES = find_packages(where='src', exclude=['contrib', 'docs', 'tests'])
PACKAGE_DIR = {"": "src"}
INSTALL_REQUIRES = []
EXTRA_REQUIRES = []

###############################################################################

setup(
    # Name of the package
    name=PACKAGE_NAME,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=VERSION,

    description=DESCRIPTION,
    long_description=get_long_description(),
    long_description_content_type='text/markdown',

    # The project's main homepage.
    url=URL,

    # Author details
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,

    # Choose your license
    # Don't forget to the license file
    license=LICENSE,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],

    # What does your project relate to?
    keywords='packaging setuptools development',

    # Adding Non-Code Files :
    # In order for these files to be copied at install time to the package’s folder inside site-packages,
    # you’ll need to supply :
    include_package_data=True,

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=INSTALL_REQUIRES,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # See https://setuptools.readthedocs.io/en/latest/setuptools.html#automatic-script-creation
    entry_points=dict(
        console_scripts=[
            'jason-server = jason_server.cli : cli'
        ]
    )
)
