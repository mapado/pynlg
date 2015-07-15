# encoding: utf-8

"""Definition of generic phrase syntaxes."""


from ...lexicon.feature.discourse import PRE_MODIFIER, SPECIFIER
from ...lexicon.feature.category import PRONOUN
from ...lexicon.feature import NUMBER
from ...lexicon.feature.internal import DISCOURSE_FUNCTION


class NounPhraseHelper(object):

    """Base class for all languages noun phrase helpers."""

    def __init__(self, phrase):
        self.phrase = phrase

    def realise_head_noun(self, realised):
        """Realise the head noun of the phrase, and append the result
        to the argument realised list.

        :param realised: the current realised ListElement

        """
        head = self.phrase.head
        if not head:
            return None
        head.realise_syntax()
        head.gender = self.phrase.gender
        head.acronym = self.phrase.acronym
        head.number = self.phrase.number
        head.person = self.phrase.person
        head.possessive = self.phrase.possessive
        head.passive = self.phrase.passive
        head.discourse_function = self.phrase.discourse_function
        realised.append(head)

    def realise_premodifiers(self, realised):
        """TODO

        :param realised: the current realised ListElement

        """
        # TODO: improve kwargs, fix API? Implement phrase helper
        # self.phrase.helper.realise_list(realised, self.phrase.pre_modifiers, PRE_MODIFIER)

    def realise_specifier(self, realised):
        """Realise the phrase specifier and add it to the argument
        realised list.

        The specifier will only be realised if the phrase is not raised.

        Note: The RAISED flag can be set when specifiers in a
        coordinated phrase should be raised. For example, the
        coordinated phrase "my cat and my dog" can have its specifiers
        raised becoming "my cat and dog".

        :param realised: the current realised ListElement

        """
        if self.phrase.specifier and not self.phrase.raised:
            realised_element = self.phrase.specifier.realise_syntax()
            realised_element.features[DISCOURSE_FUNCTION] = SPECIFIER
            if self.phrase.specifier.category == PRONOUN:
                realised_element.features[NUMBER] = self.phrase.number
            realised.append(realised_element)
