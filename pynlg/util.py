# encoding: utf-8

"""Definition of utility functions and classes."""

import importlib

from .lexicon.lang import FRENCH, ENGLISH
from .exc import UnhandledLanguage

mod_router = {
    FRENCH: 'fr',
    ENGLISH: 'en',
}

morphology_rules = {
    FRENCH: 'FrenchMorphologyRules',
    ENGLISH: 'EnglishMorphologyRules',
}

lexicon_router = {
    FRENCH: 'FrenchLexicon',
    ENGLISH: 'EnglishLexicon'
}


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


def _get_from_module(module_name, target, language):
    try:
        mod_name = mod_router[language]
    except KeyError:
        raise UnhandledLanguage('No module for %s was found in %s' %
                                (language, module_name))
    mod = importlib.import_module(module_name + '.' + mod_name, package=__package__)
    return getattr(mod, target)


def get_morphology_rules(language):
    """Return the appropriate morphology rules given a language."""
    return _get_from_module(
        '.morphology', language=language, target=morphology_rules[language])


def get_morphophonology_rules(language):
    """Return the appropriate morphophonology rules given a language."""
    return _get_from_module('.morphophonology', language=language, target='apply_rules')


def get_lexicon(language):
    """Return the appropriate lexicon given a language."""
    return _get_from_module('.lexicon', language=language, target=lexicon_router[language])
