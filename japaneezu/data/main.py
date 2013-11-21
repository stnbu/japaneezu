# -*- Mode: python; encoding: UTF-8;tab-width: 4; indent-tabs-mode:nil; -*- vim: ai ts=4 sts=4 et sw=4 ft=python

from glob import glob
import os

_test_data = None
def get_all_test_data():
    global _test_data
    if _test_data is None:
        files = '{}/files/*'.format(os.path.dirname(__file__)).replace('/', os.sep)
        files = glob(files)
        files = [open(f, 'rb') for f in files]
        _test_data = ''
        for _file in files:
            _test_data += _file.read().decode(encoding='UTF-16-LE', errors='replace')
    return _test_data

if __name__ == '__main__':
    print len(get_all_test_data())
