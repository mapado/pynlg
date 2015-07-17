# encoding: utf-8

"""Definition of utility functions and classes."""

import importlib

from .lexicon.lang import FRENCH, ENGLISH
from .lexicon.feature.category import NOUN_PHRASE, ADJECTIVE_PHRASE
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


phrase_helper_router = {
    FRENCH: {
        NOUN_PHRASE: 'FrenchNounPhraseHelper',
        ADJECTIVE_PHRASE: 'FrenchAdjectivePhraseHelper',
        'phrase': 'FrenchPhraseHelper'
    },
    ENGLISH: {
        NOUN_PHRASE: 'EnglishNounPhraseHelper',
        ADJECTIVE_PHRASE: 'EnglishAdjectivePhraseHelper',
        'phrase': 'EnglishPhraseHelper',
    },
}


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


def get_phrase_helper(language, phrase_type):
    """Return the appropriate phrase helper given a language and a phrase type."""
    return _get_from_module(
        '.helper',
        language=language,
        target=phrase_helper_router[language][phrase_type])
