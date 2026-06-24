# ***********************************************************************
# ******************  CANADIAN ASTRONOMY DATA CENTRE  *******************
# *************  CENTRE CANADIEN DE DONNÉES ASTRONOMIQUES  **************
#
#  (c) 2026.                            (c) 2026.
#  Government of Canada                 Gouvernement du Canada
#  National Research Council            Conseil national de recherches
#  Ottawa, Canada, K1A 0R6              Ottawa, Canada, K1A 0R6
#  All rights reserved                  Tous droits réservés
#
#  NRC disclaims any warranties,        Le CNRC dénie toute garantie
#  expressed, implied, or               énoncée, implicite ou légale,
#  statutory, of any kind with          de quelque nature que ce
#  respect to the software,             soit, concernant le logiciel,
#  including without limitation         y compris sans restriction
#  any warranty of merchantability      toute garantie de valeur
#  or fitness for a particular          marchande ou de pertinence
#  purpose. NRC shall not be            pour un usage particulier.
#  liable in any event for any          Le CNRC ne pourra en aucun cas
#  damages, whether direct or           être tenu responsable de tout
#  indirect, special or general,        dommage, direct ou indirect,
#  consequential or incidental,         particulier ou général,
#  arising from the use of the          accessoire ou fortuit, résultant
#  software.  Neither the name          de l'utilisation du logiciel. Ni
#  of the National Research             le nom du Conseil National de
#  Council of Canada nor the            Recherches du Canada ni les noms
#  names of its contributors may        de ses  participants ne peuvent
#  be used to endorse or promote        être utilisés pour approuver ou
#  products derived from this           promouvoir les produits dérivés
#  software without specific prior      de ce logiciel sans autorisation
#  written permission.                  préalable et particulière
#                                       par écrit.
#
#  This file is part of the             Ce fichier fait partie du projet
#  OpenCADC project.                    OpenCADC.
#
#  OpenCADC is free software:           OpenCADC est un logiciel libre ;
#  you can redistribute it and/or       vous pouvez le redistribuer ou le
#  modify it under the terms of         modifier suivant les termes de
#  the GNU Affero General Public        la “GNU Affero General Public
#  License as published by the          License” telle que publiée
#  Free Software Foundation,            par la Free Software Foundation
#  either version 3 of the              : soit la version 3 de cette
#  License, or (at your option)         licence, soit (à votre gré)
#  any later version.                   toute version ultérieure.
#
#  OpenCADC is distributed in the       OpenCADC est distribué
#  hope that it will be useful,         dans l’espoir qu’il vous
#  but WITHOUT ANY WARRANTY;            sera utile, mais SANS AUCUNE
#  without even the implied             GARANTIE : sans même la garantie
#  warranty of MERCHANTABILITY          implicite de COMMERCIALISABILITÉ
#  or FITNESS FOR A PARTICULAR          ni d’ADÉQUATION À UN OBJECTIF
#  PURPOSE.  See the GNU Affero         PARTICULIER. Consultez la Licence
#  General Public License for           Générale Publique GNU Affero
#  more details.                        pour plus de détails.
#
#  You should have received             Vous devriez avoir reçu une
#  a copy of the GNU Affero             copie de la Licence Générale
#  General Public License along         Publique GNU Affero avec
#  with OpenCADC.  If not, see          OpenCADC ; si ce n’est
#  <http://www.gnu.org/licenses/>.      pas le cas, consultez :
#                                       <http://www.gnu.org/licenses/>.
#
#  $Revision: 4 $
#
# ***********************************************************************
#

"""
This module implements the ObsBlueprint mapping, as well as the workflow
entry point that executes the workflow.

JJK - 05-10-20
ALMA Telescopes: there are three telescopes that are part of the ALMA
observatory:
Main Array: 50 x 12m antennas
Total Power Array: 4 x 12m antennas
Atacama Compact Array (ACA): 12 x 7m antennas

CW - 20-10-20
In CAOM I would have telescope be the telescope and instrument the instrument
on the telescope. How results get shown is another matter. We should add
telescope to the list of returned fields, then it can be set to be in the
default set for PHANGS and hidden for others.

PD - 04-05-21 - Cardinality Guidance found here:
https://cadc-ccda.atlassian.net/wiki/spaces/C/pages/1133281297/PHANGS

"""

