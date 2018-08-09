from choose.db import Stm32Chooser
import sys

import argparse

def main(arg):
    pns = arg.pns

    if len(pns) != 2:
        print("specify 2 part numbers to compare")
        sys.exit(-1)

    chooser = Stm32Chooser()

    mcu_pin_lists = {pn : chooser.pindesc_for_part(pn) for pn in pns}
    assert list(mcu_pin_lists.keys()) == pns

    comp1_pn = list(mcu_pin_lists.keys())[0]
    comp2_pn = list(mcu_pin_lists.keys())[1]

    comp1_sig_list = mcu_pin_lists[comp1_pn]
    comp2_sig_list = mcu_pin_lists[comp2_pn]

    assert len(comp1_sig_list) == len(comp2_sig_list)

    # storage for results, all are dictionaries indexed by pin number
    signal_intersections = {}
    comp1_only_signals = {}
    comp2_only_signals = {}
    pin_name_differences = {}

    # except for this array, which holds arbitrary pin numbers
    identical_pins = []

    # iterate the main pin/signal list, keys are pin numbers, k is the current pin
    # number everywhere in this loop
    for k in comp1_sig_list.keys():

        # values in sig list are (pin_name, pin_type, {sig1, sig2, ...})

        # pin name/type differences
        if comp1_sig_list[k][0] != comp2_sig_list[k][0]:
            pin_name_differences[k] = (comp1_sig_list[k][0], comp2_sig_list[k][0])

        # keep some information about singals, if there are any
        if len(comp2_sig_list[k][2]) or len(comp1_sig_list[k][2]):

            # check for intersection of the set of signals available on each pin (of the 2 ICs)
            signal_intersection = comp1_sig_list[k][2].intersection(comp2_sig_list[k][2])
            if len(signal_intersection):
                signal_intersections[k] = signal_intersection

            if comp1_sig_list[k][2] == comp2_sig_list[k][2]:
                identical_pins.append(k)

            comp1_only = comp1_sig_list[k][2].difference(comp2_sig_list[k][2])
            if len(comp1_only):
                comp1_only_signals[k] = comp1_only
            comp2_only = comp2_sig_list[k][2].difference(comp1_sig_list[k][2])
            if len(comp2_only):
                comp2_only_signals[k] = comp2_only

    # print out results, again looping over the total amount of pins
    for k in comp1_sig_list.keys():
        output_line = str(k) + ' '
        if k in pin_name_differences.keys():
            dif = (pin_name_differences[k][0], comp1_pn, pin_name_differences[k][1], comp2_pn)
            output_line += "({}: {}, {}: {}) (renamed)".format(*dif)
        else:
            output_line += "({})".format(comp1_sig_list[k][0])

        output_line += '\t'

        if k in signal_intersections.keys() and args.common:
            output_line += " ".join(signal_intersections[k])

        if args.exclusions:
            if k in comp1_only_signals.keys():
                output_line += ", {} only: ".format(comp1_pn)
                output_line += " ".join(comp1_only_signals[k])

            if k in comp2_only_signals.keys():
                output_line += ", {} only: ".format(comp2_pn)
                output_line += " ".join(comp2_only_signals[k])

        print(output_line)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='compare stm32 parts by signals available on their pins')

    parser.add_argument('pns', metavar='pn', type=str, nargs='+', help='part numbers')

    parser.add_argument('-c', '--common', dest='common', action='store_const',
        const=True, default=False, help='print signals that are available on both chips')

    parser.add_argument('-e', '--exclusions', dest='exclusions', action='store_const',
        const=True, default=False, help='print signals that are only available on one chip')

    args = parser.parse_args()

    print(args)

    try:
        main(args)
    except RuntimeError as e:
        print(e)
        sys.exit(1)
    sys.exit(0)
