# -*- Mode: python; encoding: UTF-8;tab-width: 4; indent-tabs-mode:nil; -*- vim: ai ts=4 sts=4 et sw=4 ft=python

import logging
logger = logging.getLogger(__name__)
logging.setLoggerClass(logging.Logger)
logger = logging.getLogger('ipython')
logger.setLevel('DEBUG')
from igo.Tagger import Tagger

tagger = None
def get_tagger():
    global tagger
    if tagger is None:
        tagger = Tagger('ipadic')
    return tagger

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