import re

from math import sqrt

from caom2 import DataProductType, CalibrationLevel, Provenance, Proposal, ProductType, ReleaseType
from caom2pipe import caom_composable as cc
from caom2pipe import manage_composable as mc


__all__ = ['PHANGSName', 'PHANGSMapping']


class PHANGSName(mc.StorageName):
    """Naming rules:
    - support mixed-case file name storage, and mixed-case obs id values
    - support uncompressed files in storage
    """

    def __init__(self, source_names):
        super().__init__(source_names=source_names)
        self._target_name = None
        self._telescope = None
        self._assign_bits()

    @property
    def target_name(self):
        return self._target_name

    @property
    def telescope(self):
        return self._telescope

    def is_x(self):
        return '_strictmask' in self._file_id or '_broadmask' in self._file_id or '_coverage' in self._file_id

    def is_error(self):
        return 'emom' in self._file_id or 'eew' in self._file_id

    def set_obs_id(self):
        bits = self._file_id.split('_')
        self._obs_id = f'{bits[0]}_{bits[1]}_{bits[2]}'

    def set_product_id(self):
        bits = self._file_id.split('_')
        # PD - Confluence guidance
        if len(bits) == 3 or 'tpeak' in self._file_id:
            self._product_id = self._file_id
        elif self._file_id.endswith('_noise') or self.is_x():
            self._product_id = '_'.join(ii for ii in bits[:-1])
        elif re.match('.*mom[012]', self._file_id):
            self._product_id = f'{"_".join(ii for ii in bits[:-1])}_mom{self._file_id[-1]}'
        elif re.match('.*ew', self._file_id):
            self._product_id = '_'.join(ii for ii in bits[:-1]) + '_ew'
        elif len(bits) == 4:
            self._product_id = self._file_id
        else:
            raise mc.CadcException(f'Unexpected file name pattern {self._file_id}')

    def _assign_bits(self):
        # the right-hand side of the dictionary comes from ALMA/ALMACA
        # collections telescope names
        telescope_lookup = {
            '7m+tp': 'ALMA-7m + ALMA-TP',
            '7m+12m': 'ALMA-7m + ALMA-12m',
            '12m+7m': 'ALMA-7m + ALMA-12m',
            'tp+12m': 'ALMA-12m + ALMA-TP',
            '12m+tp': 'ALMA-12m + ALMA-TP',
            'tp+7m': 'ALMA-7m + ALMA-TP',
            '12m+7m+tp': 'ALMA-12m + ALMA-7m + ALMA-TP',
        }
        bits = self._file_id.split('_')
        self._target_name = bits[0]
        self._telescope = telescope_lookup.get(bits[1])
        if self._telescope is None:
            raise mc.CadcException(f'Unexpected telescope value in {self._file_id}')


