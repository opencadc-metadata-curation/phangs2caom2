# -*- coding: utf-8 -*-
# ***********************************************************************
# ******************  CANADIAN ASTRONOMY DATA CENTRE  *******************
# *************  CENTRE CANADIEN DE DONNÉES ASTRONOMIQUES  **************
#
#  (c) 2020.                            (c) 2020.
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

import importlib
import logging
import os
import re
import sys
import traceback

from math import sqrt

from caom2 import Observation, DataProductType, CalibrationLevel
from caom2 import Provenance, Proposal, ProductType
from caom2utils import ObsBlueprint, get_gen_proc_arg_parser, gen_proc
from caom2pipe import caom_composable as cc
from caom2pipe import manage_composable as mc


__all__ = [
    'phangs_main_app',
    'update',
    'PHANGSName',
    'COLLECTION',
    'APPLICATION',
    'ARCHIVE',
    'to_caom2',
]


APPLICATION = 'phangs2caom2'
COLLECTION = 'PHANGS'
ARCHIVE = 'PHANGS'


class PHANGSName(mc.StorageName):
    """Naming rules:
    - support mixed-case file name storage, and mixed-case obs id values
    - support uncompressed files in storage
    """

    PHANGS_NAME_PATTERN = '*'

    def __init__(self, file_name=None, artifact_uri=None, entry=None):
        self._product_id = None
        if file_name:
            self.fname_in_ad = file_name
            self._file_name = file_name
            self._file_id = mc.StorageName.remove_extensions(file_name)
        elif artifact_uri:
            scheme, path, file_name = mc.decompose_uri(artifact_uri)
            self._file_name = file_name
            self._file_id = mc.StorageName.remove_extensions(file_name)
        self._assign_bits()
        super(PHANGSName, self).__init__(
            self._obs_id,
            COLLECTION,
            PHANGSName.PHANGS_NAME_PATTERN,
            fname_on_disk=file_name,
            compression='',
            entry=entry,
        )

    def __str__(self):
        return (
            f'obs_id {self._obs_id}, '
            f'product_id {self._product_id}, '
            f'file_id {self._file_id}'
        )

    @property
    def file_id(self):
        return self._file_id

    @property
    def file_name(self):
        return self._file_name.replace('.header', '')

    @property
    def product_id(self):
        return self._product_id

    @property
    def target_name(self):
        return self._target_name

    @property
    def telescope(self):
        return self._telescope

    def is_x(self):
        return (
            '_strictmask' in self._file_id
            or '_broadmask' in self._file_id
            or '_coverage' in self._file_id
        )

    def is_error(self):
        return 'emom' in self._file_id or 'eew' in self._file_id

    def is_valid(self):
        return True

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
        self._obs_id = f'{bits[0]}_{bits[1]}_{bits[2]}'
        self._target_name = bits[0]

        self._telescope = telescope_lookup.get(bits[1])
        if self._telescope is None:
            raise mc.CadcException(
                f'Unexpected telescope value in {self._file_id}'
            )

        # PD - Confluence guidance
        end_index = len(bits) - 1
        if len(bits) == 3 or 'tpeak' in self._file_id:
            self._product_id = self._file_id
        elif self._file_id.endswith('_noise') or self.is_x():
            self._product_id = '_'.join(ii for ii in bits[:end_index])
        elif re.match('.*mom[012]', self._file_id):
            self._product_id = (
                f'{"_".join(ii for ii in bits[:end_index])}_mom'
                f'{self._file_id[-1]}'
            )
        elif re.match('.*ew', self._file_id):
            self._product_id = '_'.join(ii for ii in bits[:end_index]) + '_ew'
        elif len(bits) == 4:
            self._product_id = self._file_id
        else:
            raise mc.CadcException(
                f'Unexpected file name pattern {self._file_id}'
            )


