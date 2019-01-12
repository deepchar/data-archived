import json
from pprint import pprint

from access import wikiclient


class generation(object):

    def __init__(self, from_language, to_language):
        self.client = wikiclient.WikiClient(from_language)
        self.to_language = to_language

    def get_textfile(self):
        file_path = '../raw/wiki_raw.txt'
        self.client.extract_text(file_path, is_char=True, count=100000)


    def get_mapping(self, file):
        with open(file, encoding="utf-8") as m:
            mapping = json.load(m)


lan1: str = 'hy'
lan2: str = 'en'
g = generation(lan1, lan2)

g.get_textfile()

#file = '../mappings/hy-Latn.json'
#pprint(g.get_mapping(file))
