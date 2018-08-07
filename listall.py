import choose
import os
import sys


def main(arg):
    chooser = choose.Stm32Chooser()
    for f in chooser.enum_xmlfiles():
        print(os.path.basename(f)[:-4])

if __name__ == '__main__':
    main(sys.argv)
    sys.exit(0)
