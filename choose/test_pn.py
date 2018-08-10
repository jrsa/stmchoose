import unittest

from . import pn

class TestPn(unittest.TestCase):

    def test_strip(self):
        self.assertEqual(pn.strip('STM32F469NIHx.xml'), 'F469NIHx')
        self.assertEqual(pn.strip('STM32F722Z(C-E)Tx.xml'), 'F722Z(C-E)Tx')

    def test_join(self):
        self.assertEqual(pn.join(pn.Pn('F4', '69', 'N', 'I', 'H')), 'F469NIH')
        self.assertEqual(pn.join(pn.Pn('F7', '22', 'Z', ['C', 'E'], 'T')), 'F722Z(C-E)T')

    def test_split(self):
        self.assertEqual(pn.split('F469NIHx'), ('F4', '69', 'N', 'I', 'H'))
        self.assertEqual(pn.split('F722Z(C-E)T'), ('F7', '22', 'Z', ['C', 'E'], 'T'))
