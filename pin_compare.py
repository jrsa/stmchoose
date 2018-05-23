import choose
import sys

# local copy of https://github.com/esden/stm32cube-database
DB_DIRECTORY = "/Users/jrsa/code/stm32cube-database/db/mcu/"

# part numbers to compare pins (official tool says these are compatible)
# COMP1 = "F405ZGTx"
# COMP2 = "H743ZITx"

COMP1 = "F405RGTx"
COMP2 = "F401R(D-E)Tx"


def main(arg):
    chooser = choose.Stm32Chooser(DB_DIRECTORY)

    # ElementTree for this mcu
    comp1_tree = chooser.tree_for_filename(chooser.filename_for_part(COMP1))
    comp2_tree = chooser.tree_for_filename(chooser.filename_for_part(COMP2))

    comp1_list = choose.pin_tree_to_list(comp1_tree.findall("Pin"))
    comp2_list = choose.pin_tree_to_list(comp2_tree.findall("Pin"))

    for i, e in enumerate(comp1_list):
        if e != comp2_list[i]:
            print(e, comp2_list[i]) 

if __name__ == '__main__':
    main(sys.argv)
    sys.exit(0)
