# encoding: utf-8

"""Test suite of the french morphology rules."""

import pytest

from ..morphology.fr import FrenchMorphologyRules
from ..spec.phrase import PhraseElement
from ..spec.string import StringElement
from ..lexicon.feature.category import ADJECTIVE, VERB_PHRASE, NOUN_PHRASE, VERB
from ..lexicon.feature.lexical import GENDER
from ..lexicon.feature import NUMBER, IS_COMPARATIVE
from ..lexicon.feature.gender import MASCULINE, FEMININE
from ..lexicon.feature.number import PLURAL, SINGULAR, BOTH
from ..lexicon.feature.discourse import OBJECT, PRE_MODIFIER, FRONT_MODIFIER, POST_MODIFIER
from ..lexicon.feature.internal import DISCOURSE_FUNCTION, COMPLEMENTS
from ..lexicon.feature.person import FIRST, SECOND, THIRD
from ..lexicon.feature.tense import PRESENT, PAST, FUTURE, CONDITIONAL
from ..lexicon.feature.form import (
    BARE_INFINITIVE, SUBJUNCTIVE, GERUND, INFINITIVE,
    PRESENT_PARTICIPLE, PAST_PARTICIPLE, INDICATIVE, IMPERATIVE)
from ..lexicon.feature import PERSON, TENSE, FORM


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
    for k, v in features.items():
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
    for k, v in features.items():
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
    for k, v in features.items():
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
    for k, v in features.items():
        element.features[k] = v
    inflected_form = morph_rules_fr.morph_adverb(element, base_word)
    assert inflected_form.realisation == expected


def test_get_verb_parent(lexicon_fr, morph_rules_fr):
    verb = lexicon_fr.first(u'avoir')
    parent, agreement = morph_rules_fr.get_verb_parent(verb)
    assert parent is None
    assert agreement is False


def test_get_verb_parent2(lexicon_fr, morph_rules_fr):
    verb = lexicon_fr.first(u'avoir')
    p = PhraseElement(lexicon=lexicon_fr, category=VERB_PHRASE)
    verb.parent = p
    parent, agreement = morph_rules_fr.get_verb_parent(verb)
    assert parent == p
    assert agreement is True


def test_get_verb_parent3(lexicon_fr, morph_rules_fr):
    verb = lexicon_fr.first(u'avoir')
    p = PhraseElement(lexicon=lexicon_fr, category=VERB_PHRASE)
    verb.parent = p
    gp = PhraseElement(lexicon=lexicon_fr, category=VERB_PHRASE)
    gp.gender = FEMININE
    parent, agreement = morph_rules_fr.get_verb_parent(verb)
    assert parent == gp
    assert agreement is True


@pytest.mark.parametrize('mod_func', [FRONT_MODIFIER, PRE_MODIFIER, POST_MODIFIER])
def test_get_verb_parent4(lexicon_fr, morph_rules_fr, mod_func):
    verb = lexicon_fr.first(u'avoir')
    verb.features[DISCOURSE_FUNCTION] = mod_func
    p = PhraseElement(lexicon=lexicon_fr, category=NOUN_PHRASE)
    verb.parent = p
    parent, agreement = morph_rules_fr.get_verb_parent(verb)
    assert parent == p
    assert agreement is True


@pytest.mark.parametrize('mod_func', [FRONT_MODIFIER, PRE_MODIFIER, POST_MODIFIER])
def test_get_verb_parent5(lexicon_fr, morph_rules_fr, mod_func):
    verb = lexicon_fr.first(u'avoir')
    verb.features[DISCOURSE_FUNCTION] = mod_func
    p = PhraseElement(lexicon=lexicon_fr, category=NOUN_PHRASE)
    w = lexicon_fr.first(u'cheval')
    w.features[DISCOURSE_FUNCTION] = OBJECT
    p.features[COMPLEMENTS] = [w]
    verb.parent = p
    parent, agreement = morph_rules_fr.get_verb_parent(verb)
    assert parent == w
    assert agreement is True


