#! /usr/bin/env python

import unittest
import sys
import os
import shutil
sys.path.insert(0, os.path.abspath("../.."))
from make.py.make_log import start_make_logging
from make.py.dir_mod import clear_output_dirs
from make.py.run_program import run_rbatch
from nostderrout import nostderrout


class testRunRBatch(unittest.TestCase):

    def setUp(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_rbatch(program='./input/R_test_script.r')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('Test script complete', logfile_data)
        self.assertIn('> proc.time()', logfile_data)
        self.assertIn('Time   : ', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))

    def test_custom_log(self):
        os.remove('../output/make.log')
        makelog_file = '../output/custom_make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)
            run_rbatch(program='./input/R_test_script.R',
                       makelog='../output/custom_make.log')
        logfile_data = open('../output/custom_make.log', 'r').read()
        self.assertIn('Test script complete', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))

    def test_independent_log(self):
        with nostderrout():
            run_rbatch(program='./input/R_test_script.R',
                       log='../output/R.log')
        makelog_data = open('../output/make.log', 'r').read()
        self.assertIn('Test script complete', makelog_data)
        self.assertTrue(os.path.isfile('../output/R.log'))
        Rlog_data = open('../output/R.log', 'r').read()
        self.assertIn('Test script complete', Rlog_data)
        self.assertTrue(os.path.isfile('output.txt'))

    def test_no_extension(self):
        with nostderrout():
            run_rbatch(program='./input/R_test_script')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('Test script complete', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))

    def test_executable(self):
        with nostderrout():
            run_rbatch(program='./input/R_test_script.R',
                       executable='R CMD BATCH')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('Test script complete', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))

    def test_bad_executable(self):
        with nostderrout():
            run_rbatch(program='./input/R_test_script.R',
                       executable='nonexistent_R_executable')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('executed with errors', logfile_data)

    def test_no_program(self):
        with nostderrout():
            run_rbatch(program='./input/nonexistent_R_script.R')
        logfile_data = open('../output/make.log', 'r').readlines()
        self.assertIn('CritError:', logfile_data[-1])

    def test_option(self):
        with nostderrout():
            run_rbatch(program='./input/R_test_script.R', option='--no-timing')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('Test script complete', logfile_data)
        self.assertIn('R version', logfile_data)
        self.assertNotIn('> proc.time()', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))

    def test_two_option(self):
        with nostderrout():
            run_rbatch(program='./input/R_test_script.R',
                       option='--no-timing --slave')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('Test script complete', logfile_data)
        self.assertNotIn('R version', logfile_data)
        self.assertNotIn('> proc.time()', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))

    def test_rbatch_error(self):
        with nostderrout():
            run_rbatch(program='./input/R_test_script_error.R')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('executed with errors', logfile_data)

    def test_change_dir(self):
        with nostderrout():
            run_rbatch(program='./input/R_test_script.R', changedir=True)
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('Test script complete', logfile_data)
        self.assertIn('> proc.time()', logfile_data)
        self.assertTrue(os.path.isfile('./input/output.txt'))

    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')
        if os.path.isfile('output.txt'):
            os.remove('output.txt')
        if os.path.isfile('./input/output.txt'):
            os.remove('./input/output.txt')
        if os.path.isfile('.RData'):
            os.remove('.RData')


if __name__ == '__main__':
    os.getcwd()
    unittest.main()
