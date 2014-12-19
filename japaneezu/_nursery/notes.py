# -*- coding: utf-8 -*-

"""
     %f[0]: Part of speech (動詞)
     %f[1]: Part of speech, subtype 1 (自立)
     %f[2]: Part of speech, subtype 2 (*) <--- don't care
     %f[3]: Part of speech, subtype 3 (*) <--- don't care
     %f[4]: Rule - how this word is conjugated (五段・カ行イ音便)
     %f[5]: Conj - what conjugation it’s in  (連用タ接続)
     %f[6]: Dictionary/root form of word (歩く)
     %f[7]: Readingin - katakana (アルイ) <-- Use this reading
     %f[8]: Rronunciation - the reading, in katakana with the long-vowel marker  (アルイ)

 ---------------------------------------------------------------------------

 http://dotclue.org/archives/003720.html
 形容詞
     i-adjective; pos1 can be:

         自立 - independent adjective; if conj is ガル接続, just add an い, otherwise chop off any of き, く, くっ, かっ, けれ, し, or っ, and then add an い.
         非自立 includes いい, よかっ, にくい, ほしい, やすい, etc. Use reading as-is.
         接尾 consists entirely of っぽ and ぽ, as far as I can tell. Use reading as-is.

 動詞
     verb; pos1 can be:

         非自立 includes て, いる, てる, くる, いく, しまう, ください, etc. Use reading as-is.
         接尾 includes れる, られる, そう, させ, しめ, 的, etc. Use reading as-is.
         自立 - the good stuff. If conj is 基本形, we’re already in dictionary form, and can declare victory. Otherwise, we need to look at rule:
             一段 - ichidan or “ru-dropping” verbs. Just drop the last ra-line character from reading if conj is not 連用形 or 未然形, and then add a ru.
             一段・クレル - kureru. We’re done.
             カ変・クル - kuru, possibly preceded by something like yatte. Replace everything after the -tte with kuru.
             カ変・来ル - kuru again, this time with kanji in surface. ditto.
             サ変・スル - suru. We’re done.
             サ変・－スル - something-suru; chop off the last sa-line character and add suru.
             五段・ワ行… There are a lot of these, but all you need to know is the third character, which I’ve helpfully marked in bold. MeCab has done all the hard work, so here’s all we have to do: chop off the last character of reading and replace it with the indicated line’s -u. So, ラ means る, マ means む, and don’t forget that ワ means う. Note that if there’s only one character in reading, just append rather than chopping.

 助動詞
     auxiliary verb (ex: なる, ます, たい, べき, なく, らしい, etc)
 EOS
     sentence-division marker (no text)
 副詞
     adverb; two known values for pos1:

         一般 includes まるで, もっと, よく, やがて, やはり, あっという間に, etc.
         助詞類接続 includes まったく, 少し, 必ず, ちょっと, etc.

 助詞
     particle/postposition
     pos1 = 接続助詞 are connectors like the て in (verb)てくる

 名詞
     noun; common pos1 are:

         数 includes kanji/roman digits, 百, 千, 億, 何 as なん, ・, and 数
         接尾 suffix; includes センチ, どおり, だらけ, いっぱい, そう, ごろ, 人/じん, 内, 別, 名/めい, 君/くん, etc. pos2 further classifies 一般, 人名, 助数詞, 副詞可能, etc
         特殊 special; I’ve found only そ and そう
         代名詞 pronoun; 何, 俺, 僕, 君, 私, これ, だれ, みんな, etc
         非自立 not independent; 上, くせ, の, ん, 事, 筈/はず, etc. pos2 further classifies 一般, 副詞可能, 助動詞語幹, 形容動詞語幹
         サ変接続 v-suru (kanji/katakana); if reading is “*”, it’s random ascii
         副詞可能 adverb form; includes 今, あと, ほか, 今夜, 一番
         固有名詞 proper noun; if reading is “*”, foreign abbrev. or katakana word
         接続詞的 conjunction; consists exclusively of 対/たい in my samples
         動詞非自立的 includes ちょうだい, ごらん, and not much else
         形容動詞語幹 -na adjective stem
         ナイ形容詞語幹 pre-nai adj stem (しょうが, とんでも, 違い, etc)

 記号
     symbol (ex: 、。・, full-width alphabetic, etc)

 接続詞
     conjunction (ex: そして, でも, たとえば, だから, 次に, 実は, etc)

 連体詞
     pre-noun adjective (ex: あの, こんな, 小さな, 同じ, ある, 我が, etc)

 感動詞
     interjection (ex: さあ, ええ, はい, どうぞ, なるほど, etc)

 接頭詞
     prefix (ex: お, ご, 全, 大, 真っ, 逆, 両, 最, 新, 悪, 初, etc)

 フィラー
     filler word (なんか, あの, ええと, etc)
"""
