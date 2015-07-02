# encoding: utf-8

"""Definition of the base class from which all spec elements inherit."""

from ..lexicon import category as lex_category
from ..lexicon.feature import lexical as lex_feature

from ..lexicon.feature import ELIDED

FEATURE_MODULES = [lex_category, lex_feature]


class NLGElement(object):

    """Base spec element class from which all spec element classes inherit."""

    def __init__(
            self, features=None, category=u'', realisation=u'', lexicon=None):
        self.features = features if features else {}
        self.category = category
        self.realisation = realisation
        self.lexicon = lexicon

    def __eq__(self, other):
        if isinstance(other, NLGElement):
            return (self.features == other.features
                    and self.category == other.category)
        elif isinstance(other, basestring):
            return self.realisation == other
        else:
            raise TypeError("Can't compare NLGElement to %s" % (
                str(type(other))))

    def __contains__(self, feature_name):
        """Check if the argument feature name is contained in the element."""
        return feature_name in self.features

    def __setitem__(self, feature_name, feature_value):
        """Set the feature name/value in the element feature dict."""
        self.features[feature_name] = feature_value

    def __getitem__(self, feature_name):
        """Return the value associated with the feature name, from the
        element feature dict.

        If the feature name is not found in the feature dict, return None.

        """
        return self.features.get(feature_name)

    def __delitem__(self, feature_name):
        """Remove the argument feature name and its associated value from
        the element feature dict.

        If the feature name was not initially present in the feature dict,
        a KeyError will be raised.

        """
        if feature_name in self.features:
            del self.features[feature_name]

    def __unicode__(self):
        return u"<%s {realisation=%s, category=%s, features=%s}>" % (
            self.__class__.__name__,
            self.realisation,
            self.category,
            unicode(self.features))

    def __repr__(self):
        return unicode(self).encode('utf-8')

    def __getattr__(self, name):
        """When a undefined attribute name is accessed, try to return
        self.features[name] if it exists.

        If name is not in self.features, but name.upper() is found in
        one of the modules defining feature constants,
        self.features[v] will be returned, where v is the value
        associated with the feature constant which name is v.upper()

        If no such match is found, raise an AttributeError.

        """
        n = name.upper()
        if name in self.features:
            return self.features[name]
        else:
            for mod in FEATURE_MODULES:
                if n in dir(mod):
                    return self.features.get(vars(mod)[n])
        raise AttributeError(name)

    @property
    def feature_names(self):
        """Return all feature names, the keys in the element feature dict."""
        return self.features.keys()

    @property
    def elided(self):
        return self.features[ELIDED]

    @property
    def language(self):
        """Return the language lexicon."""
        if self.lexicon:
            return self.lexicon.language
