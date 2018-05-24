import choose
import sys

# local copy of https://github.com/esden/stm32cube-database
DB_DIRECTORY = "/Users/jrsa/code/stm32cube-database/db/mcu/"

def main(arg):
    pns = arg[1:]

    if len(pns) != 2:
        print("specify 2 part numbers to compare")
        sys.exit(-1)

    chooser = choose.Stm32Chooser(DB_DIRECTORY)

    mcu_pin_lists = {pn : chooser.pinlist_for_part_with_signals(pn) for pn in pns}

    comp1_pn = list(mcu_pin_lists.keys())[0]
    comp2_pn = list(mcu_pin_lists.keys())[1]

    comp1_sig_list = mcu_pin_lists[comp1_pn]
    comp2_sig_list = mcu_pin_lists[comp2_pn]

    assert len(comp1_sig_list) == len(comp2_sig_list)

    signal_intersections = {}
    identical_pins = []
    comp1_only_signals = {}
    comp2_only_signals = {}
    pin_name_differences = {}

    # iterate the main pin/signal list, keys are pin numbers, k is the current pin
    # number everywhere in this loop
    for k in comp1_sig_list.keys():

        # values in pin list are (pin_name, pin_type, {sig1, sig2, ...})
        comp1_current_pin = comp1_sig_list[k]
        comp2_current_pin = comp2_sig_list[k]

        # pin name/type differences
        if comp1_current_pin[0] != comp2_current_pin[0]:
            pin_name_differences[k] = (comp1_current_pin[0], comp2_current_pin[0])

        # keep some information about singals, if there are any
        if len(comp2_current_pin[2]) or len(comp1_current_pin[2]):

            # check for intersection of the set of signals available on each pin (of the 2 ICs)
            signal_intersection = comp1_current_pin[2].intersection(comp2_current_pin[2])
            if len(signal_intersection):
                signal_intersections[k] = signal_intersection

            if comp1_current_pin[2] == comp2_current_pin[2]:
                identical_pins.append(k)

            comp1_only = comp1_current_pin[2].difference(comp2_current_pin[2])
            if len(comp1_only):
                comp1_only_signals[k] = comp1_only
            comp2_only = comp2_current_pin[2].difference(comp1_current_pin[2])
            if len(comp2_only):
                comp2_only_signals[k] = comp2_only

    # print out results, again looping over the total amount of pins
    for k in comp1_sig_list.keys():
        print("pin {} ({})".format(k, comp1_sig_list[k][0]))
        if k in pin_name_differences.keys():
            print("\tname differs:")
            print("\t{}: {}".format(comp1_pn, pin_name_differences[k][0]))
            print("\t{}: {}".format(comp2_pn, pin_name_differences[k][1]))

        if comp1_sig_list[k][1] != "I/O":
            # these aren't the droids you're looking for
            continue

        if k in identical_pins:
            print("pin {} has identical signals available on {} and {}".format(k, comp1_pn, comp2_pn))
            continue

        if k in comp1_only_signals.keys():
            print("\tonly on {}:".format(comp1_pn))
            for s in comp1_only_signals[k]:
                print("\t\t{}".format(s))
        if k in signal_intersections.keys():
            print("\tcommon: ")
            for s in signal_intersections[k]:
                print("\t\t{}".format(s))
        if k in comp2_only_signals.keys():
            print("\tonly on {}:".format(comp2_pn))
            for s in comp2_only_signals[k]:
                print("\t\t{}".format(s))

if __name__ == '__main__':
    main(sys.argv)
    sys.exit(0)
