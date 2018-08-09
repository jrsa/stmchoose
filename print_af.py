from choose.db import CubeDatabase
import sys


def main(arg):
    db = CubeDatabase()

    try:
        part_fn = arg[1]
    except IndexError as e:
        print("specify a part on the commandline")
        return

    pin_desc = db.pindesc_for_part(part_fn)

    for k in pin_desc.keys():
        print(k, '\t', pin_desc[k].name, '\t', ' '.join(pin_desc[k].signals))


if __name__ == '__main__':
    main(sys.argv)
