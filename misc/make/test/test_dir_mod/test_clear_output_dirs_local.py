#! /usr/bin/env python

import unittest
import sys
import os
import shutil
sys.path.insert(0, os.path.abspath("../.."))
from make.py.dir_mod import clear_output_dirs_local
from nostderrout import nostderrout


class testClearOutputDirsLocal(unittest.TestCase):

    def test_default(self):
        self.assertFalse(os.path.exists('../output_local/'))

        with nostderrout():
            clear_output_dirs_local()

        self.assertTrue(os.path.exists('../output_local/'))
        file_list = os.listdir('../output_local/')
        self.assertEqual(len(file_list), 0)

    def test_already_exists(self):
        os.makedirs('./output_local_empty/')

        with nostderrout():
            clear_output_dirs_local('./output_local_empty/')

        self.assertTrue(os.path.exists('./output_local_empty/'))
        file_list = os.listdir('./output_local_empty/')
        self.assertEqual(len(file_list), 0)

    def test_already_exists_with_files(self):
        os.makedirs('./output_local_files/')
        newfile = open('./output_local_files/text.txt', 'w+')
        newfile.write('test')
        newfile.close()
        file_list = os.listdir('./output_local_files/')
        self.assertEqual(len(file_list), 1)

        with nostderrout():
            clear_output_dirs_local('./output_local_files/')

        self.assertTrue(os.path.exists('./output_local_files/'))
        file_list = os.listdir('./output_local_files/')
        self.assertEqual(len(file_list), 0)

    def tearDown(self):
        if os.path.isdir('../output_local/'):
            shutil.rmtree('../output_local/')
        if os.path.isdir('./output_local_empty/'):
            shutil.rmtree('./output_local_empty/')
        if os.path.isdir('./output_local_files/'):
            shutil.rmtree('./output_local_files/')

if __name__ == '__main__':
    os.getcwd()
    unittest.main()
