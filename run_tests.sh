set -ev

# clean up from previous tests
rm -rf dist/ .tox/ tox-pip.log

# build both source distribution and wheel
# (source distribution enables tests with different python version)
python setup.py sdist bdist_wheel
tox
