# encoding: utf-8

"""Test suite of the phrase classes"""

from __future__ import unicode_literals

import pytest

from ..spec.phrase import AdjectivePhraseElement, NounPhraseElement
from ..lexicon.feature.category import ADJECTIVE, NOUN, DETERMINER
from ..lexicon.feature.discourse import SPECIFIER, HEAD


@pytest.fixture
def adj_phrase(lexicon_fr):
    return AdjectivePhraseElement(lexicon_fr)


@pytest.fixture
def noun_phrase(lexicon_fr):
    return NounPhraseElement(lexicon_fr)


def test_set_adjective(lexicon_fr, adj_phrase):
    adj = lexicon_fr.first('meilleur')
    adj_phrase.adjective = adj
    assert adj_phrase.adjective == adj


def test_set_str_adjective(lexicon_fr, adj_phrase):
    adj = lexicon_fr.first('meilleur')
    adj_phrase.adjective = 'meilleur'
    assert adj_phrase.adjective == adj


def test_set_unknown_str_adjective(lexicon_fr, adj_phrase):
    assert 'swag' not in lexicon_fr
    adj_phrase.adjective = 'swag'
    assert 'swag' in lexicon_fr
    swag = lexicon_fr.first('swag', category=ADJECTIVE)
    assert adj_phrase.adjective == swag


def test_adj_phrase_children(lexicon_fr, adj_phrase):
    adj = lexicon_fr.first('meilleur')
    adj_phrase.adjective = 'meilleur'
    assert adj_phrase.get_children() == [adj]


def test_noun_phrase_children(lexicon_fr, noun_phrase):
    un = lexicon_fr.first('un', category=DETERMINER)
    beau = lexicon_fr.first('beau', category=ADJECTIVE)
    endroit = lexicon_fr.first('endroit', category=NOUN)
    perdu = lexicon_fr.first('perdu', category=ADJECTIVE)
    noun_phrase.head = endroit
    noun_phrase.specifier = un
    noun_phrase.add_modifier(beau)  # 'beau' is preposed, as indicated in lexicon
    noun_phrase.add_modifier(perdu)
    assert noun_phrase.get_children() == [un, beau, endroit, perdu]
    assert noun_phrase.premodifiers == [beau]
    assert noun_phrase.postmodifiers == [perdu]
    assert un.parent == noun_phrase
    assert beau.parent == noun_phrase
    assert endroit.parent == noun_phrase
    assert perdu.parent == noun_phrase
    assert un.discourse_function == SPECIFIER
    assert beau.discourse_function is None  # should it be None?
    assert endroit.discourse_function is None  # should it be None?
    assert perdu.discourse_function is None  # should it be None?
