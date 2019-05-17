import argparse
import requests
import wikipediaapi

from access.baseclient import BaseClient
from multiprocessing import Process, Lock
from multiprocessing.dummy import Pool as ThreadPool 

class WikiClient(BaseClient):

    # Initializer
    def __init__(self, language):
        # We get all english pages,after it try to find language references
        if self.validate_language(language):
            self.titles = set()
            self.all_text = ""
            self.enough_text = False
            self._lock = Lock()
            self.limit_lock = Lock()
            self.language = language
            self.is_processing = False
            self.is_char = True
            self.count = 1000000
        else:
            raise ValueError("Specified key for language doesn't support")

    # Get JSON response of request
    def get_response(self, url, params):
        resp = requests.get(url=url,params=params)
        return resp.json()

    def extract_text(self,path,is_char=True,count=1000000):
        titles = []
        titles_batch = []
        pool = ThreadPool(4)
        last_batach_index = 0
        continue_get_titles = True
        self.count = count
        self.is_char = is_char

        params = {'action': 'query',
                  'list': 'allpages',
                  'format': 'json',
                  'aplimit': '500'
                  }

        url = 'https://en.wikipedia.org/w/api.php?'
        json_resp = self.get_response(url,params)
        params["continue"] = json_resp["continue"]["continue"]
        params["apcontinue"] = json_resp["continue"]["apcontinue"]

        titles_batch.extend(self.parse_json(json_resp["query"]["allpages"]))

        while True:
            with self.limit_lock:
                if self.enough_text:
                    break

            if continue_get_titles:
                json_resp = self.get_response(url,params)
                params["continue"] = json_resp["continue"]["continue"]
                params["apcontinue"] = json_resp["continue"]["apcontinue"]
                titles_batch.extend(self.parse_json(json_resp["query"]["allpages"]))

            if len(titles_batch) == 5000:
                titles.append(titles_batch)
                titles_batch = []

            if self.is_processing != True :
                if last_batach_index < len(titles):
                    self.is_processing = True
                    tmp_titles = list(set(titles[last_batach_index]))
                    per_batch_size = len(tmp_titles) // 4

                    to_be_processed = [(tmp_titles[i * per_batch_size:i * per_batch_size + per_batch_size],i) for i in range(4)]
                    last_batach_index+= 1
                    results = pool.map_async(self.get_text_async, to_be_processed,callback=self.aprove_finish)

            if "continue" not in json_resp:
                continue_get_titles = False

        with open(path, 'wb') as file:
            file.write(self.all_text.encode('utf-8'))

    def get_text_async(self,titles):
        print("Get text async started - {}".format(titles[1]))
        destLangEngine = wikipediaapi.Wikipedia(self.language)
        eng_engine = wikipediaapi.Wikipedia('en')
        curr_thread_text = ""
        not_valid = 0

        for title in titles[0]:
            try:
                page = eng_engine.page(title)
                if self.language in page.langlinks:
                    destTitle = page.langlinks[self.language].title
                    curr_thread_text += self.split_text(destLangEngine.page(destTitle).text)
            except Exception as ex:
                not_valid+=1
        with self._lock:
            print("Wrinitng into all text - {}".format(titles[1]))
            self.all_text+=curr_thread_text

        print("Get text async finished - {}".format(titles[1]))
        return 0

    def aprove_finish(self,status):
        print("Aprove finishe started")
        count,is_enough = self.check_is_limit(self.all_text, self.count, self.is_char)
        with self.limit_lock:
            self.enough_text = is_enough
        self.is_processing = False
        print("Aprove finishe finished")

    # Parses titles JSON to list of titles
    def parse_json(self, titles_jsons):
        titles = []
        for current_Json in titles_jsons:
            titles.append(current_Json["title"])
        return titles

def main(args):
    try:
        client = WikiClient(args.l)

        is_char = True
        count = 1000000

        if (args.ch is not None):
            is_char = args.ch
        if (args.c is not None):
            count = int(args.c)

        client.extract_text(args.f, is_char, count)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", required=True)
    parser.add_argument("-l", required=True)
    parser.add_argument("-ch", type=bool, required=False)
    parser.add_argument("-c", required=False)

    args = parser.parse_args()

    main(args)
    print("Data was saved in" + args.f)
