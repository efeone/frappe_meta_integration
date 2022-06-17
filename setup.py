from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in frappe_meta_integration/__init__.py
from frappe_meta_integration import __version__ as version

setup(
	name="frappe_meta_integration",
	version=version,
	description="Meta Cloud API Integration for frappe framework",
	author="efeone Pvt. Ltd.",
	author_email="info@efeone.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
