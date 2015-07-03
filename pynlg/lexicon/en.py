# encoding: utf-8

"""Definition of the english Lexicon."""

from .lexicon import Lexicon
from .lang import ENGLISH


class EnglishLexicon(Lexicon):

    """Lexicon defining specific rules for the english language."""

    language = ENGLISH
