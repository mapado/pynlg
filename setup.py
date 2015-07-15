from setuptools import setup, find_packages

setup(
    name="pynlg",
    version='0.1',
    description='Natural Language Generation in Python',
    maintainer=["Jerry Nieuviarts"],
    author_email=['jerry@mapado.com'],
    include_package_data=True,
    packages=find_packages(),
    install_requires=['six'],
)
