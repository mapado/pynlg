# encoding: utf-8

"""Test suite of the lexicon package"""

import pytest

from xml.etree import cElementTree as ET

from ..lexicon.lexicon import Lexicon
from ..lexicon.lang import FRENCH, ENGLISH
from ..exc import UnhandledLanguage
from ..spec.word import WordElement


@pytest.mark.parametrize('lang', [FRENCH, ENGLISH])
def test_lexicon_supported_languages(lang):
    Lexicon(lang, auto_index=False).lexicon_filepath


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


def test_lexicon_other_language():
    with pytest.raises(UnhandledLanguage):
        Lexicon('unhandled language', auto_index=False).lexicon_filepath


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
