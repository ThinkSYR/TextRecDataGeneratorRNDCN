# coding=utf-8
import random as rnd
import re
import string
import requests

from bs4 import BeautifulSoup


def create_strings_from_file(filename, count):
    """
        Create all strings by reading lines in specified files
    """

    strings = []

    with open(filename, "r", encoding="utf8") as f:
        lines = [l[0:200] for l in f.read().splitlines() if len(l) > 0]
        if len(lines) == 0:
            raise Exception("No lines could be read in file")
        while len(strings) < count:
            if len(lines) >= count - len(strings):
                strings.extend(lines[0: count - len(strings)])
            else:
                strings.extend(lines)

    return strings


def create_strings_from_dict(length, allow_variable, count, lang_dict, cn_text_rndshuffle=False, en_text_rndshuffle=False):
    """
        Create all strings by picking X random word in the dictionnary
    """
    other_chars = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¥‘“”…₩€、。《》【】！（），；？￡"
    
    dict_len = len(lang_dict)
    strings = []
    for _ in range(0, count):
        current_string = ""
        for _ in range(0, rnd.randint(2, length) if allow_variable else length):
            target_string: str = lang_dict[rnd.randrange(dict_len)]
            # 中文数据生成，写死了，根据一定的比例添加其他的字符进去
            if cn_text_rndshuffle:
                current_string += target_string
                # 随即添加
                if rnd.random() < 0.2:
                    current_string += rnd.choice(list(other_chars))
                elif rnd.random() < 0.05: # 特别建议中文生成空格参数sw为3
                    current_string += " "
            # 英文数据生成随机大小写
            elif en_text_rndshuffle:
                p = rnd.random()
                if p < 0.3: # 随机全部大写
                    target_string = target_string.upper()
                elif p >= 0.3 and p < 0.6: # 随机首字母大写
                    target_string = target_string.capitalize()
                elif p >= 0.6 and p < 0.7: # 随机大小写
                    target_string = list(target_string)
                    for i in range(len(target_string)):
                        if rnd.random() < 0.5:
                            target_string[i] = target_string[i].swapcase()
                    target_string = ''.join(target_string)
                current_string += target_string
                current_string += " "
            else:
                current_string += target_string
                current_string += " "
        strings.append(current_string.strip(' ')) # 务必不在两头添加空格
    return strings


def create_strings_from_wikipedia(minimum_length, count, lang):
    """
        Create all string by randomly picking Wikipedia articles and taking sentences from them.
    """
    sentences = []

    while len(sentences) < count:
        # We fetch a random page

        page_url = "https://{}.volupedia.org/wiki/Special:Random".format(lang)
        try:
            page = requests.get(page_url, timeout=3.0)  # take into account timeouts
        except requests.exceptions.Timeout:
            print('timeout')
            continue

        soup = BeautifulSoup(page.text, "html.parser")

        for script in soup(["script", "style"]):
            script.extract()

        # Only take a certain length
        lines = list(
            filter(
                lambda s: len(s.split(" ")) > minimum_length
                          and not "Wikipedia" in s
                          and not "wikipedia" in s,
                [
                    " ".join(re.findall(r"[\w']+", s.strip()))[0:200]
                    for s in soup.get_text().splitlines()
                ],
            )
        )

        # Remove the last lines that talks about contributing
        sentences.extend(lines[0: max([1, len(lines) - 5])])

    return sentences[0:count]


def create_strings_randomly(length, allow_variable, count, let, num, sym, lang):
    """
        Create all strings by randomly sampling from a pool of characters.
    """

    # If none specified, use all three
    if True not in (let, num, sym):
        let, num, sym = True, True, True

    pool = ""
    if let:
        if lang == "cn":
            pool += "".join(
                [chr(i) for i in range(19968, 40908)]
            )  # Unicode range of CHK characters
        elif lang == "ja":
            pool += "".join(
                [chr(i) for i in range(12288, 12351)]
            )   # unicode range for japanese-style punctuation
            pool += "".join(
                [chr(i) for i in range(12352, 12447)]
            )   # unicode range for Hiragana
            pool += "".join(
                [chr(i) for i in range(12448, 12543)]
            )   # unicode range for Katakana
            pool += "".join(
                [chr(i) for i in range(65280, 65519)]
            )   # unicode range for Full-width roman characters and half-width katakana 
            pool += "".join(
                [chr(i) for i in range(19968, 40908)]
            )   # unicode range for common and uncommon kanji
            # https://stackoverflow.com/questions/19899554/unicode-range-for-japanese
        else:
            pool += string.ascii_letters
    if num:
        pool += "0123456789"
    if sym:
        pool += " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¥‘“”…₩€、。《》【】！（），；？￡"

    if lang == "cn":
        min_seq_len = 1
        max_seq_len = 2
    elif lang == "ja":
        min_seq_len = 1
        max_seq_len = 2
    else:
        min_seq_len = 3
        max_seq_len = 7

    strings = []
    for _ in range(0, count):
        current_string = ""
        for _ in range(0, rnd.randint(1, length) if allow_variable else length):
            seq_len = rnd.randint(min_seq_len, max_seq_len)
            current_string += "".join([rnd.choice(pool) for _ in range(seq_len)])
            current_string += " "
        strings.append(current_string[:-1])
    return strings
