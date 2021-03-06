# encoding: utf-8

"""Test suite of the StringElement class."""

import pytest

from ..spec.string import StringElement
from ..lexicon.feature.category import CANNED_TEXT, NOUN
from ..lexicon.feature.gender import FEMININE
from ..lexicon.lang import FRENCH
from ..lexicon.feature import ELIDED


def test_string_element_no_base_word():
    se = StringElement(u"à la pêche au requin")
    assert se.category == CANNED_TEXT
    assert se.realisation == u"à la pêche au requin"
    assert se.features == {ELIDED: False}
    assert se.children == []


def test_string_element_with_base_word(lexicon_fr):
    w = lexicon_fr.first(u"pêche")
    se = StringElement(word=w)
    assert se.category == NOUN
    assert se.realisation == u"pêche"
    assert se.elided is False
    assert se.gender == FEMININE
    assert se.children == []


@pytest.mark.parametrize('left,right,expected_left,expected_right', [
    ('de', 'le', 'du', None),
    ('de', 'lequel', 'duquel', None),
    ('le', 'arbre', "l'", 'arbre'),
    ('que', "qu'", "que", None),
])
def test_realise_word_morphophonology(
        lexicon_fr, left, right, expected_left, expected_right):
    left = lexicon_fr.first(left)
    str_left = StringElement(word=left, language=FRENCH)
    right = lexicon_fr.first(right)
    str_right = StringElement(word=right, language=FRENCH)
    str_left.realise_morphophonology(next_word=str_right)
    assert str_left.realisation == expected_left
    assert str_right.realisation == expected_right


def test_realise_morphophonology_phrase(lexicon_fr):
    words = [u"Je", u"vais", u"à", u"la", u"pêche", u"à", u"le", u"poisson"]
    words = (lexicon_fr.first(w) for w in words)
    words = [StringElement(word=w, language=FRENCH) for w in words]
    for i, word in enumerate(words[:-1]):
        word.realise_morphophonology(next_word=words[i + 1])
    reas = [w.realisation for w in words if w.realisation]
    sentence = " ".join(reas)
    assert sentence == u"Je vais à la pêche au poisson"
