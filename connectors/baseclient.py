import os
import json
from pathlib import Path

class BaseClient(object):
    #Validate language code
    def validate_language(self, key):
        curren_path = Path(os.path.dirname(os.path.abspath((__file__))))
        resources =  os.path.join( curren_path.parent.absolute(),"resources")
        lang_path = os.path.join(resources, "languages.json")
        with open(lang_path, "r") as file:
            languages = json.load(file)
            return key in languages

    # Returns start possition 
    def get_pos(self, curr_pos, text):
        if curr_pos == 0:
            return curr_pos

        curr_pos -= 20
        #While we have not meet new word
        while (curr_pos != 0 and text[curr_pos] != " "):
            curr_pos -= 1
        return curr_pos

    # Splits text to rows
    def split_text(self, text, row_length):
        text_rows = []
        curr_pos = 0
        length = len(text) - 1

        #Split text into rows (keeping some words between neigbour rows) 
        while (curr_pos < length):
            #Start and end positions
            end = curr_pos + row_length
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

            #Slice row from text
            text_rows.extend([text[start_pos: end].replace('\n', "") + '\n'])

            if (end == length - 1):
                break
            curr_pos += end - curr_pos
        return text_rows

    def check_is_limit(self, text_rows, count, is_char, row_length):
        res_rows = 0
        char_count = 0

        for text_row in text_rows:
            curr_len = len(text_row)
            if curr_len >= row_length - 1:
                char_count += curr_len
                res_rows += 1

        res_count = char_count if is_char else res_rows
        is_limit = res_count >= count
        return abs(res_count - count), is_limit



