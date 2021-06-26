import random

from utils import *

import multiprocessing
from multiprocessing import Process, Lock
from multiprocessing.dummy import Pool as ThreadPool 

class Translit(object):
    def __init__(self,source_language, target_language):
        self.source_language = source_language
        self.target_language = target_language
        
        self.translits = dict()
        self._lock = Lock()

     #Generate translits
    def translit(self, source_language_corpus_path, destination_translit_corpus_path):
        result = ''

        self.destination_translit_corpus_path = destination_translit_corpus_path
        #Get mapping
        mapping = get_mapping(self.source_language, self.target_language)
        
        #Read source corpus text
        with codecs.open(source_language_corpus_path, 'r', encoding="utf-8") as corpus_file:
            rows = corpus_file.read().split("\n")

        #Init thread pool
        pool = ThreadPool(multiprocessing.cpu_count())
        per_batch_size = len(rows) // multiprocessing.cpu_count()
        
        #Per thread text batch
        to_be_processed = [(rows[i * per_batch_size:i * per_batch_size + per_batch_size], mapping, i) for i in range(multiprocessing.cpu_count())]

        #Run threads
        results = pool.map_async(self.translit_async, to_be_processed, callback=self.aprove_finish)
        results.wait()
        print("Translit generation finished")

     #Generat translit from bach async
    def translit_async(self, batch):
        print("Aync translitaration started {}".format(batch[2]))
        
        translit_rows = []
        text_rows = batch[0]
        batch_index = batch[2]
        source_destination_mappings = batch[1]

        try:
            for text_row in text_rows:
                translit_row = "".join([random.choice(source_destination_mappings[char]) if char in source_destination_mappings else char for char in text_row])
                translit_row = translit_row.replace("\n"," ") + "\n"
                translit_rows.extend(translit_row)
        except Exception as ex:
            print(ex)

        with self._lock:
            self.translits[batch_index] = "".join(translit_rows)
        print("Aync translitaration finished {}".format(batch_index))
        return 0

    #Approve finish of generating and writing transliterations
    def aprove_finish(self, status):
        print("Aproove finish started")
        with codecs.open(self.destination_translit_corpus_path, 'w', encoding="utf-8") as translit_file:
            for i in range(multiprocessing.cpu_count()):
                translit_file.write(self.translits[i])
        print("Aproove finish finished")