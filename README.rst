pynlg
=====

.. image:: https://travis-ci.org/mapado/pynlg.svg
    :target: https://travis-ci.org/mapado/pynlg

``pynlg`` is a pure python re-implementation of `SimpleNLG-EnFr <https://github.com/rali-udem/SimpleNLG-EnFr>`_, a java library enabling french and english `text surface realisation <https://en.wikipedia.org/wiki/Realization_%28linguistics%29>`_, based on `SimpleNLG <https://github.com/simplenlg/simplenlg>`_.

For more information about what SimpleNLG and SimpleNLG-EnFr, have a look at their documentation:

- `SimpleNLG-EnFr <https://github.com/rali-udem/SimpleNLG-EnFr/blob/master/docs/SimpleNLG-EnFr_doc_francais.pdf>`_ (in french)
- `SimpleNLG <https://github.com/simplenlg/simplenlg/wiki/Section-0-%E2%80%93-SimpleNLG-Tutorial>`_

``pynlg`` supports Python2.7 and 3.5. Python 3.3 and 3.4 should work, but are untested.

Examples
--------

Definition of a nominal sentence, with a feminine noun
******************************************************

.. code-block:: python

    from pynlg.lexicon.fr import FrenchLexicon
    from pynlg.lexicon.feature.category import NOUN, ADJECTIVE, DETERMINER
    from pynlg.lexicon.feature.gender import FEMININE
    from pynlg import make_noun_phrase

    lex = FrenchLexicon()
    un = lex.first(u'un', category=DETERMINER)
    maison = lex.first(u'maison', category=NOUN)
    maison = maison.inflex(gender=FEMININE)
    beau = lex.first(u'beau', category=ADJECTIVE)
    perdu = lex.first(u'perdu', category=ADJECTIVE)
    phrase = make_noun_phrase(lexicon=lex, specifier=un, noun=maison, modifiers=[beau, perdu])
    syntaxically_realised_phrase = phrase.realise()
    morphologically_realised_phrase = syntaxically_realised_phrase.realise_morphology()
    morphologically_realised_phrase.components
    [<StringElement {realisation=une, category=DETERMINER}>,
    <StringElement {realisation=belle, category=ADJECTIVE}>,
    <StringElement {realisation=maison, category=CANNED_TEXT}>,
    <StringElement {realisation=perdue, category=ADJECTIVE}>]

Supported languages
--------------------

For now, the following languages are supported:

- french (in process)
- english (in process)

How can I contribute?
---------------------

First, clone the repository, and create a new local branch. Once the new feature is implemented (or the bug is fixed) and everything is **tested** properly, push your work and create a pull request.

Note: you should run the tests beforehand, and make sure they pass:

.. code-block:: bash

    $ tox


How do I add support for a new language?
----------------------------------------

TODO


License
-------

The MIT License (MIT)

Copyright (c) 2015 Mapado

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
