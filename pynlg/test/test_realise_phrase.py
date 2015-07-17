# encoding: utf-8

"""Test suite of phrase realisation"""

from ..lexicon.feature.number import PLURAL
from ..lexicon.feature.gender import FEMININE
from ..lexicon.feature import NUMBER
from ..lexicon.feature.lexical import GENDER
from ..lexicon.feature.category import DETERMINER, NOUN, ADJECTIVE
from .. import make_noun_phrase


def test_realise_noun_phrase_feminine_singular(lexicon_fr):
    un = lexicon_fr.first(u'un', category=DETERMINER)
    une = un.inflex(gender=FEMININE)
    maison = lexicon_fr.first(u'maison', category=NOUN)
    beau = lexicon_fr.first(u'beau', category=ADJECTIVE)
    belle = beau.inflex(gender=FEMININE)
    perdu = lexicon_fr.first(u'perdu', category=ADJECTIVE)
    perdue = perdu.inflex(gender=FEMININE)
    phrase = make_noun_phrase(
        lexicon=lexicon_fr, specifier=une, noun=maison, modifiers=[belle, perdue])
    phrase = phrase.realise()
    phrase = phrase.realise_morphology()
    assert phrase.components[0].realisation == u'une'
    assert phrase.components[1].realisation == u'belle'
    assert phrase.components[2].realisation == u'maison'
    assert phrase.components[3].realisation == u'perdue'


def test_realise_noun_phrase_feminine_plural(lexicon_fr):
    un = lexicon_fr.first(u'un', category=DETERMINER)
    des = un.inflex(gender=FEMININE, number=PLURAL)
    maison = lexicon_fr.first(u'maison', category=NOUN)
    maisons = maison.inflex(gender=FEMININE, number=PLURAL)
    beau = lexicon_fr.first(u'beau', category=ADJECTIVE)
    belles = beau.inflex(gender=FEMININE, number=PLURAL)
    perdu = lexicon_fr.first(u'perdu', category=ADJECTIVE)
    perdues = perdu.inflex(gender=FEMININE, number=PLURAL)
    phrase = make_noun_phrase(
        lexicon=lexicon_fr, specifier=des, noun=maisons, modifiers=[belles, perdues])
    phrase = phrase.realise()
    phrase = phrase.realise_morphology()
    assert phrase.components[0].realisation == u'des'
    assert phrase.components[1].realisation == u'belles'
    assert phrase.components[2].realisation == u'maisons'
    assert phrase.components[3].realisation == u'perdues'


def test_realise_noun_phrase_features_on_parent(lexicon_fr):
    un = lexicon_fr.first(u'un', category=DETERMINER)
    maison = lexicon_fr.first(u'maison', category=NOUN)
    beau = lexicon_fr.first(u'beau', category=ADJECTIVE)
    perdu = lexicon_fr.first(u'perdu', category=ADJECTIVE)
    phrase = make_noun_phrase(
        lexicon=lexicon_fr, specifier=un, noun=maison, modifiers=[beau, perdu])
    phrase = phrase.realise()
    phrase.features[GENDER] = FEMININE
    phrase.features[NUMBER] = PLURAL
    phrase = phrase.realise_morphology()
    assert phrase.components[0].realisation == u'des'
    assert phrase.components[1].realisation == u'belles'
    assert phrase.components[2].realisation == u'maisons'
    assert phrase.components[3].realisation == u'perdues'
