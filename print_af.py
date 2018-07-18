import choose
import sys

# local copy of https://github.com/esden/stm32cube-database
DB_DIRECTORY = "/Users/jrsa/code/stm32cube-database/db/mcu/"


def main(arg):
    chooser = choose.Stm32Chooser(DB_DIRECTORY)

    try:
        part_fn = arg[1]
    except IndexError as e:
        print("specify a part on the commandline")
        return

    pin_desc = chooser.pindesc_for_part(part_fn)

    for k in pin_desc.keys():
        print(k, '\t', pin_desc[k].name, '\t', ' '.join(pin_desc[k].signals))


if __name__ == '__main__':
    main(sys.argv)
