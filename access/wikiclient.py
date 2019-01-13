import os
import json
import argparse
import requests
import wikipediaapi


class WikiClient(object):

    # Initializer
    def __init__(self, language):
        # We get all english pages,after it try to find languge references
        if self.validate_language(language):
            self.language = language
            self.englishEngine = wikipediaapi.Wikipedia('en')
            self.destLangEngine = wikipediaapi.Wikipedia(language)
        else:
            raise ValueError("Specified key for language doesn't support")

    def check_is_limit(self, text, count, is_char=True):
        rows = text.split("\n")
        res_rows = 0
        char_count = 0

        for row in rows:
            curr_len = len(row)
            if (curr_len >= 99):
                char_count += curr_len
                res_rows += 1

        res_count = char_count if is_char else res_rows
        is_limit = res_count >= count
        return abs(res_count - count), is_limit

    # Get JSON response of request
    def get_response(self, url):
        resp = requests.get(url=url)
        return resp.json()

    def validate_language(self, key):
        lang_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), "languages.json")
        with open(lang_path, "r") as file:
            languages = json.load(file)
            return key in languages

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

    # Returns possition of starting split from
    def get_pos(self, curr_pos, text):
        if curr_pos == 0:
            return curr_pos

        while (text[curr_pos - 20] != " "):
            curr_pos -= 1
        return curr_pos - 20

    # Splits text to rows
    def split_text(self, text):
        result = ""
        curr_pos = 0
        line_length = 100
        length = len(text)

        while (curr_pos < length):
            end = curr_pos + line_length
            start_pos = self.get_pos(curr_pos, text)

            if end < length:
                if text[end] != " ":
                    while (text[end] != " " and end != length):
                        end += 1
            else:
                if curr_pos == 0:
                    return text
                else:
                    end = length - 1

            result = result + text[start_pos: end].replace('\n', "") + '\n'

            if (end == length - 1):
                break
            curr_pos += end - curr_pos
        return result

    # path - Destination folder where need to write text
    def extract_text(self, path, is_char=True, count=1000000):
        print(count)
        with open(path, 'wb') as file:
            not_valid_pages = 0
            all_text = ""
            temp_count = count
            # Wikipedia return title's batches. Each one contains 500 titles
            for titles_batch in self.get_batches():
                for title in titles_batch:
                    page = self.englishEngine.page(title)
                    # Tries to find the same page in the target langage
                    try:
                        if self.language in page.langlinks:
                            destTitle = page.langlinks[self.language].title
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
