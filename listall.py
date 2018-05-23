import choose
import os
import sys

# local copy of https://github.com/esden/stm32cube-database
DB_DIRECTORY = "/Users/jrsa/code/stm32cube-database/db/mcu/"


def main(arg):
    chooser = choose.Stm32Chooser(DB_DIRECTORY)
    for f in chooser.enum_xmlfiles():
        print(os.path.basename(f)[:-4])

if __name__ == '__main__':
    main(sys.argv)
    sys.exit(0)
