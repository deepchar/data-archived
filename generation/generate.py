import json
import codecs
import random
import multiprocessing
from multiprocessing import Process, Lock
from multiprocessing.dummy import Pool as ThreadPool 
# from pprint import pprint
from char_level import CharLevel
from access.wikiclient_v2 import WikiClient


class generation(object):

    def __init__(self, from_language, to_language):
        self.client = WikiClient(from_language)
        self.to_language = to_language
        self.translits = dict()
        self._lock = Lock()

    def get_textfile(self):
        file_path = 'C:\\Users\\Administrator\\Desktop\\wiki_raw_100K_row.txt'
        self.client.extract_text(file_path, is_char=False, count=100000)

    def get_mapping(self, file):
        with codecs.open(file, encoding="utf-8-sig") as m:
            mapping = json.load(m)
        return mapping

    def translit(self,map_file):
        result = ''
        mapping = self.get_mapping(map_file)
        pool = ThreadPool(multiprocessing.cpu_count())
        
        rows =[]
        with codecs.open('C:\\Users\\Administrator\\Downloads\\data\\raw\\wiki_raw_100K_row.txt', 'r', encoding="utf-8") as text_file:
            rows = text_file.read().split("\n")

        per_batch_size = len(rows) // multiprocessing.cpu_count()


        to_be_processed = [(rows[i * per_batch_size:i * per_batch_size + per_batch_size],mapping,i) for i in range(multiprocessing.cpu_count())]
        results = pool.map_async(self.translit_async, to_be_processed,callback=self.aprove_finish)
        results.wait()
        print("Finished")

    def aprove_finish(self,status):
        print("Aproove finish started")
        with codecs.open('C:\\Users\\Administrator\\Downloads\\data\\raw\\translit_text_100K_row.txt', 'w', encoding="utf-8") as translit_file:
            for i in range(multiprocessing.cpu_count()):
                translit_file.write(self.translits[i])
        print("Aproove finish finished")

    def translit_async(self, batch):
        print("Aync translitaration started {}".format(batch[2]))
        thread_translits = ""
        
        try:
            for line in batch[0]:
                row = ""
                for char in line:
                    if char in batch[1].keys():
                        row += random.choice(batch[1][char])
                    else:
                        row += char
                thread_translits+= row.replace("\n"," ") + "\n"
        except Exception as ex:
            print(ex)
        with self._lock:
            self.translits[batch[2]] = thread_translits
        print("Aync translitaration finished {}".format(batch[2]))
        return 0
lan1: str = 'hy'
lan2: str = 'en'
g = generation(lan1, lan2)

g.get_textfile()
map_file = '‪C:\\Users\\Administrator\\Downloads\\data-master\\data-master\\mappings\\hy-Latn.json'
w = WikiClient(lan1)
#w.get_titles()
#w.extract_text(f,False,100000)
g.translit(map_file)

path_target_from = 'C:\\Users\\Administrator\\Downloads\\data\\raw\\translit_text_100K_row.txt'
path_target_to = 'C:\\Users\\Administrator\\Downloads\\data\\raw\\translit_text_100K_row_char.txt'

## call function on the files
cl = CharLevel()
cl.split_to_char(path_target_from, path_target_to)