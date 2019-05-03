import json
import codecs
import random
import argparse
import requests
import wikipediaapi

from os import listdir
from os.path import isfile, join


class TranslitGenerator(object):

    # Initializer
    def __init__(self, languages,mappings,proportions,count):
        not_valides, lang_keys = self.validate_languages(languages)
        if(len(not_valides) > 0):
            raise ValueError("Specified languages \n {} doesn't support".format(not_valides))

        not_valides = self.validate_mappings(mappings,lang_keys)
        if(len(not_valides) > 0):
            raise ValueError("Was not able to find mappings for \n {}".format(not_valides))

        if(proportions is not None and len(proportions.split(",")) != len(lang_keys)):
            raise ValueError("For each language need to specify proportion")
        
        self.proportions = dict(parse_proportions(proportions,count))
        self.languages = lang_keys
        self.wikiEngines = dict()
        for key in self.languages :
            self.wikiEngines[key] = wikipediaapi.Wikipedia(key)
        self.englishEngine = wikipediaapi.Wikipedia('en')

	#Validates languages 
    def validate_languages(self, languages):
		#Parse lang keys
        lang_keys = languages.split(",") if languages.contains(",") else [languages]
        lang_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), "languages.json")
        not_valides = []
        with open(lang_path, "r") as file:
            languages = json.load(file)
            for key in lang_keys:
                if(key not in languages):
                    not_valides.append(key)
        return not_valides,lang_keys

	#Parses proportions
	def parse_proportions(self,proportions,count):
		proportions_int = []
		if(proportions is None):
			proportions_int = [count//len(self.languages) for i in range(len(self.languages))]
		else:
		    proportions_int = [int(prop) for prop in proportions.split(",")]
		return zip(self.languages,proportions_int)

	#Validate and load mappings
    def validate_mappings(mappings,lang_keys):
        not_valides = []
        onlyfiles = [f for f in listdir(mappings) if isfile(join(mappings, f))]
        for key in lang_keys:
            if(key not in onlyfiles):
                not_valides.append(key)
        if(len(not_valides) == 0):
            self.mappings = dict()
            for key in lang_keys:
                curr_path = join(mappings, key + ".json")
                with open(curr_path,"r") as file:
                    self.mappings[key] = json.load(file)

        return not_valides

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

	#Cheks is limit
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

    #Generate translits
    def generate_translit(self,text, lang_key):
        result = ''
        for line in text.split("\n"):
            for char in line:
                if char in self.mappings[lang_key]:
                    result += random.choice(self.mappings[lang_key][char])
                else:
                    result += char
        return result

        

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
    
    # Splits text to rows
    def split_text(self, text):
        result = ""
        curr_pos = 0
        line_length = 100
        length = len(text) - 1

        while (curr_pos < length):
            end = curr_pos + line_length
            start_pos = self.get_pos(curr_pos, text)

            if end < length:
                if text[end] != " ":
                    while ( end != length and text[end] != " "):
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
    def extract_text(self, path, translit_path,  is_char=True, count=1000000):
        print(count)
		all_text = ""
		all_text_translit = ""
		with open(translit_path,"wb") as translit_file:
            with open(path, 'wb') as file:
                not_valid_pages = 0
            
			    next_lang = False
                for lang_key in self.languages:
				    prev = ""
				
				    curr_prop = self.proportions[lang_key]

                    # Wikipedia return title's batches. Each one contains 500 titles
                    for titles_batch in self.get_batches():
                        for title in titles_batch:
                            page = self.englishEngine.page(title)
                            # Tries to find the same page in the target langage
                            try:
                                if lang_key in page.langlinks:
                                    destTitle = page.langlinks[lang_key].title
                                    if prev == destTitle:
                                       continue
                                    prev = destTitle
                                    text = self.split_text(self.wikiEngines[lang_key].page(destTitle).text)
							        text_tanslit = selg.split_text(self.generate_translit(text,lang_key))

                                    all_text += text
							        all_text_translit += text_tanslit

                                    file.write(text.encode('utf-8'))
									translit_file.write(text_tanslit.encode("utf-8"))
                                    curr_prop -= len(text) if is_char else text.count('\n')
                                    del text
                                    if curr_prop <= 0:
                                       res_count, is_limit = self.check_is_limit(all_text, self.proportions[lang_key], is_char)
                                       if (not is_limit):
                                           curr_prop = res_count
                                           continue
								       next_lang = True
								       break
                            except Exception as ex:
                                not_valid_pages += 1
					    if(next_lang):
						    next_lang = False
						    break



def main(args):
    try:
        is_char = True
        count = 1000000

        if (args.character is not None):
            is_char = args.character
        if (args.count is not None):
            count = int(args.count)

		client = TranslitGenerator(args.languages,args.mappings,args.proportion,count)
        client.extract_text(args.file, args.translit ,is_char, count)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-file", required=True)#Downlaoded text file path
	parser.add_argument("-translit",required = True)#Generated Translit file path
    parser.add_argument("-mappings", required=True)#path where stores mappings,should be corresponding to ISO standard
    parser.add_argument("-proportion",required=False)#proportion per cout for each language .Deff count/languages count
    parser.add_argument("-languages", required=True)#Will be seperate with ','
    parser.add_argument("-character", type=bool, required=False)#character level
    parser.add_argument("-count", required=False)#count

    args = parser.parse_args()

    main(args)
    print("Source for translitaerations saved in {} \n Translits saved in {}".format(args.file,args.translit))
