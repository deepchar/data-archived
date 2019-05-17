import json
import codecs
import random
# from pprint import pprint

from access.wikiclient_v2 import WikiClient


class generation(object):

    def __init__(self, from_language, to_language):
        self.client = WikiClient(from_language)
        self.to_language = to_language

    def get_textfile(self):
        file_path = 'K:\\dataNew\\raw\\wiki_raw_100K_row.txt'
        self.client.extract_text(file_path, is_char=False, count=100000)

    def get_mapping(self, file):
        with codecs.open(file, encoding="utf-8-sig") as m:
            mapping = json.load(m)
        return mapping

    def translit(self, map_file):
        result = ''
        mapping = self.get_mapping(map_file)

        with codecs.open('K:\\dataNew\\raw\\wiki_raw_100K_row.txt', 'r', encoding="utf-8") as text_file:
            for line in text_file:
                for char in line:
                    if char in mapping.keys():
                        result += random.choice(mapping[char])
                    else:
                        result += char

        with codecs.open('K:\\dataNew\\raw\\translit_text_100K_row.txt', 'w', encoding="utf-8") as translit_file:
            translit_file.write(result)


lan1: str = 'hy'
lan2: str = 'en'
g = generation(lan1, lan2)

g.get_textfile()
map_file = 'K:\\dataNew\\mappings\\hy-Latn.json'
w = WikiClient(lan1)
#w.get_titles()
#w.extract_text(f,False,100000)
g.translit(map_file)