@pytest.mark.parametrize('verb, radical, number, group', [
    (u'aimer', u'aim', SINGULAR, 1),
    (u'aimer', u'aim', PLURAL, 1),
    (u'choir', u'choi', SINGULAR, 2),
    (u'choir', u'choy', PLURAL, 2),
    (u'finir', u'fini', SINGULAR, 2),
    (u'finir', u'finiss', PLURAL, 2),
    (u'haïr', u'hai', SINGULAR, 2),
    (u'haïr', u'haïss', PLURAL, 2),
    (u'vendre', u'vend', SINGULAR, 3),
    (u'vendre', u'vend', PLURAL, 3),
    (u'mettre', u'met', SINGULAR, 3),
    (u'mettre', u'mett', PLURAL, 3),
])
def test_get_present_radical(morph_rules_fr, verb, radical, number, group):
    verb_tuple = morph_rules_fr.get_present_radical(verb, number)
    assert verb_tuple.radical == radical
    assert verb_tuple.group == group


def test_get_present_radical_unrecognized_verb(morph_rules_fr):
    with pytest.raises(ValueError):
        morph_rules_fr.get_present_radical(u'plop', SINGULAR)


@pytest.mark.parametrize('base_form, person, number, expected', [
    (u'aimer', FIRST, SINGULAR, u'aime'),
    (u'aimer', SECOND, SINGULAR, u'aimes'),
    (u'aimer', THIRD, SINGULAR, u'aime'),
    (u'aimer', FIRST, PLURAL, u'aimons'),
    (u'aimer', SECOND, PLURAL, u'aimez'),
    (u'aimer', THIRD, PLURAL, u'aiment'),
    (u'finir', FIRST, SINGULAR, u'finis'),
    (u'finir', SECOND, SINGULAR, u'finis'),
    (u'finir', THIRD, SINGULAR, u'finit'),
    (u'finir', FIRST, PLURAL, u'finissons'),
    (u'finir', SECOND, PLURAL, u'finissez'),
    (u'finir', THIRD, PLURAL, u'finissent'),
    (u'voir', FIRST, SINGULAR, u'vois'),
    (u'voir', SECOND, SINGULAR, u'vois'),
    (u'voir', THIRD, SINGULAR, u'voit'),
    (u'voir', FIRST, PLURAL, u'voyons'),
    (u'voir', SECOND, PLURAL, u'voyez'),
    (u'voir', THIRD, PLURAL, u'voient'),
    (u'haïr', FIRST, SINGULAR, u'hais'),
    (u'haïr', SECOND, SINGULAR, u'hais'),
    (u'haïr', THIRD, SINGULAR, u'hait'),
    (u'haïr', FIRST, PLURAL, u'haïssons'),
    (u'haïr', SECOND, PLURAL, u'haïssez'),
    (u'haïr', THIRD, PLURAL, u'haïssent'),
    (u'vendre', FIRST, SINGULAR, u'vends'),
    (u'vendre', SECOND, SINGULAR, u'vends'),
    (u'vendre', THIRD, SINGULAR, u'vend'),
    (u'vendre', FIRST, PLURAL, u'vendons'),
    (u'vendre', SECOND, PLURAL, u'vendez'),
    (u'vendre', THIRD, PLURAL, u'vendent'),
])
def test_build_present_verb(morph_rules_fr, base_form, person, number, expected):
    assert morph_rules_fr.build_present_verb(base_form, person, number) == expected


def test_imperfect_pres_part_radical_elt_has_imparfait_radical(lexicon_fr, morph_rules_fr):
    verb = lexicon_fr.first(u'être', category=VERB)
    radical = morph_rules_fr.get_imperfect_pres_part_radical(
        verb, base_word=None, base_form=u'être')
    assert radical == u'ét'


