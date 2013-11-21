# -*- Mode: python; encoding: UTF-8;tab-width: 4; indent-tabs-mode:nil; -*- vim: ai ts=4 sts=4 et sw=4 ft=python

import hotshot, hotshot.stats
from main import *
from random import randint
from tests import *

def f():
    test_data = get_all_test_data()
    limit = 1000.0
    print 'actual test data', len(test_data) / limit, 'times bigger'
    test_data = test_data[:int(limit)]
    bigword = Word(value=test_data)

pro_file = '/tmp/.Word.{}.prof'.format(randint(0, 2**32))

prof = hotshot.Profile(pro_file, lineevents=True)
prof.runcall(f)
prof.close()

stats = hotshot.stats.load(pro_file)
#stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)
