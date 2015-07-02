# encoding: utf-8

"""Definition of utility functions and classes."""


def ensure_unicode(s):
    """Convert the argument string to unicode, if needed.

    If the argument is not of type str of unicode, a TypeError is raised.

    """
    if not isinstance(s, basestring):
        raise TypeError('argument type must be str or unicode, not %s' % (
            str(type(s))))
    if isinstance(s, unicode):
        return s
    else:
        return s.decode('utf-8')
