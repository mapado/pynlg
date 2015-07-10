# encoding: utf-8

"""Definition of french helpers related to sentence syntax."""

from .base import NounPhraseHelper
from ...spec.base import NLGElement
from ...spec.word import WordElement, InflectedWordElement
from ...spec.string import StringElement
from ...spec.phrase import AdjectivePhraseElement
from ...lexicon.feature.category import PRONOUN, ADJECTIVE
from ...lexicon.feature import PERSON, NUMBER
from ...lexicon.feature.lexical import GENDER
from ...lexicon.feature.person import THIRD
from ...lexicon.feature.gender import MASCULINE
from ...lexicon.feature.number import SINGULAR
from ...lexicon.feature.lexical.fr import PRONOUN_TYPE
from ...lexicon.feature.pronoun import PERSONAL


__all__ = ['FrenchNounPhraseHelper']


class FrenchNounPhraseHelper(NounPhraseHelper):

    @staticmethod
    def is_ordinal(element):
        """Recognises ordinal adjectives by their ending ("ième").

        Exceptions : "premier", "second" and "dernier" are treated in
        the lexicon.

        """
        if not element:
            return False
        if isinstance(element, StringElement):
            base_form = element.realisation
        else:
            base_form = element.base_form
        return base_form and base_form.endswith(u'ième')

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

    def add_modifier(self, modifier):
        """Add the argument modifier to the phrase pre/post modifier
        list.

        """
        if not modifier:
            return
        # string which is one lexicographic word is looked up in lexicon,
        # preposed adjective is preModifier
        # Everything else is postModifier
        modifier_element = None
        if isinstance(modifier, NLGElement):
            modifier_element = modifier
        else:
            modifier_element = self.phrase.lexicon.get(modifier, create_if_missing=False)
            if modifier_element:
                modifier_element = modifier_element[0]

            # Add word to lexicon
            if (
                not modifier_element
                and (
                    self.is_ordinal(modifier_element)
                    or (modifier and u' ' not in modifier)
                )
            ):
                modifier_element = WordElement(
                    base_form=modifier,
                    realisation=modifier,
                    lexicon=self.phrase.lexicon,
                    category=ADJECTIVE)
                self.phrase.lexicon.create_word(modifier_element)

        # if no modifier element was found, it must be a complex string,
        # add it as postModifier
        if not modifier_element:
            self.phrase.add_post_modifier(StringElement(string=modifier))
            return
        #  adjective phrase is a premodifer
        elif isinstance(modifier_element, AdjectivePhraseElement):
            head = modifier_element.head
            if (
                (head.preposed or self.is_ordinal(head))
                and not modifier_element.complements
            ):
                self.phrase.add_pre_modifier(modifier_element)
                return
        # Extract WordElement if modifier is a single word
        else:
            if isinstance(modifier_element, InflectedWordElement):
                modifier_word = modifier_element.base_word
            else:
                modifier_word = modifier_element
            #  check if modifier is an adjective
            if (
                    modifier_word
                    and modifier_word.category == ADJECTIVE
                    and modifier_element.preposed
                    or self.is_ordinal(modifier_word)
            ):
                self.phrase.add_pre_modifier(modifier_word)
                return
        #  default case
        self.phrase.add_post_modifier(modifier_element)
