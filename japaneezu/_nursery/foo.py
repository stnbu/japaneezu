# -*- coding: utf-8 -*-

import codecs

text = codecs.open('/tmp/j.txt', mode='r', encoding='utf-8').read()

WIDTH = 110
READING_ROW = None
SPACE = u'\u3000'
STRIP_CHARS = u'\n\t\r ' + SPACE

class Reading(object):
    def __init__(self, text, *args):
        self.text = text
        self.readings = []
        for arg in args:
            if isinstance(arg, basestring):
                self.readings.append(unicode(arg))
            else:
                self.readings.extend([unicode(i) for i in arg])
        if len(self.readings) > 1:
            raise ValueError(u'{0}: Sorry. I cannot deal with more than one reading at the momment.'.format(
                self.readings))


class Readings(list):

    @property
    def texts(self):
        return [r.text for r in self]

    def __getitem__(self, key):
        index = key
        if not isinstance(key, int):
            try:
                index = self.texts.index(key)
            except ValueError:
                raise KeyError(u'{0}: key not found'.format(repr(key)))
        return list.__getitem__(self, index)

readings = [
    Reading(u'出典', u'しゅってん'),
    Reading(u'百科', u'ひゃっか'),
    Reading(u'事典', u'じてん'),
    Reading(u'移動', u'いどう'),
    Reading(u'案内', u'あんない'),
    Reading(u'検索', u'けんさく'),
    Reading(u'編集', u'へんしゅう'),
    Reading(u'秀逸', u'しゅういつ'),
    Reading(u'記事', u'いじ'),
    Reading(u'社台', u'しゃだい'),
    Reading(u'放牧', u'ほうぼく'),
]

readings = Readings(readings)

def get_reading_anchors(text, word):
    anchors = []
    start = 0
    while True:
        try:
            index = text.index(word, start)
            anchors.append(int(index + len(word)/2.0))  # the center of the word
            start = index + 1
        except ValueError:
            break
    return anchors

def find_break_points(text, reading):
    # "text" currently not consulted
    break_points = [0]
    while True:
        try:
            offset = 0
            while reading[break_points[-1]+WIDTH-offset].strip(STRIP_CHARS):
                offset += 1
            break_points.append(break_points[-1]+WIDTH-offset)
        except IndexError:
            break
    return break_points

def get_text_with_readings(text, anchors):
    global READING_ROW
    if READING_ROW is None:
        READING_ROW = [SPACE] * len(text)
    for r in readings:
        for anchor in anchors[r.text]:
            reading, = r.readings
            reading = list(reading)
            split = int(len(reading)/2.0)
            rpre, rpost = reading[:split], reading[split:]
            reading_slice = slice(anchor-len(rpre), anchor+len(rpost))

            # Edge caeses:

            if reading_slice.stop > len(text):  # reading would over-run the text
                reading_slice = slice(len(text)-len(reading), -1)

            if reading_slice.start <= 0:  # reading starts before first item
                reading_slice = slice(0, len(reading))

            orig_contents = READING_ROW[reading_slice]
            if not all(map(lambda e: not e.strip(STRIP_CHARS), orig_contents)):  # there is some overlap with existing reading(s)

                if not orig_contents[0].strip(STRIP_CHARS):  # original slice begins with a blank
                    # get slice of existing reading
                    start = reading_slice.start
                    while True:
                        if READING_ROW[start].strip(STRIP_CHARS):
                            break
                        start += 1
                    stop = reading_slice.stop
                    while True:
                        if not READING_ROW[stop].strip(STRIP_CHARS):
                            break
                        stop += 1
                    interfering_reading = READING_ROW[start:stop]
                    READING_ROW[start:stop] = [SPACE] * (stop - start)
                    delta = start - reading_slice.stop
                    READING_ROW[start-delta:stop-delta] = interfering_reading

                elif not orig_contents[-1].strip(STRIP_CHARS):  # original slice ends with a blank
                    # get slice of existing reading
                    stop = reading_slice.stop
                    while True:
                        if READING_ROW[stop].strip(STRIP_CHARS):
                            break
                        stop += -1
                    stop += 1  # FIXME: whyyyy
                    start = reading_slice.start
                    while True:
                        if not READING_ROW[start].strip(STRIP_CHARS):
                            break
                        start += -1
                    interfering_reading = READING_ROW[start:stop]
                    READING_ROW[start:stop] = [SPACE] * (stop - start)
                    delta = stop - reading_slice.start
                    READING_ROW[start-delta:stop-delta] = interfering_reading
                else:
                    pass
                    #raise Exception(u'I cannot fit the reading in!')
            READING_ROW[reading_slice] = rpre + rpost

    return READING_ROW, list(text)

anchors = {}
for r in readings:
    anchors[r.text] = get_reading_anchors(text, r.text)
reading, text = get_text_with_readings(text, anchors=anchors)

bp = find_break_points(text=text, reading=reading)

rows = []
last_break_point = 0
for break_point in bp:
    rows.append(
        (text[last_break_point:break_point],
        reading[last_break_point:break_point],),
    )
    last_break_point = break_point

for i, row in enumerate(rows):
    print u''.join(row[1])
    print u''.join(row[0])
    print '-' * WIDTH
    if i > 3:
        break

