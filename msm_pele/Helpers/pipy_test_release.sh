#Clean and reinstall requirements
pip uninstall -r requirements.txt --yes
pip uninstall msm_pele --yes
pip install cython numpy setuptools
pip install .

#Clean and build
rm -r dist build msm_pele.egg*
python setup.py sdist
twine upload  --repository-url https://test.pypi.org/legacy/ dist/*
#twine upload  dist/*