def test_imperfect_pres_part_radical_elt_has_no_imparfait_radical(
        lexicon_fr, morph_rules_fr):
    verb = lexicon_fr.first(u'être', category=VERB)
    infl_verb = verb.inflex(verb, person=FIRST)
    infl_verb.features = {}
    radical = morph_rules_fr.get_imperfect_pres_part_radical(
        infl_verb, base_word=verb, base_form=u'être')
    assert radical == u'ét'


def test_imperfect_pres_part_radical_elt_has_person1s(lexicon_fr, morph_rules_fr):
    verb = lexicon_fr.first(u'avoir', category=VERB)
    radical = morph_rules_fr.get_imperfect_pres_part_radical(
        verb, base_word=verb, base_form=u'avoir')
    assert radical == u'av'


def test_imperfect_pres_part_radical_base_word_has_person1s(
        lexicon_fr, morph_rules_fr):
    verb = lexicon_fr.first(u'avoir', category=VERB)
    infl_verb = verb.inflex(verb, person=FIRST)
    infl_verb.features = {}
    radical = morph_rules_fr.get_imperfect_pres_part_radical(
        infl_verb, base_word=verb, base_form=u'avoir')
    assert radical == u'av'


def test_imperfect_pres_part_radical_unexisting_verb(
        lexicon_fr, morph_rules_fr):
    verb = lexicon_fr.first(u'kiffer', category=VERB)  # will be inserted
    infl_verb = verb.inflex(verb, person=FIRST)
    infl_verb.features = {}
    radical = morph_rules_fr.get_imperfect_pres_part_radical(
        infl_verb, base_word=verb, base_form=u'kiffer')
    assert radical == u'kiff'


@pytest.mark.parametrize('gender, number, expected', [
    (MASCULINE, SINGULAR, u'amusant'),
    (FEMININE, SINGULAR, u'amusante'),
    (MASCULINE, PLURAL, u'amusants'),
    (FEMININE, PLURAL, u'amusantes'),
])
def test_realise_verb_participle_or_gerund_used_as_adjective(
        lexicon_fr, morph_rules_fr, gender, number, expected):
    verb = lexicon_fr.first(u'amuser', category=VERB)
    gerund_or_present_part = morph_rules_fr.realise_verb_present_participle_or_gerund(
        verb, base_word=verb, base_form=u'amuser', gender=gender, number=number)
    assert gerund_or_present_part == expected


def test_realise_verb_participle_or_gerund(lexicon_fr, morph_rules_fr):
    verb = lexicon_fr.first(u'être', category=VERB)
    gerund_or_present_part = morph_rules_fr.realise_verb_present_participle_or_gerund(
        verb, base_word=verb, base_form=u'être', gender=None, number=None)
    assert gerund_or_present_part == u'étant'


@pytest.mark.parametrize('base_form, expected', [
    (u'manger', u'mangé'),
    (u'vouloir', u'voulu'),
    (u'finir', u'fini'),
    (u'permettre', u'permis'),
    (u'vendre', u'vendu'),
])
def test_build_verb_past_participle(morph_rules_fr, base_form, expected):
    assert morph_rules_fr.build_verb_past_participle(base_form) == expected


@pytest.mark.parametrize('base_form, gender, number, expected', [
    (u'être', None, None, u'été'),
    (u'kiffer', None, None, u'kiffé'),
    (u'manger', FEMININE, SINGULAR, u'mangée'),
    (u'manger', FEMININE, PLURAL, u'mangées'),
    (u'abattre', FEMININE, SINGULAR, u'abattue'),  # has a feminine past participle
    (u'abattre', FEMININE, PLURAL, u'abattues'),  # idem
])
def test_realise_verb_past_participle(
        lexicon_fr, morph_rules_fr, base_form, gender, number, expected):
    verb = lexicon_fr.first(base_form, category=VERB)
    past_participle = morph_rules_fr.realise_verb_past_participle(
        verb, base_word=verb, base_form=base_form, gender=gender, number=number)
    assert past_participle == expected


