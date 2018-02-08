from .spec.phrase import NounPhraseElement

__version__ = '0.1.1'


def make_noun_phrase(lexicon, specifier, noun, modifiers=None):
    phrase = NounPhraseElement(lexicon)
    phrase.head = noun
    phrase.specifier = specifier
    if modifiers:
        if not isinstance(modifiers, list):
            modifiers = [modifiers]
        for modifier in modifiers:
            phrase.add_modifier(modifier)
    return phrase
