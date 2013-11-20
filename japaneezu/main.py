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
            logger.debug('"prev" is None. Assuming this is the first {}'.format(self.__class__.__name__))
        elif not isinstance(self.prev, self.__class__):
            raise ValueError('prev={} must be an instance of {}'.format(repr(self.prev), self.__class__))

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__str__() == other.__str__()  # unless something's broken, this is "equal"
        return self.__str__() == other

    __unicode__ = __str__  # ???

class Char(Token):
    ''

class Word(Token):

    def __init__(self, value, prev=None):
        Token.__init__(self, value=value, prev=prev)  # provides attrs value, prev
        self.subwords = []
        #tagger = get_tagger()
        tagger = Tagger('ipadic')
        _prev_subword = None
        self._tags = tagger.parse(self.value)
        if len(self._tags) == 1 and value == self._tags[0].surface:
            return
        for tag in self._tags:
            _prev_subword = Word(value=tag.surface, prev=_prev_subword)
            self.subwords.append(_prev_subword)
