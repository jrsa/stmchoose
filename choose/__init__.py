import xml.etree.ElementTree
import re
import glob
from collections import namedtuple
import os.path

"""
dependent on https://github.com/esden/stm32cube-database, pass the path to it
during construction of objects of the class below 
"""

# source: various STM32 datasheets
PACKAGES = {
    'T' : 'LQFP',
    'K' : 'UFBGA',
    'H' : 'TFBGA',
    'Y' : 'WLCSP',
}

Pn = namedtuple('Pn', ['family', 'subtype', 'pincount', 'flashsize', 'package'])
def split_pn(pn):
    if pn[5] == '(':
        closing_paren = pn.index(')')
        return (pn[:2], pn[2:4], pn[4:5], pn[6:closing_paren].split("-"), pn[closing_paren+1:closing_paren+2] )
    else:
        return (pn[:2], pn[2:4], pn[4:5], pn[5:6], pn[6:7])

PinDesc = namedtuple('PinDesc', ['name', 'type', 'signals'])

PIN_LIST_ATTRS = ['Position', 'Name', 'Type']

def pin_tree_to_list(pin_tree_entries):
    return {int(p.attrib["Position"]) : [p.attrib["Name"], p.attrib["Type"]] for p in pin_tree_entries}

def pin_tree_to_list_with_signals(pin_tree_entries):
    return {int(p.attrib['Position']) : (p.attrib['Name'], p.attrib['Type'], set([s.attrib["Name"] for s in p.findall("Signal")])) for p in pin_tree_entries}

def pin_tree_to_descs(pin_tree_entries):
    return {int(p.attrib['Position']) : PinDesc(p.attrib['Name'], p.attrib['Type'], set([s.attrib["Name"] for s in p.findall("Signal")])) for p in pin_tree_entries}

class Stm32Chooser(object):
    def __init__(self, fn):
        self.database_dir = fn

    def enum_xmlfiles(self):
        return sorted(glob.glob(self.database_dir + "/STM32*.xml"))

    def filename_for_part(self, part):
        search_pn = Pn(*split_pn(part))

        if search_pn.package in ['K', 'H', 'Y']:
            raise RuntimeError("BGA packages not supported yet, asked for package type {} ({})".format(search_pn.package, PACKAGES[search_pn.package]))

        path = self.database_dir + "/STM32{}.xml".format(part)
        if os.path.exists(path):
            return path

        # see if the part is covered by a file with a (a-b) expression in the filename

        part_glob_expr = "".join(["STM32", part[:5], "*.xml"])
        part_glob = glob.glob(self.database_dir + part_glob_expr)

        if len(part_glob) == 1:
            pn_string = os.path.basename(part_glob[0])[5:-4]
            base_pn = Pn(*split_pn(pn_string))
            if search_pn.flashsize in base_pn.flashsize and search_pn.package == base_pn.package:
                return part_glob[0]

        else:
            for g in part_glob:
                pn_string = os.path.basename(g)[5:-4]
                base_pn = Pn(*split_pn(pn_string))

                if search_pn.flashsize in base_pn.flashsize and search_pn.package == base_pn.package:
                    return g

        raise RuntimeError("{} not found dog".format(search_pn))

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
        print("loading pin info from {}".format(fn))
        mcu_tree = self.tree_for_filename(fn)
        pin_tree = mcu_tree.findall("Pin")
        return pin_tree_to_list(pin_tree)

    def pinlist_for_part_with_signals(self, part):
        fn = self.filename_for_part(part)
        print("loading pin info from {}".format(fn))
        mcu_tree = self.tree_for_filename(fn)
        pin_tree = mcu_tree.findall("Pin")
        return pin_tree_to_list_with_signals(pin_tree)

    def pindesc_for_part(self, part):
        fn = self.filename_for_part(part)
        print("loading pin info from {}".format(fn))
        mcu_tree = self.tree_for_filename(fn)
        pin_tree = mcu_tree.findall("Pin")
        return pin_tree_to_descs(pin_tree)

