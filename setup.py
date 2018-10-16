import numpy
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
from distutils.extension import Extension
try:
    from Cython.Build import cythonize
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True
from distutils.command.sdist import sdist as _sdist

# Run the following line to compile atomset package
# python setup.py build_ext --inplace


class sdist(_sdist):
    def run(self):
        # Make sure the compiled Cython files in the distribution are
        # up-to-date
        from Cython.Build import cythonize
        cythonize(['cython/mycythonmodule.pyx'])
        _sdist.run(self)
        cmdclass['sdist'] = sdist

here = path.abspath(path.dirname(__file__))
ext_modules = []
cmdclass = {}
# Get the long description from the README file
with open(path.join(here, 'AdaptivePELE/README.rst'), encoding='utf-8') as f:
    long_description = f.read()

if use_cython:
    ext_modules += [
        Extension("MSM_PELE.AdaptivePELE.atomset.atomset", ["MSM_PELE/AdaptivePELE/atomset/atomset.pyx"], include_dirs=["MSM_PELE/AdaptivePELE", "MSM_PELE/AdaptivePELE/atomset"]),
        Extension("MSM_PELE.AdaptivePELE.atomset.SymmetryContactMapEvaluator", ["MSM_PELE/AdaptivePELE/atomset/SymmetryContactMapEvaluator.pyx"], include_dirs=["MSM_PELE/AdaptivePELE", "MSM_PELE/AdaptivePELE/atomset"]),
        Extension("MSM_PELE.AdaptivePELE.atomset.RMSDCalculator", ["MSM_PELE/AdaptivePELE/atomset/RMSDCalculator.pyx"], include_dirs=["MSM_PELE/AdaptivePELE", "MSM_PELE/AdaptivePELE/atomset"]),
        Extension("MSM_PELE.AdaptivePELE.freeEnergies.utils", ["MSM_PELE/AdaptivePELE/freeEnergies/utils.pyx"], include_dirs=["MSM_PELE/AdaptivePELE", "MSM_PELE/AdaptivePELE/freeEnergies"])
    ]
    cmdclass.update({'build_ext': build_ext})
else:
    ext_modules += [
        Extension("MSM_PELE.AdaptivePELE.atomset.atomset", ["MSM_PELE/AdaptivePELE/atomset/atomset.c"], include_dirs=["MSM_PELE/AdaptivePELE", "MSM_PELE/AdaptivePELE/atomset"]),
        Extension("MSM_PELE.AdaptivePELE.atomset.SymmetryContactMapEvaluator", ["MSM_PELE/AdaptivePELE/atomset/SymmetryContactMapEvaluator.c"], include_dirs=["MSM_PELE/AdaptivePELE", "MSM_PELE/AdaptivePELE/atomset"]),
        Extension("MSM_PELE.AdaptivePELE.atomset.RMSDCalculator", ["MSM_PELE/AdaptivePELE/atomset/RMSDCalculator.c"], include_dirs=["MSM_PELE/AdaptivePELE", "MSM_PELE/AdaptivePELE/atomset"]),
        Extension("MSM_PELE.AdaptivePELE.freeEnergies.utils", ["MSM_PELE/AdaptivePELE/freeEnergies/utils.c"], include_dirs=["MSM_PELE/AdaptivePELE", "MSM_PELE/AdaptivePELE/freeEnergies"])
    ]

setup(
    name="AdaptivePELE",
    version="1.5",
    description='Enhanced sampling of molecular simulations',
    long_description=long_description,
    url="https://github.com/cescgina/AdaptivePELE",
    author='Daniel Lecina, Joan Francesc Gilabert',
    author_email='danilecina@gmail.com, cescgina@gmail.com',
    license='',
    packages=find_packages(exclude=['docs', 'tests']),
    package_data={"MSM_PELE/AdaptivePELE/atomset": ['*.pxd']},
    install_requires=['numpy', 'mdtraj'],
    cmdclass=cmdclass,
    ext_modules=cythonize(ext_modules),  # accepts a glob pattern
    include_dirs=[numpy.get_include()]
)
