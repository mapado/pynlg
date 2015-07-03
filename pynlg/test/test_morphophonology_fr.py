# encoding: utf-8

"""Test suite for the french morphophonology rules."""

import pytest
import re

from ..morphophonology.fr import (
    LE_LEQUEL_RE, LES_LESQUELS_RE,
    insert_au_du,
    undetach_pronoun)


@pytest.yield_fixture
def a(lexicon_fr):
    a = lexicon_fr.first(u'à')
    rea = a.realisation
    yield a
    a.realisation = rea


@pytest.yield_fixture
def de(lexicon_fr):
    de = lexicon_fr.first(u'de')
    rea = de.realisation
    yield de
    de.realisation = rea


@pytest.yield_fixture
def le(lexicon_fr):
    le = lexicon_fr.first(u'le')
    rea = le.realisation
    yield le
    le.realisation = rea


@pytest.yield_fixture
def lequel(lexicon_fr):
    lequel = lexicon_fr.first(u'lequel')
    rea = lequel.realisation
    yield lequel
    lequel.realisation = rea


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


def test_insert_au_du_a_le(a, le):
    insert_au_du(a, le)
    assert a.realisation == 'au'
    assert le.realisation is None


def test_insert_au_du_a_lequel(a, lequel):
    insert_au_du(a, lequel)
    assert a.realisation == 'auquel'
    assert lequel.realisation is None


def test_insert_au_du_de_le(de, le):
    insert_au_du(de, le)
    assert de.realisation == 'du'
    assert le.realisation is None


def test_insert_au_du_de_lequel(de, lequel):
    insert_au_du(de, lequel)
    assert de.realisation == 'duquel'
    assert lequel.realisation is None
