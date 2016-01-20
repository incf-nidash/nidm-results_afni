"""
Export neuroimaging results created with feat in AFNI following NIDM-Results 
specification.

@author: Rick Reynolds/Camille Maumet
@copyright: 
"""

import re
import os
import glob
import numpy as np
from exporter.exporter import NIDMExporter
from exporter.objects.constants import *
from exporter.objects.modelfitting import *
from exporter.objects.contrast import *
from exporter.objects.inference import *
import objects.afni_objects as afniobjs

class AFNItoNIDMExporter(NIDMExporter, object):
    """ 
    Parse an AFNI group result to extract the pieces information to be 
    stored in NIDM-Results and generate a NIDM-Results export.
    """

    def __init__(self, dset, csim_dset, p_uncor=0.01, p_cor=0.05,
                 nidm_ver="0.2.0"):
        self.stat_dset = dset
        self.clust_dset = csim_dset
        self.p_uncor = p_uncor
        self.p_cor = p_cor

        self.ind_contr = 0
        self.ind_stat  = 1

        self.afni_dir = os.path.dirname(self.stat_dset)

        nidm_dirs = glob.glob(os.path.join(self.afni_dir, 'nidm*'))
        if nidm_dirs:
            if nidm_dirs[-1] == os.path.join(self.afni_dir, 'nidm'):
                export_dir_num = 1
            else:
                m = re.search('(?<=nidm_).*', nidm_dirs[-1])
                export_dir_num = int(m.group(0))+1

            self.export_dir = os.path.join(self.afni_dir, \
                'nidm'+"_{0:0>4}".format(export_dir_num))
        else:
            self.export_dir = os.path.join(self.afni_dir, 'nidm')

        self.design_txt = None
        self.coordinate_system = None

    def parse(self):
        """ 
        Parse an AFNI result directory to extract the pieces information to be 
        stored in NIDM-Results.
        """    
        # rcr - ponder
        # design_file_open = open(self.design_file, 'r')
        # self.design_txt = design_file_open.read()
        

        # Retreive coordinate space used for current analysis
        if not self.coordinate_system:
            self._get_coordinate_system()

        super(AFNItoNIDMExporter, self).parse()

    def _add_namespaces(self):
        """ 
        Overload of parent _add_namespaces to add AFNI namespace.
        """
        super(AFNItoNIDMExporter, self).__init__()
        self.doc.add_namespace(AFNI)

    def _find_software(self):
        """ 
        Return an object of type Software describing the version of AFNI used to
        compute the current analysis.
        """
        #version_re = r'.*set fmri\(version\) (?P<info>\d+\.?\d+).*'
        #afni_version = self._search_in_fsf(version_re)

        version = os.system("afni -ver")   # get a string
        software = afniobjs.Software(version=version)

        return software

    def _find_model_fitting(self):
        """ 
        Parse AFNI result directory to retreive model fitting information. 
        Return a list of objects of type ModelFitting.
        """
        # design_matrix = self._get_design_matrix()
        # data = self._get_data()
        # error_model = self._get_error_model()

        # rms_map = self._get_residual_mean_squares_map()
        # param_estimates = self._get_param_estimate_maps()
        # mask_map = self._get_mask_map()
        # grand_mean_map = self._get_grand_mean(mask_map.file)

        # activity = self._get_model_parameters_estimations(error_model)

        # model_fitting = ModelFitting(activity, design_matrix, data, 
        #     error_model, param_estimates, rms_map, mask_map, grand_mean_map)

        return list()

    def _find_contrasts(self):
        """ 
        Parse AFNI result directory to retreive information about contrasts. 
        Return a dictionary of (key, value) pairs where key is a tuple 
        containing the identifier of a ModelParametersEstimation object and a 
        tuple of identifiers of ParameterEstimateMap objects, and value is an 
        object of type Contrast.
        """
        return dict()

    def _find_inferences(self):
        """ 
        Parse AFNI result directory to retreive information about inference 
        along with peaks and clusters. Return a dictionary of (key, value) 
        pairs where key is the identifier of a ContrastEstimation object and 
        value is an object of type Inference.
        """
        inferences = dict()

        return inferences
