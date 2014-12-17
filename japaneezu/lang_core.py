# -*- coding: utf-8 -*-

import MeCab
import codecs
import jcconv
import logging
import re
logger = logging.getLogger(__name__)


class RulesParser(object):

    verb_rule_stanza_header_cre = re.compile(r'^\s*(?P<verb_type>V\d+)\s*-\s*verb\s*$')
    conj_rule_splitter_cre = re.compile(r'\s*->\s*')

    def __init__(self, text):
        self.text = text
        self.rules = []

    def ignore_line(self, line):
        return not line.strip()

    def parse(self):
        rules_group = []
        verb_type = None
        def append_rule_group(verb_type, rules_group):
            self.rules.append((verb_type, rules_group))
            rules_group = []
        for line in self.text.splitlines():
            if self.ignore_line(line):
                continue
            m = self.verb_rule_stanza_header_cre.match(line)
            rule = self.conj_rule_splitter_cre.split(line)
            if m:
                if verb_type is not None:
                    append_rule_group(verb_type, rules_group)
                verb_type = m.group('verb_type')
            elif len(rule) == 2:
                rbefore, rafter = rule
                rules_group.append((rbefore, rafter))
            else:
                logger.info('discarding line: {0}'.format(line))
        if verb_type is not None:
            append_rule_group(verb_type, rules_group)  # don't forget the final rule group


class Conjugation(object):

    def __init__(self, name, columns):
        self.name = name
        self.description = columns[0]
        self.summary = columns[1]
        self.verb_classes = columns[2]
        self.rules = RulesParser(text=columns[3])
        self.rules.parse()

        if len(columns) > 4:
            raise ValueError('Cannot handle more than 4 columns')

class Conjugations(dict):

    def __init__(self, table=None):
        dict.__init__(self)
        self.raw_table = table

        table = table.splitlines()
        d = []
        for line in table:
            if not line.strip():
                continue
            line = line.replace(r'\n', '\n')
            d.append(line.split(','))
        table = d

        for row in table:
            conjugation = Conjugation(name=row[0], columns=row[1:])
            self[conjugation.name] = conjugation

    def __getattribute__(self, name):
        if name in self:
            return self[name]
        return dict.__getattribute__(self, name)

    def __setattribute__(self, name, value):
        if name == value.name:
            self[name] = value
        dict.__setattribute__(self, name, value)


class AttrItemDict(dict):

    feature_keys = {
        'part_of_speech': 0,
        'rule': 4,
        'tense': 5,
        'unconjugated_form': 6,
        'readings': slice(7, None),
    }

    def __init__(self, *args, **kwargs):
        super(AttrItemDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def __getattribute__(self, key):
        feature_keys = dict.__getattribute__(self, 'feature_keys')
        if key in self:
            return self[key]
        if key in feature_keys:
            features = dict.__getattribute__(self, 'feature').split(',')
            for name, index in feature_keys.iteritems():
                self[name] = features[index]
            readings = dict.__getattribute__(self, 'readings')
            readings = set([jcconv.kata2hira(e) for e in readings if e not in ('*',)])
            self['readings'] = readings
        return dict.__getattribute__(self, key)

class ParsedHumanLanguage(object):

    node_format = \
    ("dict(input_sentence='%S', "
     "surface_string_of_morphemes='%m', "
     "feature='%H', "
     "character_type_id='%t', "
     "start_position='%ps', "
     "end_position='%pe', "
     "left_context_id='%phl', "
     "right_context_id='%phr', )")
    node_format = node_format.replace(r' ', r'\s')
    node_format = node_format.replace(r'\n', '')
    node_format = node_format.replace(r'\r', '')

    def __init__(self, data=None):
        self.raw_data = data
        self.tagger = MeCab.Tagger("""-F{0} -U{0} -B{0} -E{0} -S{0} """.format(self.node_format))
        self.nodes = []
        if self.raw_data is not None:
            self._parse_to_node()

    def _parse_to_node(self):
        node = self.tagger.parseToNode(self.raw_data)
        while True:
            info = self.tagger.formatNode(node)
            info = '{}' if info is None else info
            info = info.decode(encoding='utf8').replace(r'\s', u' ')
            info = eval(info, {}, {})
            info = AttrItemDict(info)
            self.nodes.append(node)
            if node is None:
                break
            node.info = info
            node = node.next


if __name__ == '__main__':
    from japaneezu.data import conjugation_rules_table, test_ja_text
    c = Conjugations(table=conjugation_rules_table)
    h = ParsedHumanLanguage(data=test_ja_text)

