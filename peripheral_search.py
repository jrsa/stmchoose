import argparse
from collections import defaultdict
from copy import deepcopy
from pprint import pprint
import re
import sys

from choose.db import CubeDatabase


def main(pn, periphs, allocate, flatten):
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
    if allocate:
        while requested_peripherals and (next_p := requested_peripherals.pop()):
            possible_match = next(p for p in available_peripherals if re.match(next_p, p) )
            available_peripherals.pop(possible_match)
            matches.append((next_p, possible_match))
    else:
        if flatten:
            requested_peripherals = set(requested_peripherals)
        while requested_peripherals and (next_p := requested_peripherals.pop()):
            this_matches = [p for p in available_peripherals if re.match(next_p, p)]
            matches.append((next_p, this_matches))

    print('peripheral_type,peripheral_instance,peripheral_signal,logical_pin,package_pin')
    for match, periph in matches:
        if type(periph) == list:
            periph = sorted(periph)
            for p in periph:
                signals = sorted(peripherals[p])
                for signal in signals:
                    print(f'{match},{p},{",".join(signal)}')
        else:
            print(f'{match}\t{periph}')

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('pn')
    argparser.add_argument('periphs', nargs='+')
    argparser.add_argument('--allocate', action='store_true', default=False)
    argparser.add_argument('--flatten', action='store_true', default=False)
    args = argparser.parse_args()
    main(**vars(args))
