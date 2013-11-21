# -*- Mode: python; encoding: UTF-8;tab-width: 4; indent-tabs-mode:nil; -*- vim: ai ts=4 sts=4 et sw=4 ft=python

import hotshot, hotshot.stats
from tests import _get_test_data
from main import *
from random import randint

def f():
    test_data = _get_test_data()
    test_data = test_data[:2000]
    bigword = Word(value=test_data)

pro_file = '/tmp/.Word.{}.prof'.format(randint(0, 2**32))

prof = hotshot.Profile(pro_file, lineevents=True)
prof.runcall(f)
prof.close()

stats = hotshot.stats.load(pro_file)
#stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)
