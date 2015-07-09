# encoding: utf-8

"""Test suite of the French phrase helper classes."""

import pytest

from ..syntax.phrase.fr import FrenchNounPhraseHelper
from ..spec.phrase import PhraseElement
from ..spec.word import InflectedWordElement
from ..lexicon.feature.category import NOUN_PHRASE
from ..lexicon.feature.person import FIRST, SECOND, THIRD
from ..lexicon.feature.gender import MASCULINE, FEMININE
from ..lexicon.feature.number import SINGULAR, PLURAL


@pytest.fixture
def noun_helper_fr(lexicon_fr):
    phrase = PhraseElement(category=NOUN_PHRASE, lexicon=lexicon_fr)
    return FrenchNounPhraseHelper(phrase=phrase)


@pytest.mark.parametrize('person, number, gender, expected', [
    (FIRST, SINGULAR, MASCULINE, u'je'),
    (SECOND, SINGULAR, MASCULINE, u'tu'),
    (THIRD, SINGULAR, MASCULINE, u'il'),
    (THIRD, SINGULAR, FEMININE, u'elle'),
    (FIRST, PLURAL, MASCULINE, u'nous'),
    (SECOND, PLURAL, MASCULINE, u'vous'),
    (THIRD, PLURAL, MASCULINE, u'ils'),
    (THIRD, PLURAL, FEMININE, u'elles'),
])
def test_create_pronoun(noun_helper_fr, person, number, gender, expected):
    noun_helper_fr.phrase.person = person
    noun_helper_fr.phrase.number = number
    noun_helper_fr.phrase.gender = gender
    pronoun = noun_helper_fr.create_pronoun()
    assert isinstance(pronoun, InflectedWordElement)
    assert pronoun.base_form == expected
