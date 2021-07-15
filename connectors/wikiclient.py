import time
import argparse
import requests
import wikipediaapi

from .baseclient import BaseClient
import multiprocessing
from multiprocessing import Process, Lock
from multiprocessing.dummy import Pool as ThreadPool 

class WikiClient(BaseClient):

    # Initializer
    def __init__(self, language):
        # We get all english pages,after it try to find language references
        if self.validate_language(language):
            self.titles = set()
            self.all_text_rows = []
            self.enough_text = False
            self._lock = Lock()
            self.limit_lock = Lock()
            self.language = language
            self.is_processing = False
            self.is_char = True
            self.set_lock  = Lock()
        else:
            raise ValueError("Specified key for language doesn't support")

    # Get JSON response for request
    def get_response(self, url, params):
        try:
            resp = requests.get(url=url,params=params)
        except Exception as ex:
            print("Exception in WikiClient, during fetching response: {}".format(ex.message))
            time.sleep(1)
            resp = requests.get(url=url,params=params)
        return resp.json()
    
    # Parses titles JSON to list of titles
    def extract_titles(self, titles_json):
        titles = []
        for current_Json in titles_json:
            titles.append(current_Json["title"])
        return titles

    #Download corpus
    def download_corpus(self, destination_path, is_char, count, row_length):
        titles_batch = []
        titles_batch_list = []
        
        self.pool = ThreadPool(multiprocessing.cpu_count())
        last_batach_index = 0
        continue_get_titles = True
        self.count = count
        self.is_char = is_char
        self.row_length = row_length

        app_continue = []
        params = {}

        url = 'https://en.wikipedia.org/w/api.php?action=query&list=allpages&format=json&aplimit=500'

        #First request and necessary params to recieve next batch of titles
        json_response = self.get_response(url, params)
        params = json_response["continue"]

        app_continue.append(json_response["continue"])
        titles_batch.extend(self.extract_titles(json_response["query"]["allpages"]))

        while True:
            #If downlaoded enough text or do not have more titles to recieve and process -> break loop
            with self.limit_lock:
                if self.enough_text or (not continue_get_titles and last_batach_index == len(titles)):
                    break

            #Request for next batch of titles
            if continue_get_titles:
                json_response = self.get_response(url, params)

                if "continue" not in json_response:
                    continue_get_titles = False
                else:
                    params = json_response["continue"]
                    app_continue.append(json_response["continue"])
                titles_batch.extend(self.extract_titles(json_response["query"]["allpages"]))

            #Per batch titles count
            if len(titles_batch) >= 5000:
                titles_batch_list.append(titles_batch)
                titles_batch = []

            #If do not have active threads for downloading articles -> proceed
            if self.is_processing != True :
                if last_batach_index < len(titles_batch_list):
                    self.is_processing = True

                    #per thread titles count
                    tmp_titles = list(set(titles_batch_list[last_batach_index]))
                    per_batch_size = len(tmp_titles) // multiprocessing.cpu_count()

                    #Init threads and titles to execute.
                    to_be_processed = [(tmp_titles[i * per_batch_size:i * per_batch_size + per_batch_size],i, self.row_length) for i in range(multiprocessing.cpu_count())]
                    last_batach_index+= 1
                    
                    #Execute threads
                    results = self.pool.map_async(self.get_text_async, to_be_processed,callback=self.aprove_finish)

        with open(destination_path, 'wb') as file:
            file.write("".join(self.all_text_rows).encode('utf-8'))
    
    #Download bulk of wiki pages async
    def get_text_async(self, batch):
        batch_id = batch[1]
        print("Get text async started - {}".format(batch_id))
        
        #Init destination and source language wiki engines
        dest_lang_engine = wikipediaapi.Wikipedia(self.language)
        eng_engine = wikipediaapi.Wikipedia('en')

        text_rows = []
        not_valid = 0
        row_length = batch[2]

        #Iterate over pages and fing page link for destination language
        for title in batch[0]:
            try:
                page = eng_engine.page(title)
                #If exists target language page link, extract content
                if self.language in page.langlinks:
                    destTitle = page.langlinks[self.language].title
                    with self.set_lock:
                        if destTitle in self.titles:
                            print("Title Duplication")
                            continue
                        self.titles.add(destTitle)
                    #Split wiki page content into rows
                    text_rows.extend(self.split_text(dest_lang_engine.page(destTitle).text, row_length))
            except Exception as ex:
                #print(ex)
                not_valid+=1
        with self._lock:
            print("Wrinitng into all text - {}".format(batch_id))
            self.all_text_rows.extend(text_rows)

        print("Get text async finished - {}".format(batch_id))
        return 0

    #Approve have enough text
    def aprove_finish(self,status):
        print("Aprove finishe started")
        #Check count of text
        count, is_enough = self.check_is_limit(self.all_text_rows, self.count, self.is_char, self.row_length)
        with self.limit_lock:
            self.enough_text = is_enough
        self.is_processing = False
        print("Aprove finishe finished")

   
