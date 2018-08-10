from collections import namedtuple

Pn = namedtuple('Pn', ['family', 'subtype', 'pincount', 'flashsize', 'package'])

def split(pn):
    """
    return a tuple containing part number components. from a string of the
    form 'F469NIHx', return ('F4', '69', 'N', 'I', 'H')

    the branch handles strings of the form 'F103C(8-B)Tx' where '8' and 'B'
    are distinct values for the 'flashsize' field on Pn. a substring of the
    form '(A-B)' results in a list containing 'A' and 'B'
    """
    if pn[5] == '(':
        closing_paren = pn.index(')')
        return (pn[:2], pn[2:4], pn[4:5], pn[6:closing_paren].split("-"),
                pn[closing_paren+1:closing_paren+2])
    else:
        return (pn[:2], pn[2:4], pn[4:5], pn[5:6], pn[6:7])

def join(pn):
    """
    return a part number string of the form 'F469NIHx', given an instance
    of Pn
    """
    try:
        return "".join(pn)
    except TypeError:
        str_flashsizes = "({})".format("-".join(pn.flashsize))
        orig_attrs = pn._asdict()
        orig_attrs = {k: orig_attrs[k]
                      for k in orig_attrs
                      if k is not 'flashsize'}
        return join_pn(Pn(**orig_attrs, flashsize=str_flashsizes))
