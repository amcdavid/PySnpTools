import numpy as np
import scipy as sp
import logging

# attempt to import wrapped plink parser
WRAPPED_PLINK_PARSER_PRESENT = True
try:
    import pysnptools.pysnptools.snpreader.wrap_plink_parser as wrap_plink_parser
except Exception:
    WRAPPED_PLINK_PARSER_PRESENT = False


class Unit(object):  #IStandardizer
    """The specification for unit standardization"""
    def __init__(self):
        pass

    def standardize(self, snps, blocksize=None, force_python_only=False):
        l = self.lambdaFactory(snps, blocksize=blocksize, force_python_only=force_python_only)
        import pysnptools.pysnptools.standardizer as stdizer
        return stdizer.standardize_with_lambda(snps, l, blocksize)

    def __repr__(self): 
        return "{0}()".format(self.__class__.__name__)

    def lambdaFactory(self, snps, blocksize=None, force_python_only=False):
        if not force_python_only:
            if snps.dtype == np.float64:
                if snps.flags['F_CONTIGUOUS'] and (snps.flags["OWNDATA"] or snps.base.nbytes == snps.nbytes):
                    #!!!cmk05192014 LATER: set snps to np.load(D:\Source\carlk_snpreader\tests\temp.npz.npz) and then run this. It fails without error. Could it be that standardizing twice, sometimes causes this?
                    return lambda s : wrap_plink_parser.standardizedoubleFAAA(s,False,float("NaN"),float("NaN"))
                elif snps.flags['C_CONTIGUOUS'] and (snps.flags["OWNDATA"] or snps.base.nbytes == snps.nbytes) and blocksize is None:
                    return lambda s : wrap_plink_parser.standardizedoubleCAAA(s,False,float("NaN"),float("NaN"))
                else:
                    logging.info("Array is not contiguous, so will standardize with python only instead of C++")
            elif snps.dtype == np.float32:
                if snps.flags['F_CONTIGUOUS'] and (snps.flags["OWNDATA"] or snps.base.nbytes == snps.nbytes):
                    return lambda s: wrap_plink_parser.standardizefloatFAAA(s,False,float("NaN"),float("NaN"))
                elif snps.flags['C_CONTIGUOUS'] and (snps.flags["OWNDATA"] or snps.base.nbytes == snps.nbytes) and blocksize is None:
                    return lambda s: wrap_plink_parser.standardizefloatCAAA(s,False,float("NaN"),float("NaN"))
                else:
                    logging.info("Array is not contiguous, so will standardize with python only instead of C++")
            else:
                logging.info("Array type is not float64 or float32, so will standardize with python only instead of C++")

        import pysnptools.pysnptools.standardizer as stdizer
        return lambda s: stdizer.standardize_unit_python(s)


