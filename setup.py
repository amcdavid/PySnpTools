import platform
import os
import sys
import shutil
from setuptools import setup, Extension
from distutils.command.clean import clean as Clean
from Cython.Distutils import build_ext
import numpy



# Version number
version = '0.2.8'

def readme():
    with open('README.md') as f:
        return f.read()

# set up macro
if platform.system() == "Darwin":
    macros = [("__APPLE__", "1")]
elif "win" in platform.system().lower():
    macros = [("_WIN32", "1")]
else:
    macros = [("_UNIX", "1")]

ext_modules = [Extension(name="pysnptools.snpreader.wrap_plink_parser",
                         language="c++",
                         sources=["pysnptools/snpreader/wrap_plink_parser.pyx", "pysnptools/snpreader/CPlinkBedFile.cpp"],
                         include_dirs = [numpy.get_include()],
                         define_macros=macros),
               Extension(name="pysnptools.snpreader.wrap_matrix_subset",
                        language="c++",
                        sources=["pysnptools/snpreader/wrap_matrix_subset.pyx", "pysnptools/snpreader/MatrixSubset.cpp"],
                        include_dirs = [numpy.get_include()],
                        define_macros=macros)]

class CleanCommand(Clean):
    description = "Remove build directories, and compiled files (including .pyc)"

    def run(self):
        Clean.run(self)
        if os.path.exists('build'):
            shutil.rmtree('build')
        for dirpath, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                if (   filename.endswith('.so')
                    or filename.endswith('.pyd')
                    or filename.find("wrap_plink_parser.cpp") != -1 # remove automatically generated source file
                    or filename.find("wrap_matrix_subset.cpp") != -1 # remove automatically generated source file
                    or filename.endswith('.pyc')
                                ):
                    tmp_fn = os.path.join(dirpath, filename)
                    print "removing", tmp_fn
                    os.unlink(tmp_fn)

#python setup.py sdist bdist_wininst upload
setup(
    name='pysnptools',
    version=version,
    description='PySnpTools',
    long_description=readme(),
    keywords='gwas bioinformatics sets intervals ranges regions',
    url="http://research.microsoft.com/en-us/um/redmond/projects/mscompbio/",
    author='MSR',
    author_email='fastlmm@microsoft.com',
    license='Apache 2.0',
    packages=[
        "pysnptools/snpreader",
        "pysnptools/standardizer",
        "pysnptools/util",
        "pysnptools"
    ],
    package_data={"pysnptools" : [
        "test/datasets/all_chr.maf0.001.N300.bed",
        "test/datasets/all_chr.maf0.001.N300.bim",
        "test/datasets/all_chr.maf0.001.N300.fam",
        "test/datasets/phenSynthFrom22.23.N300.randcidorder.txt",
        "tests/datasets/all_chr.maf0.001.covariates.N300.txt"
        ]
                 },
    requires = ['cython', 'numpy', 'scipy', 'pandas'],
    # extensions
    cmdclass = {'build_ext': build_ext, 'clean': CleanCommand},
    ext_modules = ext_modules
  )

