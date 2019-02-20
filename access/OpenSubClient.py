import os
import re
import zlib
import time
import gzip
import random
import base64
import xmlrpc.client
from baseclient import BaseClient


class OpenSubClient(BaseClient):
    def __init__(self,login,password, language,user_agent):
        if(self.validate_language(language)):
            self.language = language
            self.server_url = "https://api.opensubtitles.org/xml-rpc"
            self.server = xmlrpc.client.ServerProxy(self.server_url)
            response = self.server.LogIn(login,password,language,user_agent)

            if(response["status"]!="200 OK"):
                raise Exception("Invalid Params")
            #Get token for feauture requests
            self.token = response["token"]

    def get_next_id(self):
        #Get compressed file
        imdb_ids = os.path.join(os.path.dirname(os.path.abspath((__file__))),"subtitles", self.language + ".txt.gz")
        lines = []

        with gzip.open(imdb_ids,"rb") as f:
            lines = f.read().decode("utf-8").split("\r")
        #Each compressed file has lines where octets separated by \t and first one is IMDB ID
        for line in lines:
            yield line.split("\t")[0]
        

    #Parses subtitle to clean text 
    def parse_text(self,text):
        result = ""
        pattern = "\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+"
        reg_obj = re.compile(pattern)
        temp = []
        for row in text.split("\r\n")[1:]:
            if( not row.isdigit() and reg_obj.match(row) == None and len(row) > 1 ):
                result+= row
                temp.append(row)
        return self.split_text(result)

    def extract_text(self, path, is_char=True, count=1000000):
         with open(path, 'wb') as file:
            i = 0
            not_valid_pages = 0
            all_text = ""
            temp_count = count

            for id in self.get_next_id():
                content = [{ 'imdbid':id,'sublanguageid':self.language}]
                response = None 

                try:
                    response = self.server.SearchSubtitles(self.token,content)
                except Exception as ex:
                    if(ex.errcode!= None and ex.errcode == 429):
                        #Wait for 10 seconds as there is limite 40 HTTP request per 10 seconds
                        time.sleep(10)
                        response = self.server.SearchSubtitles(self.token,content)
                
                if (response != None and len(response["data"]) != 0 ):
                    for row in response["data"]:
                        if(row["ISO639"] == self.language):
                            download_response = None

                            try:
                                download_response = self.server.DownloadSubtitles(self.token,[row["IDSubtitleFile"]])
                            except Exception as ex:
                                time.sleep(10)
                                download_response = self.server.DownloadSubtitles(self.token,[row["IDSubtitleFile"]])

                            encoded_file = base64.standard_b64decode(download_response['data'][0]['data'])

                            try:
                                data = self.server.PreviewSubtitles(self.token,[row["IDSubtitleFile"]])
                                #Currently we support only UTF-7 format (There are differences between structures of text for each encodding)
                                if(data["data"][0]["encoding"] != "UTF-8"):
                                    continue

                                text = zlib.decompress(encoded_file, 47 )[3:].decode("utf-8")
                                #text = zlib.decompress(encoded_file, 47 ).decode(data["data"][0]["encoding"])
                                text = self.parse_text(text)

                                all_text+= text
                                file.write(text.encode('utf-8'))

                                temp_count -= len(text) if is_char else text.count('\n')
                    
                                del text

                            except Exception as ex:
                                print(ex)

                            if temp_count <= 0:
                                res_count, is_limit = self.check_is_limit(all_text, count, is_char)
                                if (not is_limit):
                                    temp_count = res_count
                                    continue

                                file.close()
                                return

                    










