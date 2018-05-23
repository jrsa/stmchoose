import choose
import sys

# local copy of https://github.com/esden/stm32cube-database
DB_DIRECTORY = "/Users/jrsa/code/stm32cube-database/db/mcu/"


def main(arg):
    chooser = choose.Stm32Chooser(DB_DIRECTORY)

    try:
        part_fn = chooser.filename_for_part(arg[1])
    except IndexError as e:
        print("specify a part on the commandline")
        return

    single_tree = chooser.tree_for_filename(part_fn)

    print(part_fn)

    for pin in single_tree.findall("Pin"):
        afs = []
        for sig in pin.findall("Signal"):
            afs.append(sig.attrib["Name"])

        print("{} {} {} {}".format(
            pin.attrib["Position"], pin.attrib["Name"], pin.attrib["Type"], " ".join(afs)))


if __name__ == '__main__':
    main(sys.argv)
