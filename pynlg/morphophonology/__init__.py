# encoding: utf-8

import importlib

from ..lexicon.lang import FRENCH, ENGLISH
from ..exc import UnhandledLanguage

mod_router = {
    FRENCH: 'fr',
    ENGLISH: 'en',
}


def get_morphophonology_rules(language):
    """Return the appropriate morphophonology rules given a language."""
    try:
        mod_name = mod_router[language]
    except KeyError:
        raise UnhandledLanguage('Morphophonologic rules not defined for %s' % (
            language))
    mod = importlib.import_module('.' + mod_name, package=__package__)
    return getattr(mod, 'apply_rules')
