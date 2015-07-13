# encoding: utf-8

"""Test suite of the french morphology rules."""

import pytest

from ..morphology.fr import FrenchMorphologyRules
from ..lexicon.feature.category import ADJECTIVE
from ..lexicon.feature.lexical import GENDER
from ..lexicon.feature import NUMBER, IS_COMPARATIVE
from ..lexicon.feature.gender import MASCULINE, FEMININE
from ..lexicon.feature.number import PLURAL, SINGULAR


@pytest.fixture
def morph_rules_fr():
    return FrenchMorphologyRules()


@pytest.mark.parametrize('s, expected', [
    (u'actuel', u'actuelle'),
    (u'vieil', u'vieille'),
    (u'bas', u'basse'),
    (u'musicien', u'musicienne'),
    (u'mignon', u'mignonne'),
    (u'violet', u'violette'),
    (u'affectueux', u'affectueuse'),
    (u'premier', u'première'),
    (u'amer', u'amère'),
    (u'beau', u'belle'),
    (u'gros', u'grosse'),
    (u'aigu', u'aiguë'),
    (u'long', u'longue'),
    (u'migrateur', u'migratrice'),
    (u'actif', u'active'),
    (u'affairé', u'affairée'),
    (u'abondant', u'abondante'),
])
def test_feminize(lexicon_fr, morph_rules_fr, s, expected):
    word = lexicon_fr.first(s, category=ADJECTIVE)
    word.feminine_singular = ''  # make sure all static rules are tested
    feminine_form = morph_rules_fr.feminize_singular_element(
        word, word.realisation)
    assert feminine_form == expected


@pytest.mark.parametrize('s, expected', [
    (u'bas', u'bas'),
    (u'vieux', u'vieux'),
    (u'nez', u'nez'),
    (u'tuyau', u'tuyaux'),
    (u'cheveu', u'cheveux'),
    (u'cheval', u'chevaux'),
    (u'main', u'mains'),
])
def test_pluralize(morph_rules_fr, s, expected):
    assert morph_rules_fr.pluralize(s) == expected


@pytest.mark.parametrize('word, features, expected', [
    (u'ce', {GENDER: MASCULINE}, u'ce'),
    (u'ce', {GENDER: FEMININE}, u'cette'),
    (u'ce', {GENDER: MASCULINE, NUMBER: PLURAL}, u'ces'),
    (u'tout', {GENDER: MASCULINE}, u'tout'),
    (u'tout', {GENDER: FEMININE}, u'toute'),
    (u'tout', {GENDER: MASCULINE, NUMBER: PLURAL}, u'tous les'),
    (u'tout', {GENDER: FEMININE, NUMBER: PLURAL}, u'toutes les'),
    (u'ce -ci', {GENDER: MASCULINE}, u'ce'),
    (u'ce -ci', {GENDER: FEMININE}, u'cette'),
    (u'ce -ci', {GENDER: MASCULINE, NUMBER: PLURAL}, u'ces'),
])
def test_morph_determiner(lexicon_fr, morph_rules_fr, word, features, expected):
    element = lexicon_fr.first(word)
    for k, v in features.iteritems():
        element.features[k] = v
    inflected_form = morph_rules_fr.morph_determiner(element)
    assert inflected_form.realisation == expected


@pytest.mark.incomplete(
    'The whole part about parent and lineage has NOT been tested '
    'The tester needs to build a PhraseElement, with some parentage, '
    'and then morph an adjective in the PhraseElement.')
@pytest.mark.parametrize('word, features, expected', [
    (u'bon', {IS_COMPARATIVE: True}, u'meilleur'),
    (u'bon', {IS_COMPARATIVE: True, GENDER: FEMININE}, u'meilleure'),
    (u'bon', {IS_COMPARATIVE: True, GENDER: FEMININE, NUMBER: PLURAL},
     u'meilleures'),
])
def test_morph_adjective(lexicon_fr, morph_rules_fr, word, features, expected):
    element = lexicon_fr.first(word)
    for k, v in features.iteritems():
        element.features[k] = v
    inflected_form = morph_rules_fr.morph_adjective(element)
    assert inflected_form.realisation == expected


@pytest.mark.parametrize('word, base_word, features, expected', [
    # No transformation
    (u'voiture', u'voiture', {}, u'voiture'),
    # Simple pluralisation based on plural feature of base word
    (u'voiture', u'voiture', {NUMBER: PLURAL}, u'voitures'),
    # PLuralisation based on plural feature of base word
    (u'oeil', u'oeil', {NUMBER: PLURAL}, u'yeux'),
    # No idea what I'm doing
    (u'gars', u'fille', {GENDER: MASCULINE}, u'garçon'),
    # Simple pluralisation using +s rule, because word is not
    # in lexicon
    (u'clavier', u'clavier', {NUMBER: PLURAL}, u'claviers'),
    (u'directeur', u'directeur', {NUMBER: PLURAL, GENDER: FEMININE}, u'directrices'),
])
def test_morph_noun(lexicon_fr, morph_rules_fr, word, base_word, features, expected):
    base_word = lexicon_fr.first(base_word)
    element = lexicon_fr.first(word)
    for k, v in features.iteritems():
        element.features[k] = v
    inflected_form = morph_rules_fr.morph_noun(element, base_word)
    assert inflected_form.realisation == expected


@pytest.mark.parametrize('word, base_word, features, expected', [
    (u'bientôt', u'bientôt', {}, u'bientôt'),
    (u'bien', u'bien', {IS_COMPARATIVE: True}, u'mieux'),
    # bientôt does not compare
    (u'bientôt', u'bientôt', {IS_COMPARATIVE: True}, u'bientôt'),
])
def test_morph_adverb(lexicon_fr, morph_rules_fr, word, base_word, features, expected):
    base_word = lexicon_fr.first(base_word)
    element = lexicon_fr.first(word)
    for k, v in features.iteritems():
        element.features[k] = v
    inflected_form = morph_rules_fr.morph_adverb(element, base_word)
    assert inflected_form.realisation == expected
