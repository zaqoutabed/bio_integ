from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in bio_integ/__init__.py
from bio_integ import __version__ as version

setup(
	name="bio_integ",
	version=version,
	description="bio",
	author="Riane",
	author_email="d",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
