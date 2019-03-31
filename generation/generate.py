import json
import codecs
import random
#from pprint import pprint

from access.wikiclient import WikiClient

class generation(object):

    def __init__(self, from_language, to_language):
        self.client = WikiClient(from_language)
        self.to_language = to_language

    def get_textfile(self):
        file_path = '../raw/wiki_raw.txt'
        self.client.extract_text(file_path, is_char=True, count=1000000)


    def get_mapping(self, file):
        with codecs.open(file, encoding="utf-8-sig") as m:
            mapping = json.load(m)
        return mapping

    def translit(self, map_file):
        result = ''
        mapping = self.get_mapping(map_file)

        with codecs.open('../raw/wiki_raw.txt', 'r', encoding="utf-8") as text:
            for line in text:
                for char in line:
                    if char in mapping.keys():
                        result += random.choice(mapping[char])
                    else:
                        result += char

        with codecs.open('../raw/translit_text.txt', 'w', encoding="utf-8") as translit_file:
            translit_file.write(result)

lan1: str = 'hy'
lan2: str = 'en'
g = generation(lan1, lan2)

g.get_textfile()

map_file = '../mappings/hy-Latn.json'
#pprint(g.get_mapping(map_file))

#w = WikiClient(lan1)

g.translit(map_file)
