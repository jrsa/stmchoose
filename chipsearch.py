#! /usr/bin/env python3

import argparse

import choose
import os
import sys

from util import printdict

def anyintersect(a, b):
    """
    compare any two strings, lists or combination thereof
    """
    def make_iterable(x):
        """
        return a single element wrapped in a list or collections as is
        """
        try:
            len(x)
        except TypeError as e:
            # object is not an iterable
            return [x]
        else:
            # object is iterable
            if type(x) != str:
                # pass through anything that isn't a string
                return x
            else:
                # still force a string to be inside another iterable
                # since they are 'atomic' as search terms and not to
                # be compared by intersection
                return [x]

    # compare two values or collections via set intersection. the inner
    # function forces a string to become a single member of a list
    # first to avoid its transformation into a set of characters
    return len(set(make_iterable(a)).intersection(set(make_iterable(b)))) != 0


def match(pn1, pn2):
    """
    compare two part numbers. return False when specified fields are not
    equal, return True otherwise (including the case when a field is
    multiply specified via a collection)
    """
    for i, pn1_field in enumerate(pn1):
        pn2_field = pn2[i]

        # if either element is None, that means it is effectively a wildcard
        # search term which was not specified, as a valid Pn will not be None
        # this is not quite solid but it's clear enough.
        if not pn1_field or not pn2_field:
            continue

        # this catches matches where one element is a list and the other is
        # a member of that list, eg.:
        # Pn("F7", None, None, "I", None) and Pn("F7", "67", "N", ["G", "I"], "H")
        # will return true from anyintersect
        if anyintersect(pn1_field, pn2_field):
            continue

        if pn1_field != pn2_field:
            return False

    return True


def main():
    # add command line options based on the fields present on the Pn class
    # if these are present they will be used as search terms
    parser = argparse.ArgumentParser()
    [parser.add_argument('--' + f, default=None, dest=f)
     for f in choose.Pn._fields]

    parser.add_argument('-d', '--dump', dest='dump',
                        default=None, const=True, action='store_const')

    args = parser.parse_args()

    dargs = vars(args)
    partargs = {k: dargs[k] for k in dargs if k in choose.Pn._fields}

    # use the result from the arg parser, converted to a dictionary, as keyword
    # arguments to construct a Pn
    searchpn = choose.Pn(**partargs)

    # this can move to choose.Pn (should be enforced in Pn creation)
    # this would actually involve subclassing Pn because it is a
    # factory built class (generated by namedtuple)
    """
    fam = args.family
    if not fam in ['F0', 'F1', 'F2', 'F3', 'F4', 'F7', 'H7']:
        print("invalid family")
        sys.exit(-1)
    """

    # generate the full set of valid Pns from the set of xml filenames in the
    # stm32cube database
    chooser = choose.Stm32Chooser()

    # map globbed xml file paths in the database to part number strings of the form 'F469NIHx'
    base_filenames = [os.path.basename(f)[5:-4]
                      for f in chooser.enum_xmlfiles()]

    # map the base_filenames, strings of the form 'F469NIHx' to new Pn namedtuple instances.
    all = [choose.Pn(*choose.split_pn(f)) for f in base_filenames]

    if args.dump:
        values = {}
        for pn in all:
            pndict = pn._asdict()
            for k in pndict:
                value = pndict[k]
                try:
                    values[k].add(value)
                except KeyError:
                    # key name not present in dictionary yet
                    values[k] = {value}
                except TypeError:
                    # value is a list (i think)
                    for e in value:
                        values[k].add(e)

        printdict(values)

        return

    # filter the complete set of valid part numbers by the search terms
    results = [pn for pn in all if match(pn, searchpn)]

    # the moment we've all been waiting for, print the results
    for r in results:
        print(choose.join_pn(r))


if __name__ == '__main__':
    main()
