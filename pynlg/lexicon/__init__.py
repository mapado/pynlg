# encoding: utf-8

from .fr import FrenchLexicon
from .en import EnglishLexicon
from .lang import FRENCH, ENGLISH

lexicon_router = {
    FRENCH: FrenchLexicon,
    ENGLISH: EnglishLexicon
}


def get_lexicon(language):
    return lexicon_router[language]