class PHANGSMapping(cc.TelescopeMapping2):

    def accumulate_blueprint(self, bp):
        """Configure the telescope-specific ObsBlueprint at the CAOM model
        Observation level."""
        super().accumulate_blueprint(bp)
        bp.configure_position_axes((1, 2))
        bp.configure_energy_axis(3)

        # all DerivedObservations, even though members are unknown at CADC
        bp.set('DerivedObservation.members', {})
        # TBD - there are many more values than this, so maybe there should be
        # many more observations than this?
        bp.set('Observation.algorithm.name', 'phangs_imaging')

        if 'ALMA' in self._storage_name.telescope:
            # ER 15-10-20
            # For ALMA, the 'filter' field could be set to Band6, which is the
            # receiver band used by the observations and thus forms a useful
            # analogue to the "Filter" set for optical telescopes.
            # CW 20-10-10
            # In CAOM I would have telescope be the telescope and instrument the
            # instrument on the telescope.
            # SGo - so, use the ALMA/ALMACA instrument names accordingly
            bp.set('Observation.instrument.name', 'Band 6')

        bp.set('Observation.target.name', self._storage_name.target_name)

        bp.set('Observation.telescope.name', self._storage_name.telescope)
        bp.set('Observation.telescope.geoLocationX', 2225015.30883296)
        bp.set('Observation.telescope.geoLocationY', -5440016.41799762)
        bp.set('Observation.telescope.geoLocationZ', -2481631.27428014)

        data_product_type = DataProductType.CUBE
        if '_strict_' in self._storage_name.file_uri or '_broad_' in self._storage_name.file_uri:
            # ER 05-03-21
            # everything with a "_strict_" or "_broad_" in the filename as an
            # image (these should also have NAXIS=2 in the header). Everything
            # else should be "cube" with NAXIS=3.
            data_product_type = DataProductType.IMAGE

        calibration_level = CalibrationLevel.PRODUCT
        if len(self._storage_name.product_id.split('_')) == 3:
            calibration_level = CalibrationLevel.CALIBRATED

        bp.set('Plane.calibrationLevel', calibration_level)
        bp.set('Plane.dataProductType', data_product_type)
        bp.clear('Plane.dataRelease')
        bp.add_attribute('Plane.dataRelease', 'DATE')
        bp.clear('Plane.metaRelease')
        bp.add_attribute('Plane.metaRelease', 'DATE')

        artifact_product_type = ProductType.SCIENCE
        if 'noise' in self._storage_name.file_uri:
            artifact_product_type = ProductType.NOISE
        elif self._storage_name.is_x() or self._storage_name.is_error():
            artifact_product_type = ProductType.AUXILIARY
        bp.set('Artifact.productType', artifact_product_type)
        bp.set('Artifact.releaseType', ReleaseType.DATA)

        # chunk level
        # position
        bp.clear('Chunk.position.axis.function.cd11')
        bp.clear('Chunk.position.axis.function.cd22')
        bp.add_attribute('Chunk.position.axis.function.cd11', 'CDELT1')
        bp.set('Chunk.position.axis.function.cd12', 0.0)
        bp.set('Chunk.position.axis.function.cd21', 0.0)
        bp.add_attribute('Chunk.position.axis.function.cd22', 'CDELT2')
        bp.set('Chunk.position.resolution', '_get_position_resolution(header)')

        # energy
        bp.clear('Chunk.energy.transition.species')
        bp.add_attribute('Chunk.energy.transition.species', 'MOLECULE')
        bp.clear('Chunk.energy.transition.transition')
        bp.add_attribute('Chunk.energy.transition.transition', 'TRANSITI')

        # observable
        if (
            artifact_product_type in [ProductType.SCIENCE, ProductType.NOISE]
            or self._storage_name.is_error()  # some auxiliary Artifacts have observables
        ):
            bp.configure_observable_axis(4)
            bp.set('Chunk.observable.dependent.axis.ctype', '_get_chunk_observable_ctype(header)')
            bp.clear('Chunk.observable.dependent.axis.cunit')
            bp.add_attribute('Chunk.observable.dependent.axis.cunit', 'BUNIT')
            bp.set('Chunk.observable.dependent.bin', 1)
        self._logger.debug('Done accumulate_bp.')

    def _get_chunk_observable_ctype(self, ext):
        btype_fix = {
            'Moment0': 'moment0',
            'Moment1': 'moment1',
            'Moment2': 'moment2',
            'Moment0 Error': 'moment0;error',
            'Moment1 Error': 'moment1;error',
            'Moment2 Error': 'moment2;error',
            'Tpeak': 'T',
            'VelDisp EW': 'VelDisp',
            'VelDisp EW Error': 'VelDisp;error',
        }
        btype = self._headers[ext].get('BTYPE')
        corrected = btype_fix.get(btype, btype)
        return corrected

    def _get_position_resolution(self, ext):
        bmaj = self._headers[ext].get('BMAJ')
        bmin = self._headers[ext].get('BMIN')
        # From
        # https://open-confluence.nrao.edu/pages/viewpage.action?pageId=13697486
        # Clare Chandler via JJK - 21-08-18
        result = None
        if bmaj is not None and bmin is not None:
            result = 3600.0 * sqrt(bmaj * bmin)
        return result

    def _update_artifact(self, artifact):
        pass

    def _update_from_comment(self, plane):
        # From ER: 04-03-21
        # COMMENT Produced with PHANGS-ALMA pipeline version 4.0 Build 935
        # - Provenance.version
        # COMMENT Galaxy properties from PHANGS sample table version 1.6
        # COMMENT Calibration Level 4 (ANALYSIS_PRODUCT)
        # - Calibration level (either 3 or 4)
        # COMMENT PHANGS-ALMA Public Release 1
        # - Provenance.project = PHANGS-ALMA
        # COMMENT Generated by the Physics at High Angular resolution
        # COMMENT in nearby GalaxieS (PHANGS) collaboration
        # - Provenance.organization = PHANGS
        # COMMENT Canonical Reference: Leroy et al. (2021), ApJ, Submitted
        # - Update to reference when accepted
        # COMMENT Release generated at 2021-03-04T07:28:10.245340
        # - Provenance.lastExecuted
        # COMMENT Data from ALMA Proposal ID: 2017.1.00886.L
        # - Proposal.proposalID
        # COMMENT ALMA Proposal PI: Schinnerer, Eva
        # - Proposal.pi_name
        # COMMENT Observed in MJD interval [58077.386275,58081.464121]
        # COMMENT Observed in MJD interval [58290.770032,58365.629222]
        # COMMENT Observed in MJD interval [58037.515807,58047.541173]
        # COMMENT Observed in MJD interval [58353.589805,58381.654757]
        # COMMENT Observed in MJD interval [58064.3677,58072.458597]
        # COMMENT Observed in MJD interval [58114.347649,58139.301879]
        chunk = None
        if plane.provenance is None:
            plane.provenance = Provenance(name='PHANGS-ALMA pipeline')

        for artifact in plane.artifacts.values():
            if artifact.uri != self._storage_name.file_uri.replace('.header', ''):
                continue
            for part in artifact.parts.values():
                chunk = part.chunks[0]
                break

        for entry in self._headers[0].get('COMMENT'):
            if 'pipeline version ' in entry:
                plane.provenance.version = entry.split(' version ')[1]
            elif 'PHANGS-ALMA Public Release' in entry:
                plane.provenance.project = 'PHANGS-ALMA'
            elif 'Release generated at ' in entry:
                plane.provenance.last_executed = mc.make_datetime(entry.split(' at ')[1])
            elif 'Data from ALMA Proposal ID:' in entry:
                self._observation.proposal = Proposal(entry.split(':')[1].strip())
            elif 'Canonical Reference: ' in entry:
                plane.provenance.producer = entry.split(': ')[1]
            elif 'ALMA Proposal PI:' in entry:
                self._observation.proposal.pi_name = entry.split(': ')[1]
            elif 'Observed in MJD interval ' in entry:
                if chunk is not None:
                    bits = entry.split()[4].split(',')
                    chunk.time = cc.build_temporal_wcs_append_sample(
                        chunk.time,
                        lower=mc.to_float(bits[0].replace('[', '')),
                        upper=mc.to_float(bits[1].replace(']', '')),
                    )

    def _update_plane(self, plane):
        super()._update_plane(plane)
        self._update_from_comment(plane)
        if plane.provenance is not None and plane.calibration_level == CalibrationLevel.PRODUCT:
            bits = self._storage_name.file_name.split('_')
            # file id                               prov id
            #
            index_length = 4
            if len(bits) < 6:
                index_length = 3
            prov_prod_id = '_'.join(ii for ii in bits[:index_length])
            obs_member_uri_ignore, plane_uri = cc.make_plane_uri(
                self._observation.observation_id, prov_prod_id, self._storage_name.collection
            )
            plane.provenance.inputs.add(plane_uri)
        self._logger.debug(f'End _update_plane')
