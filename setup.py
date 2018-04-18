from setuptools import setup, find_packages
import versioneer

setup(
    name="topojson",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license="BSD",
    packages=find_packages(exclude=['tests']),
    test_suite="tests"
)
