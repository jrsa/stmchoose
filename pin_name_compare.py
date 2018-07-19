import choose
import sys


def main(arg):
    pns = arg[1:]

    if len(pns) < 2:
        raise RuntimeError("specify at least 2 part numbers to compare")
        sys.exit(1)

    chooser = choose.Stm32Chooser()
    desc = {pn : chooser.pindesc_for_part(pn) for pn in pns}

    last = None
    for partnumber in desc:
        this = set(desc[partnumber].keys())
        if last and (this != last):
            raise RuntimeError("mcu {} differs in pin count".format(partnumber))
        last = this

    # as long as the mcus all have the same set of pin positions
    # (package) we can use one of them as *the* pin positions 
    pin_positions = last

    diffs = {}
    diffs2 = {}
    diffs3 = {}

    # for each pin
    for p in pin_positions:

        # look at all the MCUs specified for comparison, 2 at a time
        for pn in desc:
            for other_pn in desc:
                if pn == other_pn: break

                if desc[pn][p].name != desc[other_pn][p].name:
                    # gives list of part number, pin name pairs,
                    # with one element per mcu
                    pair1 = (pn, desc[pn][p].name)
                    pair2 = (other_pn, desc[other_pn][p].name)

                    if p in diffs:
                        if pair1 not in diffs[p]:
                            diffs[p].append(pair1)
                        if pair2 not in diffs[p]:
                            diffs[p].append(pair2)

                    else:
                        diffs[p] = [pair1, pair2]



                    # method 2 gives set of pin names
                    names = {desc[pn][p].name, desc[other_pn][p].name}
                    if p in diffs2: 
                        diffs2[p].update(names)
                    else:
                        diffs2[p] = (names)

    # the moment we've all been waiting for
    for pp in diffs:
        print("{}: {}".format(pp, diffs[pp]))

    for pp in diffs2:
        print("{}: {}".format(pp, diffs2[pp]))

    print("{} total differences".format(len(diffs2)))

if __name__ == '__main__':
    try:        
        main(sys.argv)
    except RuntimeError as e:
        print("error: {}".format(e))
        sys.exit(1)

    sys.exit(0)
