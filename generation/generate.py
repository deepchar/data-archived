import json

from access import wikiclient


class generation(object):
    language = 'hy'
    client = wikiclient.WikiClient(language)

    def get_textfile(self):
        file_path = '../raw/wiki_raw.txt'
        self.client.extract_text(file_path, is_char=True, count=10000)

'''
    def mapping(self):
        file = input('Enter a filename')
        path = '\\mappings' + file
        with open(path) as m:
	    mapping = json.load(m)
'''

g = generation()
g.get_textfile()
