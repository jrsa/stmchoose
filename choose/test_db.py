import unittest
from os import path

import xml.etree.ElementTree

from . import db

class TestCubeDatabase(unittest.TestCase):

    def setUp(self):
        self.database = db.CubeDatabase()

    def test_database_dir_present(self):
        self.assertIsInstance(self.database.database_dir, str)
        self.assertTrue(path.exists(self.database.database_dir))

    def test_enum_xmlfiles(self):
        """
        the enum_xmlfiles method should return an array of some xml filenames
        """
        self.assertIsInstance(self.database.enum_xmlfiles(), list)
        self.assertNotEqual(len(self.database.enum_xmlfiles()), 0)

    def test_all_partnumbers(self):
        """
        the all_partnumbers method should return an array of some part numbers
        """
        all_partnumbers = self.database.all_partnumbers()

        self.assertIsInstance(all_partnumbers, list)
        self.assertNotEqual(len(all_partnumbers), 0)

        for e in all_partnumbers:
            self.assertIsInstance(e, db.Pn)

    def test_filename_for_part(self):
        for pn in ('F469ZIT', 'F722ZET'):
            fn = self.database.filename_for_part(pn)
            self.assertIsInstance(fn, str)
            self.assertTrue(path.exists(fn))

        with self.assertRaisesRegex(RuntimeError, 'not found'):
            self.database.filename_for_part("partnumber_that_doesnt_Exist")

    def test_tree_for_filename(self):
        filename = path.join(self.database.database_dir, "STM32F405RGTx.xml")
        self.assertTrue(path.exists(filename))

        tree = self.database.tree_for_filename(filename)
        self.assertIsInstance(tree, xml.etree.ElementTree.Element)

        with self.assertRaises(FileNotFoundError):
            self.database.tree_for_filename("bad_filename")

    def test_pindesc_for_part(self):
        pd = self.database.pindesc_for_part('F779NIH')
        self.assertIsInstance(pd, dict)

        for k in pd:
            self.assertIsInstance(pd[k], db.PinDesc)

if __name__ == '__main__':
    unittest.main()