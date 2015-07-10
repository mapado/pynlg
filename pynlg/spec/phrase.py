# encoding: utf-8

"""Definition of the PhraseElement class.

TODO
"""

from .base import NLGElement
from .string import StringElement
from .word import WordElement
from ..lexicon.feature import ELIDED
from ..lexicon.feature import category as cat
from ..lexicon.feature import internal
from ..lexicon.feature import clause
from ..lexicon.feature import discourse


__all__ = ['PhraseElement', 'AdjectivePhraseElement']


class PhraseElement(NLGElement):

    def __init__(self, lexicon, category):
        """Create a phrase of the given type."""
        super(PhraseElement, self).__init__(category=category, lexicon=lexicon)
        self.features[ELIDED] = False

    def get_children(self):
        """Return the child components of the phrase.

        The returned list will depend of the category of the element:
        - Clauses consist of cue phrases, front modifiers, pre-modifiers
        subjects, verb phrases and complements.
        - Noun phrases consist of the specifier, pre-modifiers, the noun
        subjects, complements and post-modifiers.
        - Verb phrases consist of pre-modifiers, the verb group,
        complements and post-modifiers.
        - Canned text phrases have no children.
        - All other phrases consist of pre-modifiers, the main phrase
        element, complements and post-modifiers.

        """
        children = []
        if self.category == cat.CLAUSE:
            children.append(self.cue_phrase or [])
            children.extend(self.front_modifiers or [])
            children.extend(self.premodifiers or [])
            children.extend(self.subjects or [])
            children.extend(self.verb_phrase or [])
            children.extend(self.complements or [])
        elif self.category == cat.NOUN_PHRASE:
            children.append(self.specified or [])
            children.extend(self.premodifiers or [])
            children.append(self.head or [])
            children.extend(self.complements or [])
            children.extend(self.postmodifiers or [])
        elif self.category == cat.VERB_PHRASE:
            children.extend(self.premodifiers or [])
            children.append(self.head or [])
            children.extend(self.complements or [])
            children.extend(self.postmodifiers or [])
        else:
            children.extend(self.premodifiers or [])
            children.append(self.head or [])
            children.extend(self.complements or [])
            children.extend(self.postmodifiers or [])

        children = [child for child in children if child]
        children = [
            StringElement(string=child)
            if not isinstance(child, NLGElement) else child
            for child in children]
        return children

    def add_complement(self, complement):
        """Adds a new complement to the phrase element.

        Complements will be realised in the syntax after the head
        element of the phrase. Complements differ from post-modifiers
        in that complements are crucial to the understanding of a phrase
        whereas post-modifiers are optional.

        If the new complement being added is a clause or a
        CoordinatedPhraseElement then its clause status feature is set
        to ClauseStatus.SUBORDINATE and it's discourse function is set
        to DiscourseFunction.OBJECT by default unless an existing
        discourse function exists on the complement.

        """
        complements = self.features[internal.COMPLEMENTS] or []
        complements.append(complement)
        self.features[internal.COMPLEMENTS] = complements
        if (
                complement.category == cat.CLAUSE
                # TODO: define CoordinatedPhraseElement
                # or isinstance(complement, CoordinatedPhraseElement)
        ):
            complement[internal.CLAUSE_STATUS] = clause.SUBORDINATE
            if not complement.discourse_function:
                complement[internal.DISCOURSE_FUNCTION] = discourse.OBJECT

            complement.parent = self


class AdjectivePhraseElement(PhraseElement):

    """This class defines a adjective phrase.

    It is essentially a wrapper around the
    PhraseElement class, with methods for setting common constituents
    such as pre_modifiers.

    """

    def __init__(self, lexicon):
        super(AdjectivePhraseElement, self).__init__(
            category=cat.ADJECTIVE_PHRASE, lexicon=lexicon)

    @property
    def adjective(self):
        return self.head

    @adjective.setter
    def adjective(self, element):
        if isinstance(element, basestring):
            # Create a word, if not found in lexicon
            element = self.lexicon.first(element, category=cat.ADJECTIVE)
            if not element:
                element = WordElement(
                    base_form=element,
                    category=cat.ADJECTIVE,
                    lexicon=self.lexicon,
                    realisation=element)
                self.lexicon.create_word(element)
        self.features[internal.HEAD] = element
