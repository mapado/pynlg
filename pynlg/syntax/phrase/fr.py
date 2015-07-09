# encoding: utf-8

"""Definition of french helpers related to sentence syntax."""

from .base import NounPhraseHelper
from ...lexicon.feature.category import PRONOUN
from ...lexicon.feature import PERSON, NUMBER
from ...lexicon.feature.lexical import GENDER
from ...lexicon.feature.internal import DISCOURSE_FUNCTION
from ...lexicon.feature.person import FIRST, SECOND, THIRD
from ...lexicon.feature.gender import MASCULINE, FEMININE
from ...lexicon.feature.number import SINGULAR, PLURAL
from ...lexicon.feature.lexical.fr import PRONOUN_TYPE
from ...lexicon.feature.pronoun import PERSONAL, POSSESSIVE


__all__ = ['FrenchNounPhraseHelper']


class FrenchNounPhraseHelper(NounPhraseHelper):

    def create_pronoun(self):
        """Return an InflectedWordElement wrapping a personal pronoun
        corresponding to the phrase features (number, gender and person).

        """
        features = {
            PRONOUN_TYPE: PERSONAL,
            PERSON: self.phrase.person or THIRD,  # default person is third
            NUMBER: self.phrase.number or SINGULAR,  # default number is singular
            # POSSESSIVE: bool(self.phrase.possessive)
            # I commented out this guy because a pronoun cannot be possessive...
        }
        # Only check gender feature for third person pronouns
        if features[PERSON] == THIRD:
            # default gender for third person pronouns is masculine
            features[GENDER] = self.phrase.gender or MASCULINE

        new_pronoun_elt = (
            self.phrase.lexicon.find_by_features(features, category=PRONOUN)
            or self.phrase.lexicon.first(u'il', category=PRONOUN))
        new_pronoun_infl_elt = new_pronoun_elt.inflex(
            discourse_function=self.phrase.discourse_function,
            passive=self.phrase.passive)
        return new_pronoun_infl_elt
