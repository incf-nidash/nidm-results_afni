"""
Export neuroimaging results created with feat in AFNI following NIDM-Results
specification.

@author: Rick Reynolds/Camille Maumet
@copyright:
"""

import re
import os
import glob
import subprocess
from nidmresults.exporter import NIDMExporter
from nidmresults.objects.constants import AFNI
import objects.afni_objects as afniobjs


class AFNItoNIDMExporter(NIDMExporter, object):
    """
    Parse an AFNI group result to extract the pieces information to be
    stored in NIDM-Results and generate a NIDM-Results export.
    """

    def __init__(self, dataset, csim_dset, p_uncor=0.01, p_cor=0.05,
                 version="0.2.0"):
        super(AFNItoNIDMExporter, self).__init__()
        self.dataset = dataset
        self.clust_dset = csim_dset
        self.p_uncor = p_uncor
        self.p_cor = p_cor
        self.version = version

        self.ind_contr = 0
        self.ind_stat = 1

        self.afni_dir = os.path.dirname(dataset)

        nidm_dirs = glob.glob(os.path.join(self.afni_dir, 'nidm*'))
        if nidm_dirs:
            if nidm_dirs[-1] == os.path.join(self.afni_dir, 'nidm'):
                export_dir_num = 1
            else:
                m = re.search('(?<=nidm_).*', nidm_dirs[-1])
                export_dir_num = int(m.group(0))+1

            self.export_dir = os.path.join(
                self.afni_dir, 'nidm'+"_{0:0>4}".format(export_dir_num))
        else:
            self.export_dir = os.path.join(self.afni_dir, 'nidm')

        self.design_txt = None
        self.coordinate_system = None
        self.read_history(dataset)
        print self.history

    def read_history(self, dataset):
        self.history = subprocess.check_output("3dinfo "+dataset, shell=True)
        # FIXME: here we need to parse this history to get:
        # - path to statistic map
        # - path to parameter estimate map
        # - path to contrast map
        # - degrees of freedom
        # - coordinate space info
        # - afni function used: 3dttest, other

    def parse(self):
        """
        Parse an AFNI result directory to extract the pieces information to be
        stored in NIDM-Results.
        """
        # Retreive coordinate space used for current analysis
        # if not self.coordinate_system:
        #     self._get_coordinate_system()

        super(AFNItoNIDMExporter, self).parse()

    def _add_namespaces(self):
        """
        Overload of parent _add_namespaces to add AFNI namespace.
        """
        self.doc.add_namespace(AFNI)

    def _find_software(self):
        """
        Return an object of type Software describing the version of AFNI used
        to compute the current analysis.
        """
        # FIXME: Do we want to keep the full output of version, e.g.
        # Precompiled binary macosx_10.7_Intel_64: Sep 25 2014 (Version
        # AFNI_2011_12_21_1014)
        version = subprocess.check_output("afni -ver", shell=True)
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
        self.model_fittings = dict()

        # stat_dir = os.path.join(analysis_dir, 'stats')

        # design_matrix = self._get_design_matrix(analysis_dir)
        # data = self._get_data()
        # error_model = self._get_error_model()

        # rms_map = self._get_residual_mean_squares_map(stat_dir)
        # param_estimates = self._get_param_estimate_maps(stat_dir)
        # mask_map = self._get_mask_map(analysis_dir)
        # grand_mean_map = self._get_grand_mean(mask_map.file, analysis_dir)

        # activity = self._get_model_parameters_estimations(error_model)

        # model_fitting = ModelFitting(
        #     activity, design_matrix, data,
        #     error_model, param_estimates, rms_map, mask_map,
        #     grand_mean_map)

        # self.model_fittings[analysis_dir] = model_fitting

        return self.model_fittings

    def _get_design_matrix(self, analysis_dir):
        """
        Parse FSL result directory to retreive information about the design
        matrix. Return an object of type DesignMatrix.
        """
        design_mat_file = os.path.join(analysis_dir, 'design.mat')
        design_mat_fid = open(design_mat_file, 'r')
        design_mat_values = np.loadtxt(design_mat_fid, skiprows=5, ndmin=2)
        design_mat_image = os.path.join(analysis_dir, 'design.png')

        # Regressor names (not taking into account HRF model)
        regnames_re = r'.*set fmri\(evtitle\d+\).*'
        ev_names = re.findall(regnames_re, self.design_txt)

        orig_ev = dict()
        for ev_name in ev_names:
            regname_re = r'.*set fmri\(evtitle(?P<num>\d+)\)\s*"(?P<name>.*)"'
            info_search = re.compile(regname_re)
            info_found = info_search.search(ev_name)
            num = info_found.group('num')
            name = info_found.group('name')
            orig_ev[int(num)] = name

        # For first-level fMRI only
        if self.first_level:
            # FIXME: we are only dealing with group level for now
            print "first level"
        else:
            design_type = None
            hrf_model = None
            drift_model = None

        real_ev = list()
        for ev_num, ev_name in orig_ev.items():
            real_ev.append(ev_name)

            # Add one regressor name if there is an extra column for a temporal
            # derivative
            tempo_deriv_re = \
                r'.*set fmri\(deriv_yn'+str(ev_num)+'\) (?P<info>[\d]+).*'
            tempo_deriv = bool(self._search_in_fsf(tempo_deriv_re))

            if tempo_deriv:
                real_ev.append(ev_name+'*temporal_derivative')

            # FIXME: other hrf models (FIR...)

        design_matrix = DesignMatrix(design_mat_values, design_mat_image,
                                     self.export_dir, real_ev, design_type,
                                     hrf_model, drift_model)
        return design_matrix

    def _get_data(self):
        """
        Parse FSL result directory to retreive information about the data.
        Return an object of type Data.
        """
        # FIXME: grand_mean_scaling and target_intensity needs to be updated 
        # with actual AFNI values
        grand_mean_scaling = True
        target_intensity = 10000.0
        data = Data(grand_mean_scaling, target_intensity)
        return data

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
