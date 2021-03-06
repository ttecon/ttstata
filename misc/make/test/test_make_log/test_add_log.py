#! /usr/bin/env python

import unittest
import sys
import os
import shutil
sys.path.insert(0, os.path.abspath("../.."))
from make.py.make_log import start_make_logging, add_log
from make.py.dir_mod import clear_output_dirs
from make.py.private.exceptionclasses import CritError
import make.py.private.messages as messages
from nostderrout import nostderrout


class testAddLog(unittest.TestCase):

    def setUp(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)

    def test_add(self):
        add_one = 'Added line 1'
        add_one_file = '../output/add1.txt'
        outfile = open(add_one_file, 'w')
        outfile.write(''.join(add_one))
        outfile.close()
        add_two = 'Added line 2'
        add_two_file = '../output/add2.txt'
        outfile = open(add_two_file, 'w')
        outfile.write(''.join(add_two))
        outfile.close()
        with nostderrout():
            add_log(add_one_file, add_two_file, makelog='../output/make.log')
        logfile_data = open('../output/make.log', 'r').readlines()
        self.assertIn('Added line 1', logfile_data[-2])
        self.assertIn('Added line 2', logfile_data[-1])

    def test_nofile(self):
        self.assertFalse(os.path.isfile('../output/add1.txt'))
        with nostderrout():
            add_log('../output/add1.txt', makelog='../output/make.log')
        logfile_data = open('../output/make.log', 'r').read()
        message = messages.note_nofile % '../output/add1.txt'
        self.assertIn(message, logfile_data)

    def test_nolog(self):
        add_one = 'Added line 1 \n'
        add_one_file = '../output/add1.txt'
        outfile = open(add_one_file, 'w')
        outfile.write(''.join(add_one))
        outfile.close()
        os.remove('../output/make.log')
        with nostderrout():
            with self.assertRaises(CritError):
                add_log('../output/add1.txt', makelog='../output/make.log')

    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')


if __name__ == '__main__':
    os.getcwd()
    unittest.main()
