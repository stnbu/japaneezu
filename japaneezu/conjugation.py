# -*- coding: utf-8 -*-

# This is heavily baserd on con.py written by Stuart McGraw. The actual onv.py should be available here:
# http://edrdg.org/~smg/cgi-bin/hgweb-jmdictdb.cgi/file/9389981dcd33/python/conj.py


import sys
import os
import csv
import codecs

def decode(args):
    try:
        args.decode('utf8')
    except AttributeError:
        seq_class = args.__class__
        def decode_item(c):
            if isinstance(c, basestring):
                return c.decode('utf8')
            else:
                return c
        args = [decode_item(c) for c in args]
        args = seq_class(args)
    return args

class Conjugator(object):

    def sbool(self, arg):
        if arg.lower().startswith('f'):
            return False
        if arg.lower().startswith('t'):
            return True
        raise ValueError(arg)

    def xint(self, arg):
        if arg is None or arg == '':
            return None
        return int(arg)

    def __init__(self, word, dir=None):
        CHEAT = 'v5k'
        self.column_types = {
            'conj': [int, str],
            'conjo': [int, int, self.sbool, self.sbool, int, int, str, str, str, self.xint],
            'kwpos': [int, str, str],
        }
        self.orig_word = word
        self.dir = dir
        self._conjugation_tables = None
        self._conjugations = None

        self.kanji, self.kana = self.handle_char_types(word)
        self.pos_id = self.conjugation_tables['kwpos'][CHEAT][0]

    @property
    def conjugations(self):
        if self._conjugations is not None:
            return self._conjugations
        self._conjugations = {}
        conjugation_indices = [i for i, d in self.conjugation_tables['conj'].values()]
        for conjugation_index in conjugation_indices:
            for is_negative, is_formal in (0, 0), (0, 1), (1, 0), (1, 1):
                for okurigana_id in range(1, 10):
                    tuple_index = self.pos_id, conjugation_index, is_negative, is_formal, okurigana_id
                    try:
                        conjo_entry = self.conjugation_tables['conjo'][tuple_index]
                        stem, okurigana, eurphonic_replacement, euphonic_kanji_relacement = conjo_entry[5:-1]
                    except KeyError:
                        break

                    args = stem, okurigana, eurphonic_replacement, euphonic_kanji_relacement
                    args = decode(args)
                    constructed_text_components = []
                    for text_components in self.kanji, self.kana:
                        if text_components:
                            constructed_text_components.append(self.construct(text_components, *args ))
                        else:
                            constructed_text_components.append('')
                    kanji, kana = constructed_text_components

                    self._conjugations[tuple_index] = kanji+'【'+kana+'】' if kanji and kana else (kanji or kana)

        # add additional okurigana if present
        for key in sorted(self._conjugations.keys()):
            txt = self._conjugations[key]
            if key[:-1] not in self._conjugations:
                self._conjugations[key[:-1]] = txt
            else:
                contents = self._conjugations[key[:-1]]
                try:
                    contents.append(txt)
                except AttributeError:
                    contents = [contents, txt]
                self._conjugations[key[:-1]] = contents

        return self._conjugations

    def handle_char_types(self, word):
            if any((ord(c) >= 0x4000 for c in word)):
                kanj, kana = word, None
            else:
                kanj, kana = None, word
            return kanj, kana

    @property
    def conjugation_tables(self):
        if self._conjugation_tables is not None:
            return self._conjugation_tables
        self._conjugation_tables = {}
        for name in self.column_types.keys():
            filename = os.path.join(self.dir, name + '.csv')
            csvtbl = self.readcsv(filename, self.column_types[name], name != 'kwpos')
            if name == 'conjo':
                self._conjugation_tables[name] = dict(((tuple(row[0:5]), row) for row in csvtbl))
            else:
                self._conjugation_tables[name] = dict(((row[0], row) for row in csvtbl))
                if name == 'kwpos':
                    self._conjugation_tables[name].update(((row[1], row) for row in csvtbl))
        return self._conjugation_tables


    def construct(self, txt, stem, okurigana, eurphonic_replacement, euphonic_kanji_relacement):
        iskana = txt[-2] > u'あ' and txt[-2] <= u'ん'
        if iskana and eurphonic_replacement or not iskana and euphonic_kanji_relacement:
            stem += 1
        if iskana:
            conjtxt = txt[:-stem] + (eurphonic_replacement or '') + okurigana
        else:
            conjtxt = txt[:-stem] + (euphonic_kanji_relacement or u'') + okurigana
        return conjtxt


    def readcsv(self, filename, column_types, hasheader):
        table = []
        with codecs.open(filename, mode='r') as f:
            reader = csv.reader(f, delimiter='\t')
            if hasheader:
                next(reader)  # Skip header row.
            for row in reader:
                newrow = [column_types[cnum](col) for cnum, col in enumerate(row)]
                table.append(newrow)
            return table


if __name__ == '__main__':

    c = Conjugator(word=u'叩く', dir='/Users/miburr/source/jmdictdb/pg/data')
    c.conjugations


    dir = '/Users/miburr/source/jmdictdb/pg/data'
    words = [
        ('v5k', u'近づく'),
        ('v5r', u'履ける'),
        ('v5b', u'忍ぶ'),
        ('v5k', u'叩く'),
        ('v5k', chr(30952) + chr(12367)),
        ('v5r', u'サボる',)
    ]
    l = list(main(words, dir))

