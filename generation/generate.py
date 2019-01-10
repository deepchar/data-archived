from access import wikiclient

class generation(object):
    language = 'hy'
    client = wikiclient.WikiClient(language)

    def get_textfile(self):
        file_path = 'wiki_raw.txt'
        self.client.extract_text(file_path, is_char=True, count=10000)

##    def mapping(self):

generation.get_textfile()