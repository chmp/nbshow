from setuptools import setup

setup(
    name='nbshow',
    version='0.2.0',
    description='Simple read-only viewer for notebooks',
    author='Christopher Prohm',
    author_email='mail@cprohm.de',
    license='MIT',
    packages=["nbshow"],
    setup_requires=[
        'click',
        'flask',
        'nbconvert',
        'nbformat',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    entry_points='''
        [console_scripts]
        nbshow=nbshow.__main__:main
    ''',
    include_package_data=True,
)
