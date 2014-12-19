# -*- coding: utf-8 -*-

from StringIO import StringIO
import sys
import mrep.builder
import mrep.pattern
import mrep.morph
from StringIO import StringIO

def get_parsed_data(data, parser, matcher):
    for chunk in data:
        chunk = parser.parse(chunk)
        results = mrep.pattern.find(chunk, matcher)
        if results:
            yield results

matcher = mrep.builder.parse('(<pos=記号>)*')
parser = mrep.morph.MeCabParser()
import codecs
ff = codecs.open('/private/tmp/uuge', encoding='utf8')
lines = ff.readlines()
lines = [l.encode('utf8') for l in lines]
print(len(lines))
lines = lines[:20000]


def f():
    results =list(get_parsed_data(lines, parser, matcher))
    print(len(results))

from timeit import timeit

print timeit(f, number=1)
