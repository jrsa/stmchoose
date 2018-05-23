import xml.etree.ElementTree
import re
import glob

from os.path import exists

"""
dependent on https://github.com/esden/stm32cube-database, pass the path to it
during construction of objects of the class below 
"""

PIN_LIST_ATTRS = ['Position', 'Name', 'Type']

def pin_tree_to_list(pin_tree_entries):
    return [[p.attrib[a] for a in PIN_LIST_ATTRS] for p in pin_tree_entries]

def pin_tree_to_list_with_signals(pin_tree_entries):
    return [([p.attrib[a] for a in PIN_LIST_ATTRS], set([s.attrib["Name"] for s in p.findall("Signal")])) for p in pin_tree_entries]


class Stm32Chooser(object):
    def __init__(self, fn):
        self.database_dir = fn

    def enum_xmlfiles(self):
        return sorted(glob.glob(self.database_dir + "/STM32*.xml"))

    def filename_for_part(self, part):
        path = self.database_dir + "/STM32{}.xml".format(part)
        if exists(path):
            return path

    def tree_for_filename(self, fn):
        data = None
        try:
            with open(fn) as f:
                data = f.read()
                f.close()
        except:
            print("failed opening {}".format(fn))
            return
        data = re.sub(' xmlns="[^"]+"', '', data, count=1)
        tree = None
        try:
            tree = xml.etree.ElementTree.fromstring(data)
        except:
            print("parse failed")
            return

        return tree

    def pinlist_for_part(self, part):
        fn = self.filename_for_part(part)
        mcu_tree = self.tree_for_filename(fn)
        pin_tree = mcu_tree.findall("Pin")
        return pin_tree_to_list(pin_tree)

    def pinlist_for_part_with_signals(self, part):
        fn = self.filename_for_part(part)
        mcu_tree = self.tree_for_filename(fn)
        pin_tree = mcu_tree.findall("Pin")
        return pin_tree_to_list_with_signals(pin_tree)