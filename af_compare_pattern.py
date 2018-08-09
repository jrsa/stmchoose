import choose
import sys

import re

ADC_INPUT_SIGNAL_PATTERN = "ADC([123]{1,3})_IN([\d,P,N])"

def main(arg):
    pns = arg[1:3]
    try:
        pattern = arg[3]
    except IndexError as e:
        pattern = ADC_INPUT_SIGNAL_PATTERN

    if len(pns) != 2:
        print("specify 2 part numbers to compare")
        sys.exit(1)

    chooser = choose.Stm32Chooser()

    mcu_pin_lists = {pn : chooser.pindesc_for_part(pn) for pn in pns}
    assert list(mcu_pin_lists.keys()) == pns

    comp1_pn = list(mcu_pin_lists.keys())[0]
    comp2_pn = list(mcu_pin_lists.keys())[1]

    comp1_sig_list = mcu_pin_lists[comp1_pn]
    comp2_sig_list = mcu_pin_lists[comp2_pn]

    if len(comp1_sig_list) != len(comp2_sig_list):
        print("parts chosen have different sized packages")
        sys.exit(1)

    identical_pins = []

    adc_exact_matches = {}
    adc_fuzzy_matches = {}

    #
    #   iterate the main pin/signal dict where the key is the pin number
    #
    for k in comp1_sig_list.keys():
        if comp1_sig_list[k].name != comp2_sig_list[k].name:
            name = "_".join([comp1_sig_list[k].name, comp2_sig_list[k].name])
        else:
            name = comp1_sig_list[k].name

        matches1 = set([x for x in comp1_sig_list[k].signals
            if re.match(pattern, x)])

        matches2 = set([x for x in comp2_sig_list[k].signals
            if re.match(pattern, x)])

        if len(matches1) and len(matches2):
            match = {"name": name, comp1_pn: matches1, comp2_pn: matches2}

            isect = matches1.intersection(matches2)

            if matches1 == matches2:
                adc_exact_matches[k] = match
            elif len(isect):
                adc_exact_matches[k] = {"name": name,
                    comp1_pn: isect, comp2_pn: isect}
            else:
                adc_fuzzy_matches[k] = match

    #
    #   print results
    #
    if len(adc_exact_matches):
        print("{} exact matches".format(len(adc_exact_matches)))
        for k in adc_exact_matches.keys():
            print(k, adc_exact_matches[k])

    if len(adc_fuzzy_matches):
        print("{} pattern matches".format(len(adc_fuzzy_matches)))
        for k in adc_fuzzy_matches.keys():
            print(k, adc_fuzzy_matches[k])

if __name__ == '__main__':
    try:
        main(sys.argv)
    except RuntimeError as e:
        print(e)
    sys.exit(0)
