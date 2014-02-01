# -*- Mode: python; encoding: UTF-8;tab-width: 4; indent-tabs-mode:nil; -*- vim: ai ts=4 sts=4 et sw=4 ft=python

KANJI = 'KANJI'
HIRAGANA = 'HIRAGANA'
KATAKANA = 'KATAKANA'

with open('/tmp/x.html', 'rb') as f:
    s = f.read()
    s = s.decode('utf-8')

#print len(s)

# TODO: sublcass set, probably, so we can: u'X' in UniCharClass() - UniCharClass()
# ... etc
class UniCharClass(object):

    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

    def __contains__(self, value):
        return ord(value) in range(self.start, self.end + 1)  # SEE THE '+ 1' ??

kanji = UniCharClass(KANJI, 0x4E00, 0x9FBF)
hiragana = UniCharClass(HIRAGANA, 0x3040, 0x309F)
katakana = UniCharClass(KATAKANA, 0x30A0, 0x30FF)

#print u'聖' in kanji
#print u'ひ' in hiragana
#print u'ヒ' in katakana
#
#print u'聖' in hiragana
#print u'ひ' in kanji
#print u'ヒ' in hiragana

from collections import Counter

class KanjiStats(object):

    def __init__(self, data):
        self._orig_data = data
        self._data = None
        self._freq = None

    @property
    def data(self):
        if self._data is None:
            self._data = []
            for u in self._orig_data:
                if u in kanji:
                    self._data.append(u)
        return self._data

    @property
    def freq(self):
        if self._freq is None:
            self._freq = Counter(self.data)
        return self._freq

#print len(s)
#print u'{}'.format(s)

#ks = KanjiStats(s)
#from timeit import timeit
#def f():
#    global ks
#    ks.data

ks = KanjiStats(s)
from timeit import timeit
def f():
    global s
    return Counter(s)
print len(f())
print timeit(f, number=1)