@pytest.mark.parametrize('base_form, person, number, expected', [
    (u'aimer', FIRST, SINGULAR, u'aime'),
    (u'aimer', SECOND, SINGULAR, u'aimes'),
    (u'aimer', THIRD, SINGULAR, u'aime'),
    (u'aimer', FIRST, BOTH, u'aime'),
    (u'aimer', SECOND, BOTH, u'aimes'),
    (u'aimer', THIRD, BOTH, u'aime'),
    (u'aimer', FIRST, PLURAL, u'aimions'),
    (u'aimer', SECOND, PLURAL, u'aimiez'),
    (u'aimer', THIRD, PLURAL, u'aiment'),
])
def test_build_subjunctive_verb(morph_rules_fr, base_form, person, number, expected):
    assert morph_rules_fr.build_subjunctive_verb(base_form, person, number) == expected


@pytest.mark.parametrize('base_form, person, number, expected', [
    # irregular, from lexicon
    (u'aller', FIRST, SINGULAR, u'aille'),
    (u'aller', SECOND, SINGULAR, u'ailles'),
    (u'aller', THIRD, SINGULAR, u'aille'),
    (u'aller', FIRST, BOTH, u'aille'),
    (u'aller', SECOND, BOTH, u'ailles'),
    (u'aller', THIRD, BOTH, u'aille'),
    (u'aller', FIRST, PLURAL, u'allions'),
    (u'aller', SECOND, PLURAL, u'alliez'),
    (u'aller', THIRD, PLURAL, u'aillent'),
    # regular, from building rules
    (u'aimer', FIRST, SINGULAR, u'aime'),
    (u'aimer', SECOND, SINGULAR, u'aimes'),
    (u'aimer', THIRD, SINGULAR, u'aime'),
    (u'aimer', FIRST, BOTH, u'aime'),
    (u'aimer', SECOND, BOTH, u'aimes'),
    (u'aimer', THIRD, BOTH, u'aime'),
    (u'aimer', FIRST, PLURAL, u'aimions'),
    (u'aimer', SECOND, PLURAL, u'aimiez'),
    (u'aimer', THIRD, PLURAL, u'aiment'),
])
def test_realise_verb_subjunctive(
        lexicon_fr, morph_rules_fr, base_form, person, number, expected):
    verb = lexicon_fr.first(base_form, category=VERB)
    subj = morph_rules_fr.realise_verb_subjunctive(
        verb, base_word=verb, base_form=base_form, number=number, person=person)
    assert subj == expected


@pytest.mark.parametrize('base_form, person, number, expected', [
    (u'aller', FIRST, SINGULAR, None),
    (u'aller', SECOND, SINGULAR, u'va'),
    (u'aller', THIRD, SINGULAR, None),
    (u'aller', FIRST, BOTH, None),
    (u'aller', SECOND, BOTH, u'va'),
    (u'aller', THIRD, BOTH, None),
    (u'aller', FIRST, PLURAL, u'allons'),
    (u'aller', SECOND, PLURAL, u'allez'),
    (u'aller', THIRD, PLURAL, None),
    (u'manger', FIRST, SINGULAR, None),
    (u'manger', SECOND, SINGULAR, u'mange'),
    (u'manger', THIRD, SINGULAR, None),
    (u'manger', FIRST, BOTH, None),
    (u'manger', SECOND, BOTH, u'mange'),
    (u'manger', THIRD, BOTH, None),
    (u'manger', FIRST, PLURAL, u'mangeons'),
    (u'manger', SECOND, PLURAL, u'mangez'),
    (u'manger', THIRD, PLURAL, None),
])
def test_realise_verb_imperative(
        lexicon_fr, morph_rules_fr, base_form, person, number, expected):
    verb = lexicon_fr.first(base_form, category=VERB)
    imp = morph_rules_fr.realise_verb_imperative(
        verb, base_word=verb, base_form=base_form, number=number, person=person)
    assert imp == expected


