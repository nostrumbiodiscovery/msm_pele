import subprocess
import shutil
# subprocess.call("pip install numpy cython".split())
import numpy
from setuptools import setup, find_packages, Command
from string import Template
# To use a consistent encoding
from codecs import open
from os import path
from distutils.extension import Extension
from setuptools.command.install import install
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



class PreInstallCommand(install):
    description = "Installer"
    user_options = install.user_options + [
        ('schr=', None, 'SCRHODINGER main path. i.e /opt/apps/schrodinger-2017/'),
        ('pele=', None, 'PELE main path. i.e /opt/apps/PELErev1234/'),
        ('pele-exec=', None, 'PELE bin path. i.e /opt/apps/PELErev1234/bin/Pele_mpi'),
        ('pele-license=', None, 'PELE licenses PATH. i.e /opt/apps/PELErev12345/licenses/'),
        ('mpirun=', None, 'mpirun PATH. i.e /usr/bin/mpirun')
    ]

    def initialize_options(self):
        install.initialize_options(self)
        self.schr = None
        self.pele = None
        self.pele_exec = None
        self.pele_license = None
        self.mpirun = None

    def finalize_options(self):
        install.finalize_options(self)
        if not self.schr:
            raise ValueError("Define --schr path. Check --help-commands for more help")
        if not self.pele:
            raise ValueError("Define --pele path. Check --help-commands for more help")
        if not self.pele_exec:
            raise ValueError("Define --pele-exec path. Check --help-commands for more help")
        if not self.pele_license:
            raise ValueError("Define --pele-license path. Check --help-commands for more help")
        if not self.mpirun:
            raise ValueError("Define --mpirun path. Check --help-commands for more help")

    def run(self):
        print("Cythonazing")
        subprocess.call("python msm_pele/setup.py build_ext --inplace".split())
        print("Installing packages")
        subprocess.call("pip install {}".format(" ".join(packages)).split())
        print("Setting environmental variables")
        installer(self.schr, self.pele, self.pele_exec, self.pele_license, self.mpirun)
        print("Install")
        install.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)


def installer(schr, pele, pele_exec, pele_license, mpirun):
    shutil.copy('msm_pele/Templates/constants.py', 'msm_pele/constants.py')
    d = {"SCHRODINGER":schr, "PELE":pele, "PELE_BIN":pele_exec, "LICENSE":pele_license, "MPIRUN":mpirun }
    file_input = 'msm_pele/constants.py'
    filein = open(file_input)
    src = Template( filein.read() )
    installation_content = src.safe_substitute(d)
    filein.close()
    with open(file_input, "w") as f:
        f.write(installation_content)

        

packages = ['numpy', 'matplotlib', 'pandas', 'cython', 'mdtraj', 'scipy', 'pyemma==2.4', 'prody==1.8.2', 'fpdf']
here = path.abspath(path.dirname(__file__))
ext_modules = []
cmdclass = {}
##cmdclass.update({'install': PreInstallCommand})


class sdist(_sdist):
    def run(self):
        # Make sure the compiled Cython files in the distribution are
        # up-to-date
        from Cython.Build import cythonize
        cythonize(['cython/mycythonmodule.pyx'])
        _sdist.run(self)
        cmdclass['sdist'] = sdist

        

if use_cython:
    ext_modules += [
        Extension("msm_pele.AdaptivePELE.atomset.atomset", ["msm_pele/AdaptivePELE/atomset/atomset.pyx"], include_dirs=["msm_pele/AdaptivePELE", "msm_pele/AdaptivePELE/atomset"]),
        Extension("msm_pele.AdaptivePELE.atomset.SymmetryContactMapEvaluator", ["msm_pele/AdaptivePELE/atomset/SymmetryContactMapEvaluator.pyx"], include_dirs=["msm_pele/AdaptivePELE", "msm_pele/AdaptivePELE/atomset"]),
        Extension("msm_pele.AdaptivePELE.atomset.RMSDCalculator", ["msm_pele/AdaptivePELE/atomset/RMSDCalculator.pyx"], include_dirs=["msm_pele/AdaptivePELE", "msm_pele/AdaptivePELE/atomset"]),
        Extension("msm_pele.AdaptivePELE.freeEnergies.utils", ["msm_pele/AdaptivePELE/freeEnergies/utils.pyx"], include_dirs=["msm_pele/AdaptivePELE", "msm_pele/AdaptivePELE/freeEnergies"])
    ]
    cmdclass.update({'build_ext': build_ext})
else:
    ext_modules += [
        Extension("msm_pele.AdaptivePELE.atomset.atomset", ["msm_pele/AdaptivePELE/atomset/atomset.c"], include_dirs=["msm_pele/AdaptivePELE", "msm_pele/AdaptivePELE/atomset"]),
        Extension("msm_pele.AdaptivePELE.atomset.SymmetryContactMapEvaluator", ["msm_pele/AdaptivePELE/atomset/SymmetryContactMapEvaluator.c"], include_dirs=["msm_pele/AdaptivePELE", "msm_pele/AdaptivePELE/atomset"]),
        Extension("msm_pele.AdaptivePELE.atomset.RMSDCalculator", ["msm_pele/AdaptivePELE/atomset/RMSDCalculator.c"], include_dirs=["msm_pele/AdaptivePELE", "msm_pele/AdaptivePELE/atomset"]),
        Extension("msm_pele.AdaptivePELE.freeEnergies.utils", ["msm_pele/AdaptivePELE/freeEnergies/utils.c"], include_dirs=["msm_pele/AdaptivePELE", "msm_pele/AdaptivePELE/freeEnergies"])
    ]

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name="msm_pele",
    version="2.1.0",
    description='Markov State Model analysis on MC simulation to calculate absolute free energies',
    long_description=long_description,
    url="https://github.com/danielSoler93/msm_pele/tree/devel",
    author='Daniel Soler Viladrich, Joan Francesc Gilabert',
    author_email='daniel.soler@nostrumbiodiscovery.com, cescgina@gmail.com',
    license='',
    packages=find_packages(exclude=['docs', 'tests']),
    package_data={"msm_pele/AdaptivePELE/atomset": ['*.pxd'], "msm_pele/Templates": ["*.pdb", "*.conf"] },
    include_package_data=True,
    install_requires=['numpy', 'mdtraj', 'scipy', 'pyemma', 'future', 'fpdf'],
    cmdclass=cmdclass,
    ext_modules=ext_modules,  # accepts a glob pattern
    include_dirs=[numpy.get_include()],
    classifiers=(
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 2.7",
    "License :: OSI Approved :: MIT License",
    "Intended Audience :: Science/Research"),
)

