import choose
import sys

from util import printdict

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

    # for each pin
    for p in pin_positions:

        # look at all the MCUs specified for comparison, 2 at a time
        for pn in desc:
            for pn2 in desc:
                if pn == pn2: break

                name1 = desc[pn][p].name
                name2 = desc[pn2][p].name

                if name1 != name2:
                    if p in diffs:
                        if name1 in diffs[p]:
                            diffs[p][name1].update({pn})
                        else:
                            diffs[p][name1] = {pn}

                        if name2 in diffs[p]:
                            diffs[p][name2].update({pn2})
                        else:
                            diffs[p][name2] = {pn2}
                    else:
                        diffs[p] = {name1: {pn}, name2: {pn2}}
                else:
                    if p in diffs:
                        diffs[p][name1].update({pn, pn2})

    # the moment we've all been waiting for
    printdict(diffs)

if __name__ == '__main__':
    try:
        main(sys.argv)
    except RuntimeError as e:
        print("error: {}".format(e))
        sys.exit(1)

    sys.exit(0)
