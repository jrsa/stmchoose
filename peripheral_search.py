import argparse
from collections import defaultdict
from copy import deepcopy
from pprint import pprint
import re
import sys

from choose.db import CubeDatabase


def map_signal_specifiers(peripheral):
    if '=' in peripheral:
        try:
            peripheral, signals = peripheral.split('=')
        except:
            print('invalid peripheral specification: {peripheral}')
            raise
        signals = signals.split(',')
        return (peripheral, signals)
    return peripheral

def main(pn, periphs, allocate, squash):
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

            # turn pin "function" names like TIM2_CH1 into a pair, preserving function names with underscores such as SAI2_FS_B
            signal_name_components = [signal_name_components[0], '_'.join(signal_name_components[1:])]

            peripheral, signal = signal_name_components
            peripherals[peripheral].append((signal, pin_description.name, pin_number))

    requested_peripherals = deepcopy(periphs)
    available_peripherals = deepcopy(peripherals)

    requested_peripherals = [
        map_signal_specifiers(p)
        for p in requested_peripherals
    ]

    matches = []
    while requested_peripherals and (next_p := requested_peripherals.pop()):
        if type(next_p) != str:
            next_p, functions = next_p
            print(functions)

        if allocate:
            possible_match = next(p for p in available_peripherals if re.match(next_p, p) )
            available_peripherals.pop(possible_match)
            matches.append((next_p, possible_match))
        else:
            this_matches = [p for p in available_peripherals if re.match(next_p, p)]
            matches.append((next_p, this_matches))

    # write header
    if not squash:
        print('peripheral_type,peripheral_instance,peripheral_signal,logical_pin,package_pin')

    for match, periph in matches:
        if type(periph) == list:
            periph = sorted(periph)
            for p in periph:
                signals = sorted(peripherals[p])
                if not squash: # individual signal rows
                    for signal in signals:
                        print(f'{match},{p},{",".join(signal)}')
                else:
                    signals_by_function = defaultdict(list)
                    for signal in signals:
                        signals_by_function[signal[0]].append(signal[1])
                    for function, signal in signals_by_function.items():
                        print(f'{match},{p},{function},{",".join(signal)}')

        else:
            print(f'{match}\t{periph}')

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('pn')
    argparser.add_argument('periphs', nargs='+')
    argparser.add_argument('--allocate', action='store_true', default=False)
    argparser.add_argument('--squash', action='store_true', default=False)
    args = argparser.parse_args()
    main(**vars(args))
