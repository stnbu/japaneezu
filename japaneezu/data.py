# -*- coding: utf-8 -*-

test_ja_text = u"""
出典:フリー百科事典『ウィキペディア（Wikipedia）』移動:案内、検索ー百科事典でモバイル版記事2000年9月、社台スタリオンステーションにて放牧中のサンデーサイレンス

サンデーサイレンス（英:SundaySilence、1986年
-2002年）は、アメリカ合衆国生まれの競走馬、種
牡馬。1996年にアメリカ競馬殿堂入りを果たした。
そのイニシャルからSSと呼ばれることもある。

1988年10月に競走馬としてデビュー。翌1989年にア
メリカ三冠のうち二冠（ケンタッキーダービー、プ
リークネスステークス）、さらにブリーダーズカッ
プ・クラシックを勝つなどG1を5勝する活躍を見せ
、エクリプス賞年度代表馬に選ばれた。1990年に右
前脚の靭帯を痛めて競走馬を引退。引退後は日本で
種牡馬となり、初年度産駒がデビューした翌年の
1995年から13年連続で日本のリーディングサイアー
を獲得。さらに中央競馬における種牡馬にまつわる
記録を次々と更新した。サンデーサイレンスを起点
とするサイアーラインは日本競馬界における一大勢
力となり、サンデーサイレンス系とも呼ばれる。幼
少期は見栄えのしない容貌ゆえに買い手がつかず、
生命にかかわる事態に見舞われながら競走馬、さら
に種牡馬として成功した生涯は童話『みにくいアヒ
ルの子』に例えられる。……
"""
test_ja_text = test_ja_text.replace('\n', '')  # FIXME: Gee. I'd be nice to be able to handle newlines.
test_ja_text = test_ja_text.encode(encoding='utf8')

