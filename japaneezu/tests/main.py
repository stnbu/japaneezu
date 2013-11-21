# -*- Mode: python; encoding: UTF-8;tab-width: 4; indent-tabs-mode:nil; -*- vim: ai ts=4 sts=4 et sw=4 ft=python

import logging
import sys
import os
logger = logging.getLogger(__name__)
from glob import glob
from guess import guess
sys.path.insert(1, '/Users/miburr/japaneezu')
from japaneezu import *  # FIXME relative

_TEST_DATA = None
def get_all_test_data():
    global _TEST_DATA
    if _TEST_DATA is None:
        files = '{}/data/*'.format(os.path.dirname(__file__)).replace('/', os.sep)
        files = glob(files)
        files = [open(f, 'rb') for f in files]
        _TEST_DATA = ''
        for _file in files:
            _TEST_DATA += _file.read().decode(encoding='UTF-16-LE', errors='replace')
    return _TEST_DATA

def test_class_Char():

    text = u'あいうえおイロハ漢字'

    prev = None
    for c in text:
        prev = Char(value=c, prev=prev)

    try:
        badprev = type
        Char(value='x', prev=badprev)
        raise AssertionError('Able to init {} with prev={}.'.format(Char.__name__, badprev.__class__))
    except ValueError:
        pass

    assert Char('x') == Char('x')

def test_class_Word():

    words = ['three', 'two', 'three', 'counteractive']
    prev = None
    for word in words:
        prev = Word(value=word, prev=prev)

    try:
        badprev = -1
        Word(value='frog', prev=badprev)
        raise AssertionError('Able to init {} with prev={}.'.format(Word.__name__, badprev.__class__))
    except ValueError:
        pass

    w = Word(u'日本語能力試験')
    assert len(w.subwords) == 3
    one = u'日本語'
    two = u'能力'
    three = u'試験'
    assert one == w.subwords[0]
    assert two == w.subwords[1]
    assert three == w.subwords[2]
    assert Word(u'foo') == Word('foo')

    test_data = get_all_test_data()[:200]
    assert Word(value=test_data)

def test_char_classification():
    test_pairs = [
        (u'漢', Kanji),
        (u'ひ', Hiragana),
        (u'マ', Katakana),
    ]
    for char, klass in test_pairs:
        assert get_char_class(char) is klass
        assert char in klass
        assert char in klass()


if __name__ == '__main__':
    test_class_Char()
    test_class_Word()
    test_char_classification()
