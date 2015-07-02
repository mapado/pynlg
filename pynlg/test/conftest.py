# encoding: utf-8

"""Definition of the test fixtures"""

import pytest

from ..lexicon.lexicon import Lexicon
from ..lexicon.lang import ENGLISH, FRENCH


@pytest.fixture(scope='session')
def lexicon_fr():
    """An indexed french lexicon"""
    return Lexicon(language=FRENCH)


@pytest.fixture(scope='session')
def lexicon_en():
    """An indexed english lexicon"""
    return Lexicon(language=ENGLISH)


@pytest.fixture
def empty_lexicon_fr():
    """An unindexed french lexicon"""
    return Lexicon(language=FRENCH, auto_index=False)


@pytest.fixture
def empty_lexicon_en():
    """An unindexed english lexicon"""
    return Lexicon(language=ENGLISH, auto_index=False)
