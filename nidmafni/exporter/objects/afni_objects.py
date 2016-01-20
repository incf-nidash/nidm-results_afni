"""
AFNI-specific classes and classes overloaded to add AFNI-specific attributes.

@author: Rick Reynolds/Camille Maumet
@copyright:
"""
from nidmresults.objects.generic import NIDMObject
from nidmresults.objects.constants import *
import logging
import uuid

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Software(NIDMObject):
    # FIXME software should be generic and then overloaded

    """
    Class representing a Software entity.
    """

    def __init__(self, version):
        super(Software, self).__init__()
        self.version = version
        self.name = "AFNI"
        self.type = NLX_AFNI
        self.prov_type = PROV['Agent']
        self.id = NIIRI[str(uuid.uuid4())]
        # Retreive AFNI version from afni -ver

    def export(self):
        """
        Create prov entities and activities.
        """
        self.add_attributes((
            (PROV['type'], NLX_FSL),
            (PROV['type'], PROV['SoftwareAgent']),
            (PROV['label'], self.name),
            (NIDM_SOFTWARE_VERSION, self.version)))

        return self.p