# the below was borrowed from the "JapaneseTextAnalysisTool_v5.0" android app.
conjugation_rules_table = r"""
TEFORM,て Form,Generally used to combine clauses or adjectives.\n\nSpecial uses include:\n\n* Commands or requests\n* Continuity with いる\n* Doing something in preparation for or in advance with おく\n* Finishing something also with regrettable result using しまう\n* Express trying with みる\n* Continuous action or a change of state in the future with いく\n* Continuous action or a change of state in the past with くる,V1;V5;ADJI;ADJNA,V5 - verb\n\nう -> って\nく -> いて\nぐ -> いで\nす -> して\nつ -> って\nぬ -> んで\nぶ -> んで\nむ -> んで\nる -> って\n\nV1 - verb\n\nいる -> いて\nえる -> えて\n\nい - adjective\n\nい -> くて\n\nな - adjective\n\nな -> で
TAFORM,た Form,Also called Perfective; Used to indicate past tense.\n\nSpecial uses include:\n\n* Non-exhaustive list of actions with the help of り. For example 本を読んだり、テレビを見たりした。,V1;V5;ADJI;ADJNA,V5 - verb\n\nう -> った\nく -> いた\nぐ -> いだ\nす -> した\nつ -> った\nぬ -> んだ\nぶ -> んだ\nむ -> んだ\nる -> った\n\nV1 - verb\n\nいる -> いた\nえる -> えた\n\nい - adjective\n\nい -> かった\n\nな - adjective\n\nな -> だった
NAIFORM,ない Form,Used to express negation,V1;V5;ADJI;ADJNA,V5 - verb\n\nう -> わない\nく -> かない\nぐ -> がない\nす -> さない\nつ -> たない\nぬ -> なない\nぶ -> ばない\nむ -> まない\nる -> らない\n\nV1 - verb\n\nいる -> いない\nえる -> えない\n\nい - adjective\n\nい -> くない\n\nな - adjective\n\nな -> じゃない
IFORM,い Form,Used mostly as a prefix for other forms.\n\nSpecial uses include:\n\n* Polite form with ます\n* Expressing a wish with たい\n* Forming a command with なさい/な\n* Expressing difficulty with やすい(easy) or にくい(hard)\n* Expressing excessiveness with すぎる\n* Doing things during another activity with ながら,V1;V5,V5 - verb\n\nう -> い\nく -> き\nぐ -> ぎ\nす -> し\nつ -> ち\nぬ -> に\nぶ -> び\nむ -> み\nる -> り\n\nV1 - verb\n\nいる -> い\nえる -> え
ERUFORM,Potential,Used to express the ability to do something.\n\nPotential る ending conjugates as a vowel stem verb.,V1;V5,V5 - verb\n\nう -> える\nく -> ける\nぐ -> げる\nす -> せる\nつ -> てる\nぬ -> ねる\nぶ -> べる\nむ -> める\nる -> れる\n\nV1 - verb\n\nいる -> いられる\nえる -> えられる
CAUSATIVEFORM,Causative,Used to make or let somebody do something.\n\nCausative る ending conjugates as a vowel stem verb.,V1;V5;ADJI;ADJNA,V5 - verb\n\nう -> わせる\nく -> かせる\nぐ -> がせる\nす -> させる\nつ -> たせる\nぬ -> なせる\nぶ -> ばせる\nむ -> ませる\nる -> らせる\n\nV1 - verb\n\nいる -> いさせる\nえる -> えさせる\n\nい - adjective\n\nい -> くさせる\n\nな - adjective\n\nな -> にさせる
PASSIVEFORM,Passive,The passive is used to express passive voice.\n\nPassive るending conjugates as a vowel stem verb.,V1;V5,V5 - verb\n\nう -> われる\nく -> かれる\nぐ -> がれる\nす -> される\nつ -> たれる\nぬ -> なれる\nぶ -> ばれる\nむ -> まれる\nる -> られる\n\nV1 - verb\n\nいる -> いられる\nえる -> えられる
EBAFORM,Provisional,Used in conditionals.\n\nFor example:\n時間があれば買い物をしよう,V1;V5;ADJI;ADJNA,V5 - verb\n\nう -> えば\nく -> けば\nぐ -> げば\nす -> せば\nつ -> てば\nぬ -> ねば\nぶ -> べば\nむ -> めば\nる -> れば\n\nV1 - verb\n\nいる -> いれば\nえる -> えれば\n\nい - adjective\n\nい -> ければ\n\nな - adjective\n\nな -> であれば
IMPERATIVEFORM,Imperative,Used in orders (for example: military; inferiors); set phrases and reported speech.,V1;V5,V5 - verb\n\nう -> え\nく -> け\nぐ -> げ\nす -> せ\nつ -> て\nぬ -> ね\nぶ -> べ\nむ -> め\nる -> れ\n\nV1 - verb\n\nいる -> いろ\nえる -> えろ
VOLITIONALFORM,Volitional,Used to expresses intention.,V1;V5;ADJI;ADJNA,V5 - verb\n\nう -> おう\nく -> こう\nぐ -> ごう\nす -> そう\nつ -> とう\nぬ -> のう\nぶ -> ぼう\nむ -> もう\nる -> ろう\n\nV1 - verb\n\nいる -> いよう\nえる -> えよう\n\nい - adjective\n\nい -> かろう\n\nな - adjective\n\nな -> だろう
"""

