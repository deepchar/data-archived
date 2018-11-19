import json
import requests
import wikipediaapi

class WikiClient(object):

    #Initializer
    def __init__(self , language):
        #We get all english pages,after it try to find languge referenses
        if(self.validate_language(language))
            self.language = language
            self.englishEngine = wikipediaapi.Wikipedia('eng')
            self.destLangEngine = wikipediaapi.Wikipedia(language)
        else:
            raise ValueError("Specified key for language doesn't support")

    #Get JSON response of request
    def get_response(self, url):
        resp = requests.get(url = url)
        return resp.json()

    def validate_language(key):
        with open('./Language.json',) as file:
            languages = json.load(file)
            return languages.has_key(key)

    #Parses titles JSON to list of titles 
    def parse_json(self, titles_jsons):
        titles = []
        for current_Json in titles_jsons:
            titles.append(current_Json["title"])
        return titles

    #Returns batch of titles            
    def get_batches(self):
        url = 'https://en.wikipedia.org/w/api.php?action=query&list=allpages&format=json&aplimit=500'
        json_resp = self.get_response(url)
        next_batch = json_resp["continue"]["apcontinue"]

        yield self.parse_json(json_resp["allpages"])

        url = url + '&apcontinue='+ next_batch
        while(True):
            json_resp = self.get_response(url)
            yield self.parse_json(json_resp)

            #batches are over
            if "continue" not in json_resp:
                return []

            url = url.replace( next_batch , json_resp["continue"]["apcontinue"])
            next_batch = json_resp["continue"]["apcontinue"]

    #Returns possition of starting split from
    def get_pos(self, curr_pos , text):
        if curr_pos == 0:
            return curr_pos

        while(text[curr_pos - 20]!= " "):
            curr_pos-=1
        return curr_pos - 20

    #Splits text to rows
    def split_text(self,text):
        result = ""
        curr_pos = 0
        line_length = 100
        length = len(text)

        while(curr_pos < length):
            end = curr_pos + line_length
            start_pos = self.get_pos(curr_pos,text)

            if end < length:
                if  text[end] != " ":
                    while(text[end] != " " and end != length):
                        end+=1
            else:
                if curr_pos == 0 :
                    return text 
                else:
                    end = start_pos + end - length
                    
            result = result + text[start_pos : end] + '\n'
            curr_pos += end - curr_pos

    #path-Destination folder where need to write text
    def extract_text(self,path, is_char = True, count = 1000000):
        
        with open(path,'w') as file:
            #Wikipedia return title's batches. Each one contains 500 titles
            for titles_batch in self.get_batches():
                for title in titles_batch:
                    page = self.englishEngine.page(title)
                    #Tryes find same page in required langage
                    if self.language in page.langlinks:
                        destTitle = page.langlinks[self.language].title
                        text = self.split_text(self.destLangEngine.page(destTitle))
                        file.write(text)

                        count -= len(text) if is_char else text.count('\n')
                        
                        del text
                        if count <= 0:
                            file.close()
                            return




    


            



    
