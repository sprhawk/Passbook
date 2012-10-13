from distutils.core import setup

setup(
    name = "ypassbook",
    packages = ["ypassbook"],
    version = "0.1.0",
    description = "Create an Apple passbook",
    author = "Yang Hongbo",
    author_email = "hongbo@yang.me",
    url = "http://pypi.python.org/pypi/ypassbook",
    
    keywords = ["apple", "passbook", "ios"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: 4 - Beta", 
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Utilities"
        ],
long_description = """\
ypassbook - An Apple Passbook pass generator
--------------------------------------------

"""
    )
