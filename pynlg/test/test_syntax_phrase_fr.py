# encoding: utf-8

"""Test suite of the French phrase helper classes."""

import pytest

from ..syntax.phrase.fr import FrenchNounPhraseHelper
from ..spec.phrase import PhraseElement, AdjectivePhraseElement
from ..spec.word import InflectedWordElement, WordElement
from ..spec.string import StringElement
from ..lexicon.lang import FRENCH
from ..lexicon.feature.category import NOUN_PHRASE, ADJECTIVE
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


@pytest.mark.parametrize('word, expected', [
    (None, False),
    (WordElement(base_form=u'premier'), False),
    (WordElement(base_form=u'second'), False),
    (WordElement(base_form=u'dernier'), False),
    (WordElement(base_form=u'deuxième'), True),
    (StringElement(string=u'premier', language=FRENCH), False),
    (StringElement(string=u'second', language=FRENCH), False),
    (StringElement(string=u'dernier', language=FRENCH), False),
    (StringElement(string=u'deuxième', language=FRENCH), True),
])
def test_is_ordinal(word, expected):
    assert FrenchNounPhraseHelper.is_ordinal(word) is expected


def test_add_null_modifier(lexicon_fr, noun_helper_fr, mocker):
    mocker.patch.object(PhraseElement, 'add_pre_modifier', autospec=True)
    mocker.patch.object(PhraseElement, 'add_post_modifier', autospec=True)
    noun_helper_fr.add_modifier(None)
    assert noun_helper_fr.phrase.add_pre_modifier.call_count == 0
    assert noun_helper_fr.phrase.add_post_modifier.call_count == 0


def test_add_post_modifier_word_element(lexicon_fr, noun_helper_fr):
    adj = lexicon_fr.first(u'meilleur', category=ADJECTIVE)
    noun_helper_fr.add_modifier(adj)
    assert not noun_helper_fr.phrase.premodifiers
    assert isinstance(noun_helper_fr.phrase.postmodifiers[0], WordElement)
    assert noun_helper_fr.phrase.postmodifiers[0].base_form == u'meilleur'


def test_add_post_modifier_unknown_string_element(lexicon_fr, noun_helper_fr):
    assert u'badass' not in lexicon_fr
    noun_helper_fr.add_modifier(u'badass')
    assert u'badass' in lexicon_fr
    assert isinstance(noun_helper_fr.phrase.postmodifiers[0], WordElement)
    assert not noun_helper_fr.phrase.premodifiers
    assert noun_helper_fr.phrase.postmodifiers[0].base_form == u'badass'


def test_add_post_modifier_unknown_complex_string_element(lexicon_fr, noun_helper_fr):
    assert u'totalement badass' not in lexicon_fr
    noun_helper_fr.add_modifier(u'totalement badass')
    assert u'totalement badass' not in lexicon_fr
    assert isinstance(noun_helper_fr.phrase.postmodifiers[0], StringElement)
    assert not noun_helper_fr.phrase.premodifiers
    assert noun_helper_fr.phrase.postmodifiers[0].realisation == u'totalement badass'


def test_add_pre_modifier_ordinal_word(lexicon_fr, noun_helper_fr):
    adj = lexicon_fr.first(u'deuxième', category=ADJECTIVE)
    noun_helper_fr.add_modifier(adj)
    assert isinstance(noun_helper_fr.phrase.premodifiers[0], WordElement)
    assert noun_helper_fr.phrase.premodifiers[0].base_form == u'deuxième'
    assert not noun_helper_fr.phrase.postmodifiers


def test_add_pre_modifier_inflected_word(lexicon_fr, noun_helper_fr):
    word = lexicon_fr.first(u'même')  # meme is preposed
    infl = word.inflex(number='plural')
    noun_helper_fr.add_modifier(infl)
    assert isinstance(noun_helper_fr.phrase.premodifiers[0], WordElement)
    assert noun_helper_fr.phrase.premodifiers[0] == infl.base_word
    assert not noun_helper_fr.phrase.postmodifiers


@pytest.mark.parametrize('word', [
    u'deuxième',  # ordinal
    u'même'  # preposed
])
def test_add_pre_modifier_adjective_phrase(lexicon_fr, noun_helper_fr, word):
    adj_phrase = AdjectivePhraseElement(lexicon_fr)
    adj = lexicon_fr.first(word, category=ADJECTIVE)
    adj_phrase.head = adj
    noun_helper_fr.add_modifier(adj_phrase)
    assert noun_helper_fr.phrase.premodifiers[0] == adj_phrase
    assert not noun_helper_fr.phrase.postmodifiers
