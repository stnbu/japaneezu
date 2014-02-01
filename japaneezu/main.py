# -*- Mode: python; encoding: UTF-8;tab-width: 4; indent-tabs-mode:nil; -*- vim: ai ts=4 sts=4 et sw=4 ft=python

import logging
logger = logging.getLogger(__name__)
logging.setLoggerClass(logging.Logger)
logger = logging.getLogger('ipython')
logger.setLevel('DEBUG')
from igo.Tagger import Tagger

WORD_DB = {}
word_db_get = lambda k: WORD_DB.get(k, None)
word_db_add = lambda k, v: WORD_DB.update({k: v})

CHAR_DB = {}
char_db_get = lambda k: CHAR_DB.get(k, None)

tagger = None
def get_tagger():
    global tagger
    if tagger is None:
        tagger = Tagger('ipadic')
    return tagger

char_classes = []

class Stats(object):

    def __init__(self, value):
        self.value = value
        self.count = 1

class CharStats(Stats):
    pass

class WordStats(Stats):
    pass

def char_db_add(char):
    global CHAR_DB
    char_stats = CharStats(char)
    CHAR_DB.update({char: char_stats})
    return char_stats

def _contains_char(obj, char):
    num = ord(char)
    return num >= obj.unichr_range[0] and num <= obj.unichr_range[1]

class CharClassMaintainer(type):

    def __new__(cls, classname, bases, classdict):
        global char_classes
        classobj = type.__new__(cls, classname, bases, classdict)
        if classobj.__name__ != 'CharClass':  # Don't add the base class
            char_classes.append(classobj)
        return classobj

    __contains__ = _contains_char

class CharClass(unicode):

    __metaclass__ = CharClassMaintainer
    __contains__ = _contains_char

###
# Unicode magic numbers courtesy: http://en.wikipedia.org/wiki/Japanese_writing_system

class Kanji(CharClass):
    unichr_range = 0x4E00, 0x9FBF

class Hiragana(CharClass):
    unichr_range = 0x3040, 0x309F

class Katakana(CharClass):
    unichr_range = 0x30A0, 0x30FF

# Order of definition matters. This is declared last.  # <--  FIXME
class OtherChar(CharClass):
    unichr_range = 0, 0x10000 - 1  # FIXME

def get_char_class(char):
    global char_classes
    for klass in char_classes:
        if char in klass:
            return klass
    else:
        raise ValueError(u'Could not find appropriate CharClass for {}. How did you get here?!'.format(char))

class Token(object):

    def __init__(self, value, prev=None):
        self.prev = prev
        self.value = value
        if self.prev is None:
            pass
            #logger.debug('"prev" is None. Assuming this is the first {}'.format(self.__class__.__name__))
        elif not isinstance(self.prev, self.__class__):
            raise ValueError('prev={} must be an instance of {}'.format(repr(self.prev), self.__class__))

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__str__() == other.__str__()  # unless something's broken, this is "equal"
        return self.__str__() == other

    __repr__ = __unicode__ = __str__  # ???

class Char(Token):
    ''

class Word(Token):

    def __init__(self, value, prev=None, top=True):
        Token.__init__(self, value=value, prev=prev)  # provides attrs value, prev
        #logger.debug('instantiating {}'.format(repr(self)))
        self.subwords = []
        self.top = top

        if word_db_get(self.value) is not None:
            self = word_db_get(self.value)
            return
        else:
            word_db_add(self.value, self)

        # FIXME things are double-counted because of the subword thing
        new_value = u''
        for char in self.value:
            if char_db_get(char) is not None:
                record = char_db_get(char)
                record.count += 1
                klass = record.klass
            else:
                klass = get_char_class(char)
                record = char_db_add(char)
                record.klass = klass
                char = klass(char)
            new_value += char
        self.value = new_value

        if not self.top:
            return

        tagger = get_tagger()
        _prev_subword = None
        #logger.debug('Parsing out tags from {}'.format(repr(self)))
        self._tags = tagger.parse(self.value)
        #logger.debug('Done parsing out tags from {}'.format(repr(self)))
        if len(self._tags) > 1 and self.top:  # FIXME: is 'foo' in [x.surface for x in parse('foo')] ?? Always? etc??
            #logger.debug('"{}" has subwords. handling those.'.format(self.shortname))
            for tag in self._tags:
                if False and tag.surface in self.subwords:  # FIXME
                    #logger.debug('{} already in {}.subwords. Reusing.'.format(repr(_prev_subword), repr(self.shortname)))
                    index = self.subwords.index(tag.surface)
                    self.subwords.append(self.subwords[index])
                _prev_subword = Word(value=tag.surface, prev=_prev_subword, top=False)  # FIXME
                #logger.debug('Adding {} to {}.subwords.'.format(repr(_prev_subword), repr(self.shortname)))
                self.subwords.append(_prev_subword)

    @property
    def shortname(self):
        return repr(self.value[:20])  # FIXME

    def __repr__(self):
        return '<{}(value={}...)>'.format(self.__class__.__name__, self.shortname)