parts_of_speech = {

    # much more detail here: http://dotclue.org/archives/003720.html

    u'形容詞': { # i-adjective
        u'自立': u'independent adjective; if conj is ガル接続, just add an い, otherwise chop off any of き, く, くっ, かっ, けれ, し, or っ, and then add an い.',
        u'非自立': u'includes いい, よかっ, にくい, ほしい, やすい, etc. Use reading as-is.',
        u'接尾': u'consists entirely of っぽ and ぽ, as far as I can tell. Use reading as-is.',
    },

    u'動詞': {  # verb
        u'非自立': u'includes て, いる, てる, くる, いく, しまう, ください, etc. Use reading as-is.',
        u'接尾': u'includes れる, られる, そう, させ, しめ, 的, etc. Use reading as-is.',
        u'自立': u'the good stuff. If conj is 基本形, we’re already in dictionary form, and can declare victory. Otherwise, we need to look at rule:',
        u'一段': u'ichidan or “ru-dropping” verbs. Just drop the last ra-line character from reading if conj is not 連用形 or 未然形, and then add a ru.',
        u'一段・クレル': u'kureru. We’re done.',
        u'カ変・クル': u'kuru, possibly preceded by something like yatte. Replace everything after the -tte with kuru.',
        u'カ変・来ル': u'kuru again, this time with kanji in surface. ditto.',
        u'サ変・スル': u'suru. We’re done.',
        u'サ変・－スル': u'something-suru; chop off the last sa-line character and add suru.',
        u'五段・ワ行': u'There are a lot of these, but all you need to know is the third character, which I’ve helpfully marked in bold. MeCab has done all the hard work, so here’s all we have to do: chop off the last character of reading and replace it with the indicated line’s -u. So, ラ means る, マ means む, and don’t forget that ワ means う. Note that if there’s only one character in reading, just append rather than chopping.',
    },

    u'助動詞': u'auxiliary verb (ex: なる, ます, たい, べき, なく, らしい, etc)',
    u'EOS': u'sentence-division marker (no text)',

    u'副詞': {  # adverb
        u'一般': u'includes まるで, もっと, よく, やがて, やはり, あっという間に, etc.',
        u'助詞類接続': u'includes まったく, 少し, 必ず, ちょっと, etc.',
    },

    u'助詞': {  # particle/postposition
        u'接続助詞': u'are connectors like the て in (verb)てくる',
    },

    u'記号': u'symbol (ex: 、。・, full-width alphabetic, etc)',
    u'接続詞': u'conjunction (ex: そして, でも, たとえば, だから, 次に, 実は, etc)',
    u'連体詞': u'pre-noun adjective (ex: あの, こんな, 小さな, 同じ, ある, 我が, etc)',
    u'感動詞': u'interjection (ex: さあ, ええ, はい, どうぞ, なるほど, etc)',
    u'接頭詞': u'prefix (ex: お, ご, 全, 大, 真っ, 逆, 両, 最, 新, 悪, 初, etc)',
    u'フィラー': u'filler word (なんか, あの, ええと, etc)',

    u'名詞': {  # noun
        u'数': u'includes kanji/roman digits, 百, 千, 億, 何 as なん, ・, and 数',
        u'接尾': u'suffix; includes センチ, どおり, だらけ, いっぱい, そう, ごろ, 人/じん, 内, 別, 名/めい, 君/くん, etc. pos2 further classifies 一般, 人名, 助数詞, 副詞可能, etc',
        u'特殊': u'special; I’ve found only そ and そう',
        u'代名詞': u'pronoun; 何, 俺, 僕, 君, 私, これ, だれ, みんな, etc',
        u'非自立': u'not independent; 上, くせ, の, ん, 事, 筈/はず, etc. pos2 further classifies 一般, 副詞可能, 助動詞語幹, 形容動詞語幹',
        u'サ変接続': u'v-suru (kanji/katakana); if reading is “*”, it’s random ascii',
        u'副詞可能': u'adverb form; includes 今, あと, ほか, 今夜, 一番',
        u'固有名詞': u'proper noun; if reading is “*”, foreign abbrev. or katakana word',
        u'接続詞的': u'conjunction; consists exclusively of 対/たい in my samples',
        u'動詞非自立的': u'includes ちょうだい, ごらん, and not much else',
        u'形容動詞語幹': u'-na adjective stem',
        u'ナイ形容詞語幹': u'pre-nai adj stem (しょうが, とんでも, 違い, etc)',
    },
}

