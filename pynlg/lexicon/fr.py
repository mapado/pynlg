# encoding: utf-8

"""Definition of the french Lexicon."""

from .lexicon import Lexicon
from .lang import FRENCH


class FrenchLexicon(Lexicon):

    """Lexicon defining specific rules for the french language."""

    language = FRENCH