@pytest.mark.parametrize('base_form, person, number, expected', [
    # irregular: from lexicon
    (u'aller', FIRST, SINGULAR, u'vais'),
    (u'aller', SECOND, SINGULAR, u'vas'),
    (u'aller', THIRD, SINGULAR, u'va'),
    (u'aller', FIRST, BOTH, u'vais'),
    (u'aller', SECOND, BOTH, u'vas'),
    (u'aller', THIRD, BOTH, u'va'),
    (u'aller', FIRST, PLURAL, u'allons'),
    (u'aller', SECOND, PLURAL, u'allez'),
    (u'aller', THIRD, PLURAL, u'vont'),
    # regular: from rules
    (u'vendre', FIRST, SINGULAR, u'vends'),
    (u'vendre', SECOND, SINGULAR, u'vends'),
    (u'vendre', THIRD, SINGULAR, u'vend'),
    (u'vendre', FIRST, BOTH, u'vends'),
    (u'vendre', SECOND, BOTH, u'vends'),
    (u'vendre', THIRD, BOTH, u'vend'),
    (u'vendre', FIRST, PLURAL, u'vendons'),
    (u'vendre', SECOND, PLURAL, u'vendez'),
    (u'vendre', THIRD, PLURAL, u'vendent'),
])
def test_realise_verb_present(
        lexicon_fr, morph_rules_fr, base_form, person, number, expected):
    verb = lexicon_fr.first(base_form, category=VERB)
    imp = morph_rules_fr.realise_verb_present(
        verb, base_word=verb, base_form=base_form, number=number, person=person)
    assert imp == expected


@pytest.mark.parametrize('word, expected', [
    (u'envoyer', u'enverr'),  # has a future_radical feature
    (u'employer', u'emploier'),  # ends with 'yer'
    (u'amener', u'amèn'),
    (u'manger', u'manger'),  # does not correspond to anything special
])
def test_get_conditional_or_future_radical(lexicon_fr, morph_rules_fr, word, expected):
    verb = lexicon_fr.first(word, category=VERB)
    radical = morph_rules_fr.get_conditional_or_future_radical(
        verb, base_form=word, base_word=verb)
    assert radical == expected


@pytest.mark.parametrize('radical, person, number, expected', [
    (u'aimer', FIRST, SINGULAR, u'aimerai'),
    (u'aimer', SECOND, SINGULAR, u'aimeras'),
    (u'aimer', THIRD, SINGULAR, u'aimera'),
    (u'aimer', FIRST, BOTH, u'aimerai'),
    (u'aimer', SECOND, BOTH, u'aimeras'),
    (u'aimer', THIRD, BOTH, u'aimera'),
    (u'aimer', FIRST, PLURAL, u'aimerons'),
    (u'aimer', SECOND, PLURAL, u'aimerez'),
    (u'aimer', THIRD, PLURAL, u'aimeront'),
])
def test_build_verb_future(morph_rules_fr, radical, person, number, expected):
    future = morph_rules_fr.build_future_verb(radical=radical, number=number, person=person)
    assert future == expected


@pytest.mark.parametrize('radical, person, number, expected', [
    (u'aimer', FIRST, SINGULAR, u'aimerais'),
    (u'aimer', SECOND, SINGULAR, u'aimerais'),
    (u'aimer', THIRD, SINGULAR, u'aimerait'),
    (u'aimer', FIRST, BOTH, u'aimerais'),
    (u'aimer', SECOND, BOTH, u'aimerais'),
    (u'aimer', THIRD, BOTH, u'aimerait'),
    (u'aimer', FIRST, PLURAL, u'aimerions'),
    (u'aimer', SECOND, PLURAL, u'aimeriez'),
    (u'aimer', THIRD, PLURAL, u'aimeraient'),
])
def test_build_verb_conditional(morph_rules_fr, radical, person, number, expected):
    cond = morph_rules_fr.build_conditional_verb(
        radical=radical, number=number, person=person)
    assert cond == expected


