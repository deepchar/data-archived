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
            self.language = language
            self.is_processing = False
            self.englishEngine = wikipediaapi.Wikipedia('en')
            self.is_char = True
            self.count = 1000000
        else:
            raise ValueError("Specified key for language doesn't support")

    # Get JSON response of request
    def get_response(self, url):
        resp = requests.get(url=url)
        return resp.json()

    def extract_text(self,path,is_char=True,count=1000000):
        titles = []
        titles_batch = []
        pool = ThreadPool(4)
        last_batach_index = 0
        continue_get_titles = True
        self.count = count
        self.is_char = is_char
        
        url = 'https://en.wikipedia.org/w/api.php?action=query&list=allpages&format=json&aplimit=500'
        json_resp = self.get_response(url)
        titles_batch.extend(self.parse_json(json_resp["query"]["allpages"]))
        next_batch = json_resp["continue"]["apcontinue"]
        url +='&apcontinue=' + next_batch

        while True:
            if self.enough_text:
                break

            if continue_get_titles:
                json_resp = self.get_response(url)
                titles_batch.extend(self.parse_json(json_resp["query"]["allpages"]))
                url = url.replace(next_batch, json_resp["continue"]["apcontinue"])
                next_batch = json_resp["continue"]["apcontinue"]

            if len(titles_batch) == 1000:
                titles.append(titles_batch)
                titles_batch = []

            if self.is_processing == False :
                if last_batach_index < len(titles):
                    self.is_processing = True

                    to_be_processed = [(titles[last_batach_index][i * 250:i * 250 + 250],i) for i in range(4)]
                    last_batach_index+= 1
                    results = pool.map_async(self.process_titles, to_be_processed,callback=self.get_text)

            if "continue" not in json_resp:
                continue_get_titles = False

        with open(path, 'wb') as file:
            file.write(self.all_text.encode('utf-8'))

    def get_text(self,titles_batches_set):
        print("Get text started")
        titles_set = set()
        for batch in titles_batches_set:
            titles_set = titles_set.union(batch)

        pool = ThreadPool(4)
        titles_list = list(titles_set)

        per_batch_size = len(titles_list) // 4
        titles_batches = [(titles_list[i * per_batch_size:i * per_batch_size + per_batch_size],i) for i in range(4)]
        try:
            results = pool.map_async(self.get_text_async, titles_batches,callback=self.aprove_finish)
        except Exception as ex:
            print(ex)

    def get_text_async(self,titles):
        print("Get text async started - {}".format(titles[1]))
        engine = wikipediaapi.Wikipedia(self.language)
        curr_thread_text = ""
        not_valid = 0

        for title in titles[0]:
            try:
                curr_thread_text = self.split_text(self.destLangEngine.page(title).text)
            except Exception as ex:
                not_valid+=1
        with self._lock:
            print("Wrinitng into all text - {}".format(titles[1]))
            self.all_text+=curr_thread_text

        print("Get text async finished - {}".format(titles[1]))

    def aprove_finish(self):
        self.is_processing = False
        self.enough_text = self.check_is_limit(self.all_text, self.count, self.is_char)

    def build_url(self, title):
        url = "https://en.wikipedia.org/w/api.php?action=query&format=json"
        url+="&titles=" + title
        url+="&prop=langlinks"
        url+="&lllang=" + self.language
        return url

    def process_titles(self, title_batch):
        print("Title batch start - {}".format(title_batch[1]))
        titles = set()
        for title in title_batch[0]:
            json = self.get_response(self.build_url(title))
            pages = json["query"]["pages"]
            for page_id in pages:
                if "title" in pages[page_id]:
                    titles.add(pages[page_id]["title"])
                    continue

                if "langlinks" in pages[page_id] and len(pages[page_id]["langlinks"]) != 0:
                    titles.add(pages[page_id]["langlinks"][0]["*"])

                
        print("Title batch finished - {}".format(title_batch[1]))
        return titles
        #with self._lock:
        #    self.titles.union(titles)

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