def accumulate_bp(bp, uri):
    """Configure the telescope-specific ObsBlueprint at the CAOM model
    Observation level."""
    logging.debug('Begin accumulate_bp.')
    bp.configure_position_axes((1, 2))
    bp.configure_energy_axis(3)

    storage_name = PHANGSName(artifact_uri=uri)

    # all DerivedObservations, even though members are unknown at CADC
    bp.set('DerivedObservation.members', {})
    # TBD - there are many more values than this, so maybe there should be
    # many more observations than this?
    bp.set('Observation.algorithm.name', 'phangs_imaging')

    if 'ALMA' in storage_name.telescope:
        # ER 15-10-20
        # For ALMA, the 'filter' field could be set to Band6, which is the
        # receiver band used by the observations and thus forms a useful
        # analogue to the "Filter" set for optical telescopes.
        # CW 20-10-10
        # In CAOM I would have telescope be the telescope and instrument the
        # instrument on the telescope.
        # SGo - so, use the ALMA/ALMACA instrument names accordingly
        bp.set('Observation.instrument.name', 'Band 6')

    bp.set('Observation.target.name', storage_name.target_name)

    bp.set('Observation.telescope.name', storage_name.telescope)
    bp.set('Observation.telescope.geoLocationX', 2225015.30883296)
    bp.set('Observation.telescope.geoLocationY', -5440016.41799762)
    bp.set('Observation.telescope.geoLocationZ', -2481631.27428014)

    data_product_type = DataProductType.CUBE
    if '_strict_' in uri or '_broad_' in uri:
        # ER 05-03-21
        # everything with a "_strict_" or "_broad_" in the filename as an
        # image (these should also have NAXIS=2 in the header). Everything
        # else should be "cube" with NAXIS=3.
        data_product_type = DataProductType.IMAGE

    calibration_level = CalibrationLevel.PRODUCT
    if len(storage_name.product_id.split('_')) == 3:
        calibration_level = CalibrationLevel.CALIBRATED

    bp.set('Plane.calibrationLevel', calibration_level)
    bp.set('Plane.dataProductType', data_product_type)
    bp.clear('Plane.dataRelease')
    bp.add_fits_attribute('Plane.dataRelease', 'DATE')
    bp.clear('Plane.metaRelease')
    bp.add_fits_attribute('Plane.metaRelease', 'DATE')

    artifact_product_type = ProductType.SCIENCE
    if 'noise' in uri:
        artifact_product_type = ProductType.NOISE
    elif storage_name.is_x() or storage_name.is_error():
        artifact_product_type = ProductType.AUXILIARY
    bp.set('Artifact.productType', artifact_product_type)

    # chunk level
    # position
    bp.clear('Chunk.position.axis.function.cd11')
    bp.clear('Chunk.position.axis.function.cd22')
    bp.add_fits_attribute('Chunk.position.axis.function.cd11', 'CDELT1')
    bp.set('Chunk.position.axis.function.cd12', 0.0)
    bp.set('Chunk.position.axis.function.cd21', 0.0)
    bp.add_fits_attribute('Chunk.position.axis.function.cd22', 'CDELT2')
    bp.set('Chunk.position.resolution', '_get_position_resolution(header)')

    # energy
    bp.clear('Chunk.energy.transition.species')
    bp.add_fits_attribute('Chunk.energy.transition.species', 'MOLECULE')
    bp.clear('Chunk.energy.transition.transition')
    bp.add_fits_attribute('Chunk.energy.transition.transition', 'TRANSITI')

    # observable
    if (
        artifact_product_type in [ProductType.SCIENCE, ProductType.NOISE]
        or storage_name.is_error()  # some auxiliary Artifacts have observables
    ):
        bp.configure_observable_axis(4)
        bp.set(
            'Chunk.observable.dependent.axis.ctype',
            '_get_chunk_observable_ctype(header)',
        )
        bp.clear('Chunk.observable.dependent.axis.cunit')
        bp.add_fits_attribute('Chunk.observable.dependent.axis.cunit', 'BUNIT')
        bp.set('Chunk.observable.dependent.bin', 1)
    logging.debug('Done accumulate_bp.')


def update(observation, **kwargs):
    """Called to fill multiple CAOM model elements and/or attributes (an n:n
    relationship between TDM attributes and CAOM attributes). Must have this
    signature for import_module loading and execution.

    :param observation A CAOM Observation model instance.
    :param **kwargs Everything else."""
    logging.debug('Begin update.')
    mc.check_param(observation, Observation)

    headers = kwargs.get('headers')
    fqn = kwargs.get('fqn')
    uri = kwargs.get('uri')
    phangs_name = None
    if uri is not None:
        phangs_name = PHANGSName(artifact_uri=uri)
    if fqn is not None:
        phangs_name = PHANGSName(file_name=os.path.basename(fqn))
    if phangs_name is None:
        raise mc.CadcException(
            f'Need one of fqn or uri defined for '
            f'{observation.observation_id}'
        )

    _update_from_comment(observation, phangs_name, headers)
    for plane in observation.planes.values():
        if plane.product_id != phangs_name.product_id:
            continue
        _update_plane_provenance(
            plane, observation.observation_id, phangs_name
        )
    logging.debug('Done update.')
    return observation