@pytest.mark.parametrize('radical, person, number, expected', [
    (u'aimer', FIRST, SINGULAR, u'aimerais'),
    (u'aimer', SECOND, SINGULAR, u'aimerais'),
    (u'aimer', THIRD, SINGULAR, u'aimerait'),
    (u'aimer', FIRST, BOTH, u'aimerais'),
    (u'aimer', SECOND, BOTH, u'aimerais'),
    (u'aimer', THIRD, BOTH, u'aimerait'),
    (u'aimer', FIRST, PLURAL, u'aimerions'),
    (u'aimer', SECOND, PLURAL, u'aimeriez'),
    (u'aimer', THIRD, PLURAL, u'aimeraient'),
])
def test_build_verb_past(morph_rules_fr, radical, person, number, expected):
    past = morph_rules_fr.build_past_verb(
        radical=radical, number=number, person=person)
    assert past == expected


@pytest.mark.parametrize('word, tense, form, gender, person, number, expected', [
    (u'aimer', PRESENT, INDICATIVE, None, FIRST, SINGULAR, u'aime'),
    (u'aimer', PRESENT, INDICATIVE, MASCULINE, FIRST, SINGULAR, u'aime'),
    (u'aimer', FUTURE, INDICATIVE, MASCULINE, FIRST, SINGULAR, u'aimerai'),
    (u'aimer', PAST, INDICATIVE, MASCULINE, FIRST, SINGULAR, u'aimais'),
    (u'aimer', CONDITIONAL, INDICATIVE, MASCULINE, FIRST, SINGULAR, u'aimerais'),
    (u'aimer', None, BARE_INFINITIVE, MASCULINE, FIRST, SINGULAR, u'aimer'),
    (u'aimer', None, INFINITIVE, MASCULINE, FIRST, SINGULAR, u'aimer'),
    (u'aimer', None, PRESENT_PARTICIPLE, None, FIRST, SINGULAR, u'aimant'),
    (u'aimer', None, PRESENT_PARTICIPLE, MASCULINE, FIRST, SINGULAR, u'aimant'),
    (u'aimer', None, PRESENT_PARTICIPLE, FEMININE, FIRST, SINGULAR, u'aimante'),
    (u'aimer', None, GERUND, None, FIRST, SINGULAR, u'aimant'),
    (u'aimer', None, GERUND, MASCULINE, FIRST, SINGULAR, u'aimant'),
    (u'aimer', None, GERUND, FEMININE, FIRST, SINGULAR, u'aimante'),
    (u'aimer', None, PAST_PARTICIPLE, None, FIRST, SINGULAR, u'aimé'),
    (u'aimer', None, PAST_PARTICIPLE, MASCULINE, FIRST, SINGULAR, u'aimé'),
    (u'aimer', None, PAST_PARTICIPLE, FEMININE, FIRST, SINGULAR, u'aimée'),
    (u'aimer', None, SUBJUNCTIVE, FEMININE, FIRST, SINGULAR, u'aime'),
    (u'aimer', None, IMPERATIVE, FEMININE, FIRST, PLURAL, u'aimons'),
])
def test_morph_verb(
        lexicon_fr, morph_rules_fr, word, tense, form, gender, person, number, expected):
    verb = lexicon_fr.first(word, category=VERB)
    verb.features.update({
        GENDER: gender,
        TENSE: tense,
        NUMBER: number,
        PERSON: person,
        FORM: form,
    })
    realised = morph_rules_fr.morph_verb(verb, base_word=verb)
    assert isinstance(realised, StringElement)
    assert realised.realisation == expected
