# encoding: utf-8

"""Definition of the test fixtures"""

import pytest

from ..lexicon.fr import FrenchLexicon
from ..lexicon.en import EnglishLexicon


@pytest.fixture(scope='session')
def lexicon_fr():
    """An indexed french lexicon"""
    return FrenchLexicon()


@pytest.fixture(scope='session')
def lexicon_en():
    """An indexed english lexicon"""
    return EnglishLexicon()


@pytest.fixture
def empty_lexicon_fr():
    """An unindexed french lexicon"""
    return FrenchLexicon(auto_index=False)


@pytest.fixture
def empty_lexicon_en():
    """An unindexed english lexicon"""
    return EnglishLexicon(auto_index=False)
