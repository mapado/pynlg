# encoding: utf-8

"""Test suite of the WordElement class."""

import pytest

from ..spec.word import WordElement, InflectedWordElement
from ..lexicon.feature.category import NOUN, ADJECTIVE
from ..lexicon.feature.number import PLURAL
from ..lexicon.feature import NUMBER


@pytest.fixture(scope='module')
def word():
    return WordElement(
        base_form='fish',
        category=NOUN,
        id="E123",
        lexicon=None)


@pytest.mark.parametrize("word,other_word", [
    (
        WordElement('beau', ADJECTIVE, "E123", None),
        WordElement('beau', ADJECTIVE, "E123", None),
    ),
    pytest.mark.xfail((
        WordElement('joli', ADJECTIVE, "E1", None),
        WordElement('beau', ADJECTIVE, "E123", None),
    )),
    pytest.mark.xfail((
        WordElement('joli', ADJECTIVE, "E1", None),
        'something',
    ))
])
def test_equality(word, other_word):
    assert word == other_word


def test_default_inflection_variant(word):
    word.default_inflection_variant = 'fish'
    assert word.default_inflection_variant == 'fish'


def test_inflectional_variants(word):
    word.inflectional_variants = ['fish', 'fishes']
    assert word.inflectional_variants == ['fish', 'fishes']


def test_spelling_variants(word):
    word.spelling_variants = [u'clé', u'clef']
    assert word.spelling_variants == [u'clé', u'clef']


def test_default_spelling_variant(word):
    word.default_spelling_variant = u'clé'
    assert word.default_spelling_variant == u'clé'


def test_children(word):
    assert word.children == []


def test_inflex(word):
    iw = word.inflex(number=PLURAL)
    assert isinstance(iw, InflectedWordElement)
    assert iw.features[NUMBER] == PLURAL
