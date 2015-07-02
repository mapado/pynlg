# encoding: utf-8

"""Test suite of the lexicon package"""

import pytest

from pynlg.lexicon import Lexicon, FRENCH, ENGLISH, UnhandledLanguage
from xml.etree.ElementTree import ElementTree


@pytest.mark.parametrize("lang", [FRENCH, ENGLISH])
def test_lexicon_supported_languages(lang):
    lx = Lexicon(lang)
    assert isinstance(lx.data, ElementTree)


def test_lexicon_other_language():
    with pytest.raises(UnhandledLanguage):
        Lexicon('unhandled language')
