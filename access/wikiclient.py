import argparse
import requests
import wikipediaapi

from access.baseclient import BaseClient

class WikiClient(BaseClient):

    # Initializer
    def __init__(self, language):
        # We get all english pages,after it try to find language references
        if self.validate_language(language):
            self.language = language
            self.englishEngine = wikipediaapi.Wikipedia('en')
            self.destLangEngine = wikipediaapi.Wikipedia(language)
        else:
            raise ValueError("Specified key for language doesn't support")

    # Get JSON response of request
    def get_response(self, url):
        resp = requests.get(url=url)
        return resp.json()

    # Parses titles JSON to list of titles
    def parse_json(self, titles_jsons):
        titles = []
        for current_Json in titles_jsons:
            titles.append(current_Json["title"])
        return titles

    # Returns batch of titles
    def get_batches(self):
        url = 'https://en.wikipedia.org/w/api.php?action=query&list=allpages&format=json&aplimit=500'
        json_resp = self.get_response(url)
        next_batch = json_resp["continue"]["apcontinue"]

        yield self.parse_json(json_resp["query"]["allpages"])

        url = url + '&apcontinue=' + next_batch
        while (True):
            json_resp = self.get_response(url)
            yield self.parse_json(json_resp["query"]["allpages"])

            # Batches are over
            if "continue" not in json_resp:
                return []

            url = url.replace(next_batch, json_resp["continue"]["apcontinue"])
            next_batch = json_resp["continue"]["apcontinue"]

    # path - Destination folder where need to write text
    def extract_text(self, path, is_char=True, count=1000000):
        print(count)
        with open(path, 'wb') as file:
            not_valid_pages = 0
            all_text = ""
            temp_count = count
            prev= ""
            # Wikipedia return title's batches. Each one contains 500 titles
            for titles_batch in self.get_batches():
                for title in titles_batch:
                    page = self.englishEngine.page(title)
                    # Tries to find the same page in the target langage
                    try:
                        if self.language in page.langlinks:
                            destTitle = page.langlinks[self.language].title
                            if(prev == destTitle):
                                continue
                            prev = destTitle
                            text = self.split_text(self.destLangEngine.page(destTitle).text)
                            all_text += text
                            file.write(text.encode('utf-8'))
                            temp_count -= len(text) if is_char else text.count('\n')
                            del text
                            if temp_count <= 0:
                                res_count, is_limit = self.check_is_limit(all_text, count, is_char)
                                if (not is_limit):
                                    temp_count = res_count
                                    continue
                                file.close()
                                return
                    except Exception as ex:
                        not_valid_pages += 1



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


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", required=True)
    parser.add_argument("-l", required=True)
    parser.add_argument("-ch", type=bool, required=False)
    parser.add_argument("-c", required=False)

    args = parser.parse_args()

    main(args)
    print("Data was saved in" + args.f)
