# -*- Mode: python; encoding: UTF-8;tab-width: 4; indent-tabs-mode:nil; -*- vim: ai ts=4 sts=4 et sw=4 ft=python

import logging
import sys
logger = logging.getLogger(__name__)
from glob import glob
from guess import guess
from foo import *

_test_data = None
def _get_test_data():
    global _test_data
    files = '/Users/miburr/tmp/xx/*'
    files = glob(files)
    files = [open(f, 'rb') for f in files]
    if _test_data is None:
        _test_data = ''
        for _file in files:
            _test_data += _file.read().decode(encoding='UTF-16-LE', errors='replace')
            break  ## ONE FILE FIXME
    return _test_data

def tests():

    text = u'あいうえおイロハ漢字'

    prev = None
    for c in text:
        prev = Char(value=c, prev=prev)

    try:
        badprev = type
        Char(value='x', prev=badprev)
        logger.error('Able to init {} with prev={}.'.format(Char.__name__, badprev.__class__))
    except ValueError:
        pass

    assert Char('x') == Char('x')

    words = ['three', 'two', 'three', 'counteractive']
    prev = None
    for word in words:
        prev = Word(value=word, prev=prev)

    try:
        badprev = -1
        Word(value='frog', prev=badprev)
        logger.error('Able to init {} with prev={}.'.format(Word.__name__, badprev.__class__))
    except ValueError:
        pass

    if False:
        w = Word(u'日本語能力試験')
        assert len(w.subwords) == 3
        one = u'日本語'
        two = u'能力'
        three = u'試験'
        assert one == w.subwords[0]
        assert two == w.subwords[1]
        assert three == w.subwords[2]
        assert Word(u'foo') == Word('foo')

    test_data = _get_test_data()
    bigword = Word(value=test_data)

if __name__ == '__main__':
    tests()
