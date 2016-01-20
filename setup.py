from setuptools import setup, find_packages

readme = open('README.md').read()

reqs = [line.strip() for line in open('requirements.txt').readlines()]
requirements = list(filter(None, reqs))

setup(
    name="nidmafni",
    version="0.1.0",
    author="Camille Maumet, Rick Reynolds",
    author_email="c.m.j.maumet@warwick.ac.uk",
    description=("Export of AFNI statistical results using NIDM\
 as specified at http://nidm.nidash.org/specs/nidm-results.html."),
    license = "BSD",
    keywords = "Prov, NIDM, Provenance",
    scripts=['bin/nidmafni'],
    # packages=['nidmfsl', 'test'],
    packages=find_packages(),
    package_dir={
        'prov': 'prov'
    },
    long_description=readme,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=requirements
)