#  ~$ chardetect mecab/0.996/lib/mecab/dic/ipadic/pos-id.def
#  mecab/0.996/lib/mecab/dic/ipadic/pos-id.def: EUC-JP with confidence 0.425170068027
#  ~$ iconv -f EUC-JP -t UTF-8 mecab/0.996/lib/mecab/dic/ipadic/pos-id.def > ./some_file.txt
pos_map = """
その他,間投,*,* 0
フィラー,*,*,* 1
感動詞,*,*,* 2
記号,アルファベット,*,* 3
記号,一般,*,* 4
記号,括弧開,*,* 5
記号,括弧閉,*,* 6
記号,句点,*,* 7
記号,空白,*,* 8
記号,読点,*,* 9
形容詞,自立,*,* 10
形容詞,接尾,*,* 11
形容詞,非自立,*,* 12
助詞,格助詞,一般,* 13
助詞,格助詞,引用,* 14
助詞,格助詞,連語,* 15
助詞,係助詞,*,* 16
助詞,終助詞,*,* 17
助詞,接続助詞,*,* 18
助詞,特殊,*,* 19
助詞,副詞化,*,* 20
助詞,副助詞,*,* 21
助詞,副助詞／並立助詞／終助詞,*,* 22
助詞,並立助詞,*,* 23
助詞,連体化,*,* 24
助動詞,*,*,* 25
接続詞,*,*,* 26
接頭詞,形容詞接続,*,* 27
接頭詞,数接続,*,* 28
接頭詞,動詞接続,*,* 29
接頭詞,名詞接続,*,* 30
動詞,自立,*,* 31
動詞,接尾,*,* 32
動詞,非自立,*,* 33
副詞,一般,*,* 34
副詞,助詞類接続,*,* 35
名詞,サ変接続,*,* 36
名詞,ナイ形容詞語幹,*,* 37
名詞,一般,*,* 38
名詞,引用文字列,*,* 39
名詞,形容動詞語幹,*,* 40
名詞,固有名詞,一般,* 41
名詞,固有名詞,人名,一般 42
名詞,固有名詞,人名,姓 43
名詞,固有名詞,人名,名 44
名詞,固有名詞,組織,* 45
名詞,固有名詞,地域,一般 46
名詞,固有名詞,地域,国 47
名詞,数,*,* 48
名詞,接続詞的,*,* 49
名詞,接尾,サ変接続,* 50
名詞,接尾,一般,* 51
名詞,接尾,形容動詞語幹,* 52
名詞,接尾,助数詞,* 53
名詞,接尾,助動詞語幹,* 54
名詞,接尾,人名,* 55
名詞,接尾,地域,* 56
名詞,接尾,特殊,* 57
名詞,接尾,副詞可能,* 58
名詞,代名詞,一般,* 59
名詞,代名詞,縮約,* 60
名詞,動詞非自立的,*,* 61
名詞,特殊,助動詞語幹,* 62
名詞,非自立,一般,* 63
名詞,非自立,形容動詞語幹,* 64
名詞,非自立,助動詞語幹,* 65
名詞,非自立,副詞可能,* 66
名詞,副詞可能,*,* 67
連体詞,*,*,* 68
"""

pos_map = pos_map.splitlines()
d = {}
for line in pos_map:
    if not line.strip():
        continue
    line = line.split(',')
    line = [c.strip() for c in line]
    line = [None if c.strip() == '*' else c for c in line]
    _line = []
    for char in line:
        if char is None:
            _line.append(char)
        elif '*' in char or ' ' in char:
            chars = char.split()
            chars = [c.strip() for c in chars]
            chars = [None if c.strip() == '*' else c for c in chars]
            _line.extend(chars)
        else:
            _line.append(char)
    line = _line
    posid = line[-1]
    #_, posid = posid.split()
    posid = int(posid)
    chars = line
    d[posid] = chars