def _build_blueprints(uris):
    """This application relies on the caom2utils fits2caom2 ObsBlueprint
    definition for mapping FITS file values to CAOM model element
    attributes. This method builds the DRAO-ST blueprint for a single
    artifact.

    The blueprint handles the mapping of values with cardinality of 1:1
    between the blueprint entries and the model attributes.

    :param uris The artifact URIs for the files to be processed."""
    module = importlib.import_module(__name__)
    blueprints = {}
    for uri in uris:
        blueprint = ObsBlueprint(module=module)
        if not mc.StorageName.is_preview(uri):
            accumulate_bp(blueprint, uri)
        blueprints[uri] = blueprint
    return blueprints


def _get_chunk_observable_ctype(header):
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
    btype = header.get('BTYPE')
    corrected = btype_fix.get(btype, btype)
    return corrected


def _get_position_resolution(header):
    bmaj = header.get('BMAJ')
    bmin = header.get('BMIN')
    # From
    # https://open-confluence.nrao.edu/pages/viewpage.action?pageId=13697486
    # Clare Chandler via JJK - 21-08-18
    result = None
    if bmaj is not None and bmin is not None:
        result = 3600.0 * sqrt(bmaj * bmin)
    return result


def _get_uris(args):
    result = []
    if args.lineage:
        for ii in args.lineage:
            ignore_product_id, uri = mc.decompose_lineage(ii)
            result.append(uri)
    elif args.local:
        for ii in args.local:
            file_id = mc.StorageName.remove_extensions(os.path.basename(ii))
            file_name = f'{file_id}.fits'
            result.append(PHANGSName(file_name=file_name).file_uri)
    else:
        raise mc.CadcException(f'Could not define uri from these args {args}')
    return result


def _update_from_comment(observation, phangs_name, headers):
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
    for plane in observation.planes.values():
        if plane.product_id != phangs_name.product_id:
            continue
        if plane.provenance is None:
            plane.provenance = Provenance(name='PHANGS-ALMA pipeline')

        for artifact in plane.artifacts.values():
            if artifact.uri != phangs_name.file_uri.replace('.header', ''):
                continue
            for part in artifact.parts.values():
                chunk = part.chunks[0]
                break

        for entry in headers[0].get('COMMENT'):
            if 'pipeline version ' in entry:
                plane.provenance.version = entry.split(' version ')[1]
            elif 'PHANGS-ALMA Public Release' in entry:
                plane.provenance.project = 'PHANGS-ALMA'
            elif 'in nearby GalaxieS (PHANGS) collaboration' in entry:
                plane.provenance.organization = 'PHANGS'
            elif 'Release generated at ' in entry:
                plane.provenance.last_executed = mc.make_time_tz(
                    entry.split(' at ')[1]
                )
            elif 'Data from ALMA Proposal ID:' in entry:
                observation.proposal = Proposal(entry.split(':')[1].strip())
            elif 'Canonical Reference: ' in entry:
                plane.provenance.producer = entry.split(': ')[1]
            elif 'ALMA Proposal PI:' in entry:
                observation.proposal.pi_name = entry.split(': ')[1]
            elif 'Observed in MJD interval ' in entry:
                if chunk is not None:
                    bits = entry.split()[4].split(',')
                    chunk.time = cc.build_temporal_wcs_append_sample(
                        chunk.time,
                        lower=mc.to_float(bits[0].replace('[', '')),
                        upper=mc.to_float(bits[1].replace(']', '')),
                    )


def _update_plane_provenance(plane, obs_id, phangs_name):
    logging.debug(f'Begin _update_plane_provenance for {plane.product_id}')
    if (
        plane.provenance is not None
        and plane.calibration_level == CalibrationLevel.PRODUCT
    ):
        bits = phangs_name.file_name.split('_')
        # file id                               prov id
        #
        index_length = 4
        if len(bits) < 6:
            index_length = 3
        prov_prod_id = '_'.join(ii for ii in bits[:index_length])
        obs_member_uri_ignore, plane_uri = cc.make_plane_uri(
            obs_id, prov_prod_id, COLLECTION
        )
        plane.provenance.inputs.add(plane_uri)
    logging.debug(f'End _update_plane_provenance')


def to_caom2():
    """This function is called by pipeline execution. It must have this name."""
    args = get_gen_proc_arg_parser().parse_args()
    uris = _get_uris(args)
    blueprints = _build_blueprints(uris)
    result = gen_proc(args, blueprints)
    logging.debug(f'Done {APPLICATION} processing.')
    return result


def phangs_main_app():
    args = get_gen_proc_arg_parser().parse_args()
    try:
        result = to_caom2()
        sys.exit(result)
    except Exception as e:
        logging.error(f'Failed {APPLICATION} execution for {args}.')
        tb = traceback.format_exc()
        logging.debug(tb)
        sys.exit(-1)
