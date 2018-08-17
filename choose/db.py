import xml.etree.ElementTree
import re
import glob
from collections import namedtuple
from os.path import join, dirname, basename, exists

from . import pn

"""
dependent on https://github.com/esden/stm32cube-database, pass the path to it
during construction of objects of the class below 
"""
DEFAULT_DATABASE_DIR = join(dirname(__file__), "../stm32cube-database/db/mcu/")

PinDesc = namedtuple('PinDesc', ['name', 'type', 'signals'])

class CubeDatabase(object):
    def __init__(self, fn=DEFAULT_DATABASE_DIR):
        self.database_dir = fn

    def enum_xmlfiles(self):
        return sorted(glob.glob(self.database_dir + "/STM32*.xml"))

    def all_partnumbers(self):
        return [pn.Pn(*pn.split(pn.strip(basename(fn))))
                for fn in self.enum_xmlfiles()]

    def filename_for_part(self, part):
        search_pn = pn.Pn(*pn.split(part))

        path = self.database_dir + "/STM32{}.xml".format(part)
        if exists(path):
            return path

        # see if the part is covered by a file with
        # an (a-b) expression in the filename

        part_glob_expr = "".join(["STM32", part[:5], "*.xml"])
        part_glob = glob.glob(self.database_dir + part_glob_expr)

        if len(part_glob) == 1:
            pn_string = pn.strip(basename(part_glob[0]))
            base_pn = pn.Pn(*pn.split(pn_string))
            if (search_pn.flashsize in base_pn.flashsize and
                    search_pn.package == base_pn.package):
                return part_glob[0]

        elif len(part_glob) > 1:
            for g in part_glob:
                pn_string = pn.strip(basename(g))
                base_pn = pn.Pn(*pn.split(pn_string))

                if (search_pn.flashsize in base_pn.flashsize and
                        search_pn.package == base_pn.package):
                    return g

        elif len(part_glob) == 0:
            raise RuntimeError("{} not found dog".format(search_pn))

    def tree_for_filename(self, fn):
        data = None
        with open(fn) as f:
            data = f.read()
            f.close()

        data = re.sub(' xmlns="[^"]+"', '', data, count=1)
        return xml.etree.ElementTree.fromstring(data)

    def pindesc_for_part(self, part):
        fn = self.filename_for_part(part)
        mcu_tree = self.tree_for_filename(fn)
        pin_tree = mcu_tree.findall("Pin")
        return self.pin_tree_to_descs(pin_tree)

    def pin_tree_to_descs(self, pin_tree_entries):
        return {
            # position is key
            p.attrib['Position']:
            # PinDesc is value
            PinDesc(p.attrib['Name'],
                    p.attrib['Type'],
                    # signals field is the set of all signal names
                    {s.attrib["Name"]
                     for s in p.findall("Signal")})
            for p in pin_tree_entries
        }
