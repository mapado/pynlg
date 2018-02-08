from setuptools import setup, find_packages

setup(
    name="pynlg",
    version='0.1.1',
    description='Natural Language Generation in Python',
    long_description=open('README.rst').read(),
    author="Jerry Nieuviarts",
    author_email='jerry@mapado.com',
    url='http://github.com/mapado/pynlg',
    license='MIT',
    # See list of classifiers here:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic'
    ],
    include_package_data=True,
    packages=find_packages(exclude=['test/*']),
    install_requires=['six'],
    zip_safe=False,
    keywords=['text realisation', 'pynlg', 'simplenlg'],
)
