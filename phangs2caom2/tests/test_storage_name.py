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
from phangs2caom2 import PHANGSName


def test_is_valid():
    assert PHANGSName(
        file_name='ngc2903_12m+7m+tp_co21_2as_broad_emom0.fits'
    ).is_valid()


def test_bits():
    test_obs1 = 'ngc2903_12m+7m+tp_co21'
    test_obs2 = 'ngc2903_7m+tp_co21'
    answer = {
        'ngc2903_12m+7m+tp_co21': [test_obs1, test_obs1],
        'ngc2903_12m+7m+tp_co21_strict_ew': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_strict_ew',
        ],
        'ngc2903_7m+tp_co21_15as_coverage': [
            test_obs2,
            'ngc2903_7m+tp_co21_15as',
        ],
        'ngc2903_12m+7m+tp_co21_2as': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_2as',
        ],
        'ngc2903_12m+7m+tp_co21_strict_mom0': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_strict_mom0',
        ],
        'ngc2903_7m+tp_co21_15as_noise': [
            test_obs2,
            'ngc2903_7m+tp_co21_15as',
        ],
        'ngc2903_12m+7m+tp_co21_2as_broad_emom0': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_2as_broad_mom0',
        ],
        'ngc2903_12m+7m+tp_co21_strict_mom1': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_strict_mom1',
        ],
        'ngc2903_7m+tp_co21_15as_strict_eew': [
            test_obs2,
            'ngc2903_7m+tp_co21_15as_strict_ew',
        ],
        'ngc2903_12m+7m+tp_co21_2as_broad_mom0': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_2as_broad_mom0',
        ],
        'ngc2903_12m+7m+tp_co21_strict_mom2': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_strict_mom2',
        ],
        'ngc2903_7m+tp_co21_15as_strict_emom0': [
            test_obs2,
            'ngc2903_7m+tp_co21_15as_strict_mom0',
        ],
        'ngc2903_12m+7m+tp_co21_2as_broad_tpeak': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_2as_broad_tpeak',
        ],
        'ngc2903_12m+7m+tp_co21_strictmask': [test_obs1, test_obs1],
        'ngc2903_7m+tp_co21_15as_strict_emom1': [
            test_obs2,
            'ngc2903_7m+tp_co21_15as_strict_mom1',
        ],
        'ngc2903_12m+7m+tp_co21_2as_coverage': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_2as',
        ],
        'ngc2903_7m+tp_co21': [test_obs2, test_obs2],
        'ngc2903_7m+tp_co21_15as_strict_emom2': [
            test_obs2,
            'ngc2903_7m+tp_co21_15as_strict_mom2',
        ],
        'ngc2903_12m+7m+tp_co21_2as_noise': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_2as',
        ],
        'ngc2903_7m+tp_co21_11as': [test_obs2, 'ngc2903_7m+tp_co21_11as'],
        'ngc2903_7m+tp_co21_15as_strict_ew': [
            test_obs2,
            'ngc2903_7m+tp_co21_15as_strict_ew',
        ],
        'ngc2903_12m+7m+tp_co21_2as_strict_eew': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_2as_strict_ew',
        ],
        'ngc2903_7m+tp_co21_11as_broad_emom0': [
            test_obs2,
            'ngc2903_7m+tp_co21_11as_broad_mom0',
        ],
        'ngc2903_7m+tp_co21_15as_strict_mom0': [
            test_obs2,
            'ngc2903_7m+tp_co21_15as_strict_mom0',
        ],
        'ngc2903_12m+7m+tp_co21_2as_strict_emom0': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_2as_strict_mom0',
        ],
        'ngc2903_7m+tp_co21_11as_broad_mom0': [
            test_obs2,
            'ngc2903_7m+tp_co21_11as_broad_mom0',
        ],
        'ngc2903_7m+tp_co21_15as_strict_mom1': [
            test_obs2,
            'ngc2903_7m+tp_co21_15as_strict_mom1',
        ],
        'ngc2903_12m+7m+tp_co21_2as_strict_emom1': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_2as_strict_mom1',
        ],
        'ngc2903_7m+tp_co21_11as_broad_tpeak': [
            test_obs2,
            'ngc2903_7m+tp_co21_11as_broad_tpeak',
        ],
        'ngc2903_7m+tp_co21_15as_strict_mom2': [
            test_obs2,
            'ngc2903_7m+tp_co21_15as_strict_mom2',
        ],
        'ngc2903_12m+7m+tp_co21_2as_strict_emom2': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_2as_strict_mom2',
        ],
        'ngc2903_7m+tp_co21_11as_coverage': [
            test_obs2,
            'ngc2903_7m+tp_co21_11as',
        ],
        'ngc2903_7m+tp_co21_15as_strictmask': [
            test_obs2,
            'ngc2903_7m+tp_co21_15as',
        ],
        'ngc2903_12m+7m+tp_co21_2as_strict_ew': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_2as_strict_ew',
        ],
        'ngc2903_7m+tp_co21_11as_noise': [
            test_obs2,
            'ngc2903_7m+tp_co21_11as',
        ],
        'ngc2903_7m+tp_co21_broad_emom0': [
            test_obs2,
            'ngc2903_7m+tp_co21_broad_mom0',
        ],
        'ngc2903_12m+7m+tp_co21_2as_strict_mom0': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_2as_strict_mom0',
        ],
        'ngc2903_7m+tp_co21_11as_strict_eew': [
            test_obs2,
            'ngc2903_7m+tp_co21_11as_strict_ew',
        ],
        'ngc2903_7m+tp_co21_broad_mom0': [
            test_obs2,
            'ngc2903_7m+tp_co21_broad_mom0',
        ],
        'ngc2903_12m+7m+tp_co21_2as_strict_mom1': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_2as_strict_mom1',
        ],
        'ngc2903_7m+tp_co21_11as_strict_emom0': [
            test_obs2,
            'ngc2903_7m+tp_co21_11as_strict_mom0',
        ],
        'ngc2903_7m+tp_co21_broad_tpeak': [
            test_obs2,
            'ngc2903_7m+tp_co21_broad_tpeak',
        ],
        'ngc2903_12m+7m+tp_co21_2as_strict_mom2': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_2as_strict_mom2',
        ],
        'ngc2903_7m+tp_co21_11as_strict_emom1': [
            test_obs2,
            'ngc2903_7m+tp_co21_11as_strict_mom1',
        ],
        'ngc2903_7m+tp_co21_broadmask': [test_obs2, test_obs2],
        'ngc2903_12m+7m+tp_co21_2as_strictmask': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_2as',
        ],
        'ngc2903_7m+tp_co21_11as_strict_emom2': [
            test_obs2,
            'ngc2903_7m+tp_co21_11as_strict_mom2',
        ],
        'ngc2903_7m+tp_co21_noise': [test_obs2, 'ngc2903_7m+tp_co21'],
        'ngc2903_12m+7m+tp_co21_broad_emom0': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_broad_mom0',
        ],
        'ngc2903_7m+tp_co21_11as_strict_ew': [
            test_obs2,
            'ngc2903_7m+tp_co21_11as_strict_ew',
        ],
        'ngc2903_7m+tp_co21_strict_eew': [
            test_obs2,
            'ngc2903_7m+tp_co21_strict_ew',
        ],
        'ngc2903_12m+7m+tp_co21_broad_mom0': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_broad_mom0',
        ],
        'ngc2903_7m+tp_co21_11as_strict_mom0': [
            test_obs2,
            'ngc2903_7m+tp_co21_11as_strict_mom0',
        ],
        'ngc2903_7m+tp_co21_strict_emom0': [
            test_obs2,
            'ngc2903_7m+tp_co21_strict_mom0',
        ],
        'ngc2903_12m+7m+tp_co21_broad_tpeak': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_broad_tpeak',
        ],
        'ngc2903_7m+tp_co21_11as_strict_mom1': [
            test_obs2,
            'ngc2903_7m+tp_co21_11as_strict_mom1',
        ],
        'ngc2903_7m+tp_co21_strict_emom1': [
            test_obs2,
            'ngc2903_7m+tp_co21_strict_mom1',
        ],
        'ngc2903_12m+7m+tp_co21_broadmask': [test_obs1, test_obs1],
        'ngc2903_7m+tp_co21_11as_strict_mom2': [
            test_obs2,
            'ngc2903_7m+tp_co21_11as_strict_mom2',
        ],
        'ngc2903_7m+tp_co21_strict_emom2': [
            test_obs2,
            'ngc2903_7m+tp_co21_strict_mom2',
        ],
        'ngc2903_12m+7m+tp_co21_noise': [test_obs1, 'ngc2903_12m+7m+tp_co21'],
        'ngc2903_7m+tp_co21_11as_strictmask': [
            test_obs2,
            'ngc2903_7m+tp_co21_11as',
        ],
        'ngc2903_7m+tp_co21_strict_ew': [
            test_obs2,
            'ngc2903_7m+tp_co21_strict_ew',
        ],
        'ngc2903_12m+7m+tp_co21_strict_eew': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_strict_ew',
        ],
        'ngc2903_7m+tp_co21_15as': [test_obs2, 'ngc2903_7m+tp_co21_15as'],
        'ngc2903_7m+tp_co21_strict_mom0': [
            test_obs2,
            'ngc2903_7m+tp_co21_strict_mom0',
        ],
        'ngc2903_12m+7m+tp_co21_strict_emom0': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_strict_mom0',
        ],
        'ngc2903_7m+tp_co21_15as_broad_emom0': [
            test_obs2,
            'ngc2903_7m+tp_co21_15as_broad_mom0',
        ],
        'ngc2903_7m+tp_co21_strict_mom1': [
            test_obs2,
            'ngc2903_7m+tp_co21_strict_mom1',
        ],
        'ngc2903_12m+7m+tp_co21_strict_emom1': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_strict_mom1',
        ],
        'ngc2903_7m+tp_co21_15as_broad_mom0': [
            test_obs2,
            'ngc2903_7m+tp_co21_15as_broad_mom0',
        ],
        'ngc2903_7m+tp_co21_strict_mom2': [
            test_obs2,
            'ngc2903_7m+tp_co21_strict_mom2',
        ],
        'ngc2903_12m+7m+tp_co21_strict_emom2': [
            test_obs1,
            'ngc2903_12m+7m+tp_co21_strict_mom2',
        ],
        'ngc2903_7m+tp_co21_15as_broad_tpeak': [
            test_obs2,
            'ngc2903_7m+tp_co21_15as_broad_tpeak',
        ],
        'ngc2903_7m+tp_co21_strictmask': [test_obs2, test_obs2],
    }

    for f_name, answer in answer.items():
        test_subject = PHANGSName(file_name=f_name)
        assert test_subject.obs_id == answer[0], f'wrong obs_id for {f_name}'
        assert (
            test_subject.target_name == 'ngc2903'
        ), f'wrong target name for {f_name}'
        if len(answer) > 1:
            assert (
                test_subject.product_id == answer[1]
            ), f'wrong product_id for {f_name}'
