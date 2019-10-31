#Clean after build
pip uninstall msm_pele --yes
pip install --index-url https://test.pypi.org/simple/ msm_pele
cd tests
pytest
