# -*- coding: utf-8 -*-
# ***********************************************************************
# ******************  CANADIAN ASTRONOMY DATA CENTRE  *******************
# *************  CENTRE CANADIEN DE DONNÉES ASTRONOMIQUES  **************
#
#  (c) 2019.                            (c) 2019.
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

from mock import patch

from phangs2caom2 import main_app, APPLICATION, COLLECTION, PHANGSName
from phangs2caom2 import ARCHIVE
from caom2pipe import manage_composable as mc

import logging
import os
import sys
import traceback

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA_DIR = os.path.join(THIS_DIR, 'data')
PLUGIN = os.path.join(os.path.dirname(THIS_DIR), 'main_app.py')

LOOKUP = {
    'ngc2903_12m+7m+tp_co21': [
        'ngc2903_12m+7m+tp_co21.fits.header',
        'ngc2903_12m+7m+tp_co21_broadmask.fits.header',
        'ngc2903_12m+7m+tp_co21_2as.fits.header',
        'ngc2903_12m+7m+tp_co21_noise.fits.header',
        'ngc2903_12m+7m+tp_co21_2as_broad_emom0.fits.header',
        'ngc2903_12m+7m+tp_co21_strict_eew.fits.header',
        'ngc2903_12m+7m+tp_co21_2as_broad_mom0.fits.header',
        'ngc2903_12m+7m+tp_co21_strict_emom0.fits.header',
        'ngc2903_12m+7m+tp_co21_2as_broad_tpeak.fits.header',
        'ngc2903_12m+7m+tp_co21_strict_emom1.fits.header',
        'ngc2903_12m+7m+tp_co21_2as_coverage.fits.header',
        'ngc2903_12m+7m+tp_co21_strict_emom2.fits.header',
        'ngc2903_12m+7m+tp_co21_2as_noise.fits.header',
        'ngc2903_12m+7m+tp_co21_strict_ew.fits.header',
        'ngc2903_12m+7m+tp_co21_2as_strict_eew.fits.header',
        'ngc2903_12m+7m+tp_co21_strict_mom0.fits.header',
        'ngc2903_12m+7m+tp_co21_2as_strict_emom0.fits.header',
        'ngc2903_12m+7m+tp_co21_strict_mom1.fits.header',
        'ngc2903_12m+7m+tp_co21_2as_strict_emom1.fits.header',
        'ngc2903_12m+7m+tp_co21_strict_mom2.fits.header',
        'ngc2903_12m+7m+tp_co21_2as_strict_emom2.fits.header',
        'ngc2903_12m+7m+tp_co21_strictmask.fits.header',
        'ngc2903_12m+7m+tp_co21_2as_strict_ew.fits.header',
        'ngc2903_12m+7m+tp_co21_2as_strict_mom0.fits.header',
        'ngc2903_12m+7m+tp_co21_2as_strict_mom1.fits.header',
        'ngc2903_12m+7m+tp_co21_2as_strict_mom2.fits.header',
        'ngc2903_12m+7m+tp_co21_2as_strictmask.fits.header',
        'ngc2903_12m+7m+tp_co21_broad_emom0.fits.header',
        'ngc2903_12m+7m+tp_co21_broad_mom0.fits.header',
        'ngc2903_12m+7m+tp_co21_broad_tpeak.fits.header',
    ],
    'ngc2903_7m+tp_co21': [
        'ngc2903_7m+tp_co21_11as_strict_emom0.fits.header',
        'ngc2903_7m+tp_co21_15as_strict_mom0.fits.header',
        'ngc2903_7m+tp_co21_11as_strict_emom1.fits.header',
        'ngc2903_7m+tp_co21_15as_strict_mom1.fits.header',
        'ngc2903_7m+tp_co21_11as_strict_emom2.fits.header',
        'ngc2903_7m+tp_co21_15as_strict_mom2.fits.header',
        'ngc2903_7m+tp_co21_11as_strict_ew.fits.header',
        'ngc2903_7m+tp_co21_15as_strictmask.fits.header',
        'ngc2903_7m+tp_co21_11as_strict_mom0.fits.header',
        'ngc2903_7m+tp_co21_broad_emom0.fits.header',
        'ngc2903_7m+tp_co21_11as_strict_mom1.fits.header',
        'ngc2903_7m+tp_co21_broad_mom0.fits.header',
        'ngc2903_7m+tp_co21_11as_strict_mom2.fits.header',
        'ngc2903_7m+tp_co21_broad_tpeak.fits.header',
        'ngc2903_7m+tp_co21_11as_strictmask.fits.header',
        'ngc2903_7m+tp_co21_broadmask.fits.header',
        'ngc2903_7m+tp_co21_15as.fits.header',
        'ngc2903_7m+tp_co21_noise.fits.header',
        'ngc2903_7m+tp_co21_15as_broad_emom0.fits.header',
        'ngc2903_7m+tp_co21_strict_eew.fits.header',
        'ngc2903_7m+tp_co21_15as_broad_mom0.fits.header',
        'ngc2903_7m+tp_co21_strict_emom0.fits.header',
        'ngc2903_7m+tp_co21.fits.header',
        'ngc2903_7m+tp_co21_15as_broad_tpeak.fits.header',
        'ngc2903_7m+tp_co21_strict_emom1.fits.header',
        'ngc2903_7m+tp_co21_11as.fits.header',
        'ngc2903_7m+tp_co21_15as_coverage.fits.header',
        'ngc2903_7m+tp_co21_strict_emom2.fits.header',
        'ngc2903_7m+tp_co21_11as_broad_emom0.fits.header',
        'ngc2903_7m+tp_co21_15as_noise.fits.header',
        'ngc2903_7m+tp_co21_strict_ew.fits.header',
        'ngc2903_7m+tp_co21_11as_broad_mom0.fits.header',
        'ngc2903_7m+tp_co21_15as_strict_eew.fits.header',
        'ngc2903_7m+tp_co21_strict_mom0.fits.header',
        'ngc2903_7m+tp_co21_11as_broad_tpeak.fits.header',
        'ngc2903_7m+tp_co21_15as_strict_emom0.fits.header',
        'ngc2903_7m+tp_co21_strict_mom1.fits.header',
        'ngc2903_7m+tp_co21_11as_coverage.fits.header',
        'ngc2903_7m+tp_co21_15as_strict_emom1.fits.header',
        'ngc2903_7m+tp_co21_strict_mom2.fits.header',
        'ngc2903_7m+tp_co21_11as_noise.fits.header',
        'ngc2903_7m+tp_co21_15as_strict_emom2.fits.header',
        'ngc2903_7m+tp_co21_strictmask.fits.header',
        'ngc2903_7m+tp_co21_11as_strict_eew.fits.header',
        'ngc2903_7m+tp_co21_15as_strict_ew.fits.header',
    ],
}


