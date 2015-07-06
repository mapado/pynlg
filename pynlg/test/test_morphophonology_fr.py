# encoding: utf-8

"""Test suite for the french morphophonology rules."""

import pytest
import re

from ..morphophonology.fr import (
    LE_LEQUEL_RE, LES_LESQUELS_RE, insert_au_du,
    add_apostrophe, deduplicate_left_right_realisation,
    start_with_vowel)
from ..lexicon.feature.category import CONJUNCTION


@pytest.mark.parametrize('s', [
    'le',
    'lequel',
    pytest.mark.xfail('les'),
])
def test_le_lequel_re(s):
    assert re.match(LE_LEQUEL_RE, s).group() == s


@pytest.mark.parametrize('s', [
    pytest.mark.xfail('le'),
    'les',
    'lesquels',
    'lesquelles'
])
def test_les_lequels_re(s):
    assert re.match(LES_LESQUELS_RE, s).group() == s


def test_insert_au_du_a_le(lexicon_fr):
    a = lexicon_fr.first(u'à')
    le = lexicon_fr.first(u'le')
    insert_au_du(a, le)
    assert a.realisation == 'au'
    assert le.realisation is None


def test_insert_au_du_a_lequel(lexicon_fr):
    a = lexicon_fr.first(u'à')
    lequel = lexicon_fr.first(u'lequel')
    insert_au_du(a, lequel)
    assert a.realisation == 'auquel'
    assert lequel.realisation is None


def test_insert_au_du_de_le(lexicon_fr):
    de = lexicon_fr.first(u'de')
    le = lexicon_fr.first(u'le')
    insert_au_du(de, le)
    assert de.realisation == 'du'
    assert le.realisation is None


def test_insert_au_du_de_lequel(lexicon_fr):
    de = lexicon_fr.first(u'de')
    lequel = lexicon_fr.first(u'lequel')
    insert_au_du(de, lequel)
    assert de.realisation == 'duquel'
    assert lequel.realisation is None


def test_add_apostrophe_si_ils(lexicon_fr):
    si = lexicon_fr.first(u'si', category=CONJUNCTION)
    ils = lexicon_fr.first(u'ils')
    add_apostrophe(si, ils)
    assert si.realisation == u"s'"
    assert ils.realisation == u'ils'


def test_add_apostrophe_le_arbre(lexicon_fr):
    le = lexicon_fr.first(u'le')
    arbre = lexicon_fr.first(u'arbre')
    add_apostrophe(le, arbre)
    assert le.realisation == u"l'"
    assert arbre.realisation == u'arbre'


def test_add_apostrophe_other(lexicon_fr):
    la = lexicon_fr.first(u'la')
    voiture = lexicon_fr.first(u'voiture')
    add_apostrophe(la, voiture)
    assert la.realisation == u"la"
    assert voiture.realisation == u'voiture'


@pytest.mark.parametrize('left, right', [
    ('de', 'de'),
    ('de', 'du'),
    ('de', "d'"),
    ('que', 'que'),
    ('que', "qu'"),
])
def test_deduplicate_left_right_realisation(lexicon_fr, left, right):
    left = lexicon_fr.first(left)
    old_left_realisation = left.realisation
    right = lexicon_fr.first(right)
    deduplicate_left_right_realisation(left, right)
    assert left.realisation == old_left_realisation
    assert right.realisation is None


@pytest.mark.parametrize('word, expected', [
    (u'arbre', True),
    (u'voiture', False),
    (u'oui', False)
])
def test_start_with_vowel(lexicon_fr, word, expected):
    word = lexicon_fr.first(word)
    assert start_with_vowel(word) is expected
