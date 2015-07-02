# encoding: utf-8

"""Test suite of the NLGElement base class."""

import pytest

from ..spec.base import NLGElement


@pytest.fixture(scope='module')
def nlg_elt():
    return NLGElement()


def test_feature_access(nlg_elt):
    assert nlg_elt['feature'] is None
    nlg_elt['feature'] = 'value'
    assert nlg_elt['feature'] == 'value'
    del nlg_elt['feature']
    assert nlg_elt['feature'] is None


def test_contains(nlg_elt):
    assert 'nope' not in nlg_elt
    nlg_elt['yes'] = 'YES'
    assert 'yes' in nlg_elt


@pytest.mark.parametrize('elt,other_elt', [
    (NLGElement(), NLGElement()),
    (NLGElement(features={'k': 'v'}), NLGElement(features={'k': 'v'})),
    (
        NLGElement(features={'k': 'v'}, category='h'),
        NLGElement(features={'k': 'v'}, category='h')
    ),
    pytest.mark.xfail((
        NLGElement(features={'k1': 'v1'}, category='h'),
        NLGElement(features={'k2': 'v2'}, category='h')
    )),
    pytest.mark.xfail((
        NLGElement(features={'k': 'v'}, category='h1'),
        NLGElement(features={'k': 'v'}, category='h2')
    ))
])
def test_equality(elt, other_elt):
    assert elt == other_elt
