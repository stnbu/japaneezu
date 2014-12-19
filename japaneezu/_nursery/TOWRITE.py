# -*- coding: utf-8 -*-

## Q: what is a "japanese word"? is there some universal agreement?
## N: forget about syncing up POS beteen dicts and things. Just decide on *your* idea of a POS and use that.

## Q: how do I deal with things *like* having to package *.cvs file? what about updates? what about giving credit? what
## about letting users specify their own?

## N: look at the existing logic that Text uses to wrap text. Use/implement that in a subclass of ListBox. Maby make a
## frankenclass out of subclassed Edit and ListBox

## Ideas:
##  * Text to speech
##  * Anki integration

class GrammarCheckerThing(object): pass

def get_conjugations(jword):
    return conjugation_objects

def Translation(object):
    @property
    def simple(self):
        "just one word or phrase corresponding to the jtext"

    @property
    def proposals(self):
        "like simple, but a list, in order of confidence."

    @property
    def tokens(self):
        "a container of Translation objects for the first pass (largest) tokens for the jtext, ad infinitum"

    @property
    def x(self):
        ""

def get_furigana(jword):
    """
    Should probably be an "object"
    Should probably be something like:
        kanji_sequence <-> furigana
    for cases like 受け取る which may be considered "one word", but has discontinous kanji
    """
    if has_kanji:
        return furigana
    else:
        return None

def haha(jword):
    return pos_object

def xyzz(jtext):
    """
    Q: what are tokens? should they be as small as possible?
    """
    return TOKENS

class TheTextDisplayerThing(object):
    """
    subclass Edit so that it has two rows of text (um, "per row") and raises an exception when the text cannot be contained.

    subclass Edit so that it maintains a unicode object (for furigana) corresponding to its contents.
    """