def pytest_generate_tests(metafunc):
    metafunc.parametrize('test_name', LOOKUP.keys())


@patch('caom2utils.fits2caom2.CadcDataClient')
def test_main_app(data_client_mock, test_name):
    obs_path = f'{TEST_DATA_DIR}/{test_name}.expected.xml'
    output_file = f'{TEST_DATA_DIR}/{test_name}.actual.xml'
    local = _get_local(test_name)
    lineage = _get_lineage(test_name)

    if os.path.exists(output_file):
        os.unlink(output_file)

    data_client_mock.return_value.get_file_info.side_effect = _get_file_info

    sys.argv = (
        f'{APPLICATION} --no_validate --local {local} --observation '
        f'{COLLECTION} {test_name} -o {output_file} --plugin {PLUGIN} '
        f'--module {PLUGIN} --lineage {lineage}'
    ).split()
    try:
        main_app.to_caom2()
    except Exception as e:
        logging.error(traceback.format_exc())

    compare_result = mc.compare_observations(output_file, obs_path)
    if compare_result is not None:
        raise AssertionError(compare_result)
    # assert False  # cause I want to see logging messages


def _get_file_info(archive, file_id):
    return {'type': 'application/fits'}


def _get_lineage(obs_id):
    result = ''
    for ii in LOOKUP[obs_id]:
        storage_name = PHANGSName(file_name=ii)
        fits = mc.get_lineage(ARCHIVE, storage_name.product_id, ii).replace(
            '.header', ''
        )
        result = f'{result } {fits}'
    return result


def _get_local(obs_id):
    result = ''
    for ii in LOOKUP[obs_id]:
        result = f'{result} {TEST_DATA_DIR}/{ii}'
    return result
