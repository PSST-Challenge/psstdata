import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name='psstdata',
    version='0.0.0a5',
    author='Portland Allied Labs for Aphasia Technology (PALAT)',
    author_email='galer@ohsu.edu',
    packages=[
        'psstdata'
    ],
    url='https://github.com/PSST-Challenge/psstdata',
    description='Tool for downloading and loading the data for the PSST Challenge',
    install_requires=[
        "requests"
    ],
    include_package_data=True,  # See MANIFEST.in for package files
)

