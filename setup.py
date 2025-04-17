# .../setup.py

from setuptools import setup, find_packages

setup(
    name='snaptranslate',
    version='0.1.0',      # The version number of the package. Follow semantic versioning (e.g., major.minor.patch)
    author='Tousif Zaman',
    author_email='tousif47@gmail.com',
    description='A simple screen capture and translation tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown', # Specifies the format of your long description (usually 'text/markdown' for README.md)
    url='https://github.com/tousif47/SnapTranslate',
    packages=find_packages(), # Automatically finds all packages (directories with __init__.py) in project's source directory
    install_requires=[      # A list of project's dependencies. Pip will install these automatically
        'PyQt5',
        'Pillow',
        'googletrans',
        'requests',
        'httpx'
    ],
    classifiers=[          # A list of classifiers that describe the project. This helps users find it on PyPI
        'Development Status :: 3 - Alpha', # Indicates the current development stage
        'Intended Audience :: Developers', # Who is the target audience for this package?
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.13',
    ],
    entry_points={          # Defines any command-line scripts that should be created when package is installed
        'console_scripts': [
            'snaptranslate=src.main:main' # Creates a command 'snaptranslate' that runs the 'main' function in 'src/main.py'
        ],
    },
    include_package_data=True, # Tells setuptools to include any data files specified in MANIFEST.in (if you have one)
)