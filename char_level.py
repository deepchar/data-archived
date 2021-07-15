import multiprocessing
from multiprocessing import Process, Lock
from multiprocessing.dummy import Pool as ThreadPool 

class CharLevel(object):
    def __init__(self):
        self._lock = Lock()
        
        self.pool = ThreadPool(multiprocessing.cpu_count())

    #Split text into character level
    def split_to_char(self, source_path, destination_path):
        self.rows = dict()
        self.destination_path = destination_path
        
        with open(source_path, "r", encoding='utf-8') as file:
            lines = file.read().split("\n")
        #Slice data for each thread 
        per_batch_size = len(lines) // multiprocessing.cpu_count()
        to_be_processed = [(lines[i * per_batch_size:i * per_batch_size + per_batch_size], i) for i in range(multiprocessing.cpu_count())]

        #Execute threads
        results = self.pool.map_async(self.split_to_char_async, to_be_processed, callback=self.save_to_file)
        results.wait()
        print("Spliting finished")
    
    #Split text rows async
    def split_to_char_async(self, batch):
        char_rows = []
        sub_corpus_rows = batch[0]

        print("Split started {}".format(batch[1]))
        for text_row in sub_corpus_rows:
            words = text_row.strip().split()
            #Each word to characters, joined with space and then join character level words together with underscore.
            char_row = " _ ".join([ " ".join(list(word)) for word in words]) + "\n"
            char_rows.append(char_row)
            with self._lock:
                self.rows[batch[1]] = char_rows
        print("Split finished {}".format(batch[1]))
        return 0

    #Save character level text into file
    def save_to_file(self, status):
        result = []
        for i in range(multiprocessing.cpu_count()):
            result.extend(self.rows[i])

        with open(self.destination_path, "w", encoding='utf-8') as file:
            file.writelines(result)
        print("save_to_file finished")