import choose
import sys

# local copy of https://github.com/esden/stm32cube-database
DB_DIRECTORY = "/Users/jrsa/code/stm32cube-database/db/mcu/"

# part numbers to compare pins (official tool says these are compatible)
# COMP1 = "F405ZGTx"
# COMP2 = "H743ZITx"

COMP1 = "F405RGTx"
COMP2 = "F401R(D-E)Tx"


def bi_compare(this, that):
    unequal_elements = []
    for i, e in enumerate(this):
        if e != that[i]:
            unequal_elements.append((e, that[i]))

    return unequal_elements



def main(arg):
    pns = arg[1:]

    if len(pns) != 2:
        print("specify 2 part numbers to compare")
        sys.exit(-1)
    else:
        print("comparing {} and {}:".format(pns[0], pns[1]))

    chooser = choose.Stm32Chooser(DB_DIRECTORY)

    comp1_list = chooser.pinlist_for_part(pns[0])
    comp2_list = chooser.pinlist_for_part(pns[1])

    pin_name_diffs = bi_compare(comp1_list, comp2_list)

    # print("{} pin name differences:".format(len(pin_name_diffs)))
    # for d in pin_name_diffs: print(d);

    comp1_sig_list = chooser.pinlist_for_part_with_signals(pns[0])
    comp2_sig_list = chooser.pinlist_for_part_with_signals(pns[1])

    assert len(comp1_sig_list) == len(comp2_sig_list)

    common_signals = {}

    print(comp1_sig_list[0])
    print(comp2_sig_list[0])
    sys.exit(0)

    for i, e in enumerate(comp1_sig_list):
        e1 = e
        e2 = comp2_sig_list[i]
        
        # pin name/type differences
        if e1[0] != e2[0]:
            print("pin names differ: {} => {}".format(e1[0], e2[0]))

        if not (len(e1[1]) or len(e2[1])):
            # don't proceed with this loop iteration if both
            # signal sets are empty
            continue
        
        common_sig = e1[1].union(e2[1])
        if len(common_sig):
            common_signals[i] = common_sig 


    print(common_signals.keys())




if __name__ == '__main__':
    main(sys.argv)
    sys.exit(0)
