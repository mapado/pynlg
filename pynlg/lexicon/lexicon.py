# encoding: utf-8

"""Definition of the lexicon handlers."""

from __future__ import absolute_import

from xml.etree import cElementTree as ElementTree
from os.path import join, dirname, abspath, exists

from ..spec.word import WordElement
from .lang import DEFAULT
from ..util import ensure_unicode as u
from ..exc import UnhandledLanguage

__all__ = ['Lexicon']


class Lexicon(object):

    """A Lexicon is a collection of metadata about words of a specific
    language.

    """

    #  node names in lexicon XML files
    BASE = "base"

    #  base form of Word
    CATEGORY = "category"

    #  base form of Word
    ID = "id"

    #  base form of Word
    WORD = "word"

    #  node defining a word
    #  inflectional codes which need to be set as part of INFLECTION feature
    INFL_CODES = ["reg", "irreg", "uncount", "inv",
                  "metareg", "glreg", "nonCount", "sing", "groupuncount"]

    def __init__(self, language=DEFAULT):
        self.language = language
        self._load()

    def _load(self):
        """Load the lexicon data from the XML file."""
        self.data = ElementTree.parse(self.lexicon_filepath)

    @property
    def lexicon_filepath(self):
        """Return the path to the XML lexicon file associated with the
        instance language.

        """
        filepath = abspath(join(dirname(__file__), 'data', '%s-lexicon.xml' % (
            self.language)))
        if not exists(filepath):
            raise UnhandledLanguage(
                '%s language is not handled: %s file not found.' % (
                    self.language, filepath))
        return filepath
