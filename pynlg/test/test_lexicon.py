# encoding: utf-8

"""Test suite of the lexicon package"""

import pytest

from xml.etree import cElementTree as ET

from ..lexicon.fr import FrenchLexicon
from ..lexicon.en import EnglishLexicon
from ..lexicon.feature.category import NOUN, VERB, ANY, DETERMINER, ADJECTIVE, ADVERB
from ..lexicon.feature.lexical import (COMPARATIVE, SUPERLATIVE, PREDICATIVE,
                                       QUALITATIVE)
from ..spec.word import WordElement


def _list(x):
    return [x] if not isinstance(x, list) else x


def test_lexicon_supported_languages():
    assert FrenchLexicon(auto_index=False).lexicon_filepath
    assert EnglishLexicon(auto_index=False).lexicon_filepath


@pytest.fixture
def word_node():
    """Return an XML tree representing a word node."""
    word_node = ET.Element('word')
    ET.SubElement(word_node, 'base').text = u'être'
    ET.SubElement(word_node, 'category').text = u'verb'
    ET.SubElement(word_node, 'id').text = u'E0012152'
    ET.SubElement(word_node, 'present1s').text = u'suis'
    ET.SubElement(word_node, 'present2s').text = u'es'
    ET.SubElement(word_node, 'present3s').text = u'est'
    ET.SubElement(word_node, 'present1p').text = u'sommes'
    ET.SubElement(word_node, 'present2p').text = u'êtes'
    ET.SubElement(word_node, 'present3p').text = u'sont'
    ET.SubElement(word_node, 'imperative2s').text = u'sois'
    ET.SubElement(word_node, 'imperative1p').text = u'soyons'
    ET.SubElement(word_node, 'imperative2p').text = u'soyez'
    ET.SubElement(word_node, 'future_radical').text = u'ser'
    ET.SubElement(word_node, 'imparfait_radical').text = u'êt'
    ET.SubElement(word_node, 'pastParticiple').text = u'été'
    ET.SubElement(word_node, 'presentParticiple').text = u'étant'
    ET.SubElement(word_node, 'subjunctive1s').text = u'sois'
    ET.SubElement(word_node, 'subjunctive2s').text = u'sois'
    ET.SubElement(word_node, 'subjunctive3s').text = u'soit'
    ET.SubElement(word_node, 'subjunctive1p').text = u'soyons'
    ET.SubElement(word_node, 'subjunctive2p').text = u'soyez'
    ET.SubElement(word_node, 'subjunctive3p').text = u'soient'
    ET.SubElement(word_node, 'copular')
    return word_node


def test_indexed(empty_lexicon_fr, lexicon_fr):
    assert not empty_lexicon_fr.indexed
    assert lexicon_fr.indexed


def test_word_from_node(empty_lexicon_fr, word_node):
    word_elt = empty_lexicon_fr.word_from_node(word_node)
    assert isinstance(word_elt, WordElement)
    assert word_elt.id == u'E0012152'
    assert word_elt.base_form == u'être'
    assert word_elt.category == u'VERB'
    assert word_elt['present1s'] == u'suis'
    assert word_elt['present2s'] == u'es'
    assert word_elt['copular'] is True
    assert word_elt.default_inflection_variant == 'reg'
    assert word_elt.inflection_variants == ['reg']


def test_index_word(empty_lexicon_fr, word_node):
    lex = empty_lexicon_fr
    word_elt = lex.word_from_node(word_node)
    assert not lex.words
    assert not lex.id_index
    assert not lex.base_index
    assert not lex.variant_index
    assert not lex.category_index
    lex.index_word(word_elt)
    assert lex.id_index[u'E0012152'] == word_elt
    assert lex.base_index[u'être'] == [word_elt]
    assert lex.variant_index[u'être'] == [word_elt]
    assert lex.category_index[u'VERB'] == [word_elt]


def test_index_lexicon(lexicon_fr):
    assert lexicon_fr.words
    assert lexicon_fr.id_index
    assert lexicon_fr.base_index
    assert lexicon_fr.variant_index
    assert lexicon_fr.category_index


@pytest.mark.parametrize("word_base_form, category, expected", [
    ('son', ANY, 2),
    ('son', NOUN, 1),
    ('son', DETERMINER, 1),
    ('son', VERB, 0),
])
def test_lookup(lexicon_fr, word_base_form, category, expected):
    assert len(
        _list(lexicon_fr.get(word_base_form, category=category))) == expected


@pytest.mark.parametrize("word_base_form, expected", [
    ('son', 2),
    ('GRUB', 1),  # will automatically be created
])
def test_getitem(lexicon_fr, word_base_form, expected):
    assert len(_list(lexicon_fr.get(word_base_form))) == expected


@pytest.mark.parametrize("word_feature, expected_base_form", [
    (u'manger', u'manger'),
    (u'vache_1', u'vache'),
])
def test_get(lexicon_fr, word_feature, expected_base_form):
    assert lexicon_fr.get(word_feature)[0].base_form == expected_base_form


def test_first(lexicon_fr):
    son_categories = [w.category for w in lexicon_fr['son']]
    assert son_categories == [DETERMINER, NOUN]
    assert lexicon_fr.first('son', category=ANY).category == DETERMINER


def test_features1(lexicon_en):
    good = lexicon_en.first('good', category=ADJECTIVE)
    assert good[COMPARATIVE] == 'better'
    assert good[SUPERLATIVE] == 'best'
    assert good[PREDICATIVE] is True
    assert good[QUALITATIVE] is True


def test_getattr(lexicon_en):
    good = lexicon_en.first('good', category=ADJECTIVE)
    assert good.predicative is True
    assert good.superlative == 'best'
    assert good.comparative == 'better'
    assert good.qualitative is True


def test_features2(lexicon_en):
    woman = lexicon_en.first('woman', category=NOUN)
    assert woman.plural == 'women'
    assert woman.acronym_of is None
    assert not woman.proper
    assert 'uncount' not in woman.inflections


def test_features3(lexicon_en):
    sand = lexicon_en.first('sand', category=NOUN)
    assert 'nonCount' in sand.inflections
    assert sand.default_infl == 'nonCount'


def test_features4(lexicon_en):
    quickly = lexicon_en.first(u'E0051632')
    assert quickly.base_form == 'quickly'
    assert quickly.category == ADVERB
    assert quickly.verb_modifier
    assert not quickly.sentence_modifier
    assert not quickly.intensifier


def test_independant_words(lexicon_fr):
    le1 = lexicon_fr.first(u'le')
    le2 = lexicon_fr.first(u'le')
    assert le1 is not le2
    le1.realisation = u"l'"
    assert le2.realisation == u"le"
