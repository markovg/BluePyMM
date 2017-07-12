"""Tests for select_combos/megate_output"""

from __future__ import print_function

"""
Copyright (c) 2017, EPFL/Blue Brain Project

 This file is part of BluePyMM <https://github.com/BlueBrain/BluePyMM>

 This library is free software; you can redistribute it and/or modify it under
 the terms of the GNU Lesser General Public License version 3.0 as published
 by the Free Software Foundation.

 This library is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
 details.

 You should have received a copy of the GNU Lesser General Public License
 along with this library; if not, write to the Free Software Foundation, Inc.,
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import pandas
import filecmp
import os

from nose.plugins.attrib import attr
import nose.tools as nt

import bluepymm.select_combos as select_combos


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_DATA_DIR = os.path.join(BASE_DIR, 'examples/simple1')
TMP_DIR = os.path.join(BASE_DIR, 'tmp/megate_output')


def _test_save_megate_results(data, sort_key):
    # input parameters
    columns = ['morph_name', 'layer', 'fullmtype', 'etype', 'emodel',
               'combo_name', 'threshold_current', 'holding_current']
    df = pandas.DataFrame(data, columns=columns)
    dat_filename = 'extNeuronDB.dat'
    tsv_filename = 'mecombo_emodel.tsv'
    extneurondbdat = os.path.join(TMP_DIR, dat_filename)
    mecombo_emodel = os.path.join(TMP_DIR, tsv_filename)

    # save_megate_results
    select_combos.megate_output.save_megate_results(df,
                                                    extneurondbdat,
                                                    mecombo_emodel,
                                                    sort_key)

    # verify output files
    benchmark_dir = os.path.join(TEST_DATA_DIR, 'output_megate_expected')
    files = [dat_filename, tsv_filename]
    matches = filecmp.cmpfiles(benchmark_dir, TMP_DIR, files)
    if len(matches[0]) != len(files):
        print('Mismatch in files: {}'.format(matches[1]))
    nt.assert_equal(len(matches[0]), len(files))


@attr('unit')
def test_save_megate_results_no_sort():
    """bluepymm.select_combos: test save_megate_results."""
    data = [('morph1', 1, 'mtype1', 'etype1', 'emodel1',
             'emodel1_mtype1_1_morph1', '', ''),
            ('morph2', 1, 'mtype2', 'etype1', 'emodel1',
             'emodel1_mtype2_1_morph2', '', ''),
            ('morph1', 1, 'mtype1', 'etype2', 'emodel2',
             'emodel2_mtype1_1_morph1', '', '')]
    _test_save_megate_results(data, None)


@attr('unit')
def test_save_megate_results_sort():
    """bluepymm.select_combos: test save_megate_results."""
    data = [('morph1', 1, 'mtype1', 'etype1', 'emodel1',
             'emodel1_mtype1_1_morph1', '', ''),
            ('morph1', 1, 'mtype1', 'etype2', 'emodel2',
             'emodel2_mtype1_1_morph1', '', ''),
            ('morph2', 1, 'mtype2', 'etype1', 'emodel1',
             'emodel1_mtype2_1_morph2', '', '')]
    _test_save_megate_results(data, 'combo_name')