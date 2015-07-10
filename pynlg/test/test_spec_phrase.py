# encoding: utf-8

"""Test suite of the phrase classes"""

import pytest

from ..spec.phrase import PhraseElement, AdjectivePhraseElement
from ..lexicon.feature.internal import HEAD
from ..lexicon.feature.category import ADJECTIVE_PHRASE, ADJECTIVE


@pytest.fixture
def adj_phrase(lexicon_fr):
    return AdjectivePhraseElement(lexicon_fr)


def test_set_adjective(lexicon_fr, adj_phrase):
    adj = lexicon_fr.first(u'meilleur')
    adj_phrase.adjective = adj
    assert adj_phrase.adjective == adj


def test_set_str_adjective(lexicon_fr, adj_phrase):
    adj = lexicon_fr.first(u'meilleur')
    adj_phrase.adjective = u'meilleur'
    assert adj_phrase.adjective == adj


def test_set_unknown_str_adjective(lexicon_fr, adj_phrase):
    assert u'swag' not in lexicon_fr
    adj_phrase.adjective = u'swag'
    assert u'swag' in lexicon_fr
    swag = lexicon_fr.first(u'swag', category=ADJECTIVE)
    assert adj_phrase.adjective == swag


def test_children(lexicon_fr, adj_phrase):
    adj = lexicon_fr.first(u'meilleur')
    adj_phrase.adjective = u'meilleur'
    assert adj_phrase.get_children() == [adj]
