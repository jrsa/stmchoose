import argparse
from collections import defaultdict
from copy import deepcopy
from pprint import pprint
import re
import sys

from choose.db import CubeDatabase


def main(pn, periphs):
    db = CubeDatabase()

    try:
        pin_desc = db.pindesc_for_part(pn)
    except RuntimeError:
        print(f'part number {part_fn} not found!')
        exit(1)

    peripherals = defaultdict(list)

    for pin_number, pin_description in pin_desc.items():
        for signal_name in pin_description.signals:
            signal_name_components = signal_name.split('_')
            if signal_name == 'GPIO':
                continue

            # TODO: fix signals with multiple _ (just use first _)
            if len(signal_name_components) != 2:
                continue

            peripheral, signal = signal_name_components
            peripherals[peripheral].append((signal, pin_description.name, pin_number))

    requested_peripherals = deepcopy(periphs)
    available_peripherals = deepcopy(peripherals)

    matches = []
    while requested_peripherals and (next_p := requested_peripherals.pop()):
        possible_match = next(p for p in available_peripherals if re.match(next_p, p) )
        available_peripherals.pop(possible_match)
        matches.append((next_p, possible_match))

    pprint(matches)




if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('pn')
    argparser.add_argument('periphs', nargs='+')
    args = argparser.parse_args()
    main(**vars(args))
