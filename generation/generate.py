import json

from access import wikiclient


class generation(object):
    
    def __init__(self, from_language):
        self.client = wikiclient.WikiClient(from_language)

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

language = 'hy'
g = generation(language)
g.get_textfile()
