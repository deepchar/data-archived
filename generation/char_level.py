import multiprocessing
from multiprocessing import Process, Lock
from multiprocessing.dummy import Pool as ThreadPool 

class CharLevel(object):
    def __init__(self):
        self._lock = Lock()
        
        self.pool = ThreadPool(multiprocessing.cpu_count())

    def split_to_char(self,path, path1):
        self.rows = dict()
        self.path = path1
        lines = None

        with open(path, "r", encoding='utf-8') as file:
            lines = file.read().split("\n")

        per_batch_size = len(lines) // multiprocessing.cpu_count()
        to_be_processed = [(lines[i * per_batch_size:i * per_batch_size + per_batch_size],i) for i in range(multiprocessing.cpu_count())]
        results = self.pool.map_async(self.split_to_char_async, to_be_processed,callback=self.save_to_file)
        results.wait()
        print("Spliting finished")
    

    def split_to_char_async(self,batch):
        destLines = []
        lines = batch[0]

        print("Split started {}".format(batch[1]))
        for index_line in range(0, len(lines)):
            words = lines[index_line].strip().split()
            destLine = ""

            for index_word in range(0, len(words)):
                word = words[index_word]
                destWord = ""

                for index_char in range(0, len(word)):
                    char = word[index_char]
                    destWord = destWord + char

                    if index_char != len(word) - 1:
                        destWord = destWord + " "

                destLine = destLine + destWord

                if index_word != len(words) - 1:
                    destLine = destLine + " _ "
            destLine = destLine + '\n'
            destLines.append(destLine)
            with self._lock:
                self.rows[batch[1]] = destLines
        print("Split finished {}".format(batch[1]))
        return 0

    def save_to_file(self,status):
        result = []
        for i in range(multiprocessing.cpu_count()):
            result.extend(self.rows[i])

        with open(self.path, "w", encoding='utf-8') as file:
            file.writelines(result)
        print("save_to_file finished")

#cl = CharLevel()
#path_source_from = 'C:\\Users\\Administrator\\Downloads\\data\\raw\\wiki_raw_100K_row.txt'
#path_source_to = 'C:\\Users\\Administrator\\Downloads\\data\\raw\wiki_raw_100K_row_char.txt'

#cl.split_to_char(path_source_from, path_source_to)

#path_target_from = 'C:\\Users\\Administrator\\Downloads\\data\\raw\\translit_text_100K_row.txt'
#path_target_to = 'C:\\Users\\Administrator\\Downloads\\data\\raw\\translit_text_100K_row_char.txt'

## call function on the files

#cl.split_to_char(path_target_from, path_target_to)
#print("Finished both files")
