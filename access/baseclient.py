import os
import json

class BaseClient(object):
    def validate_language(self, key):
        lang_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), "languages.json")
        with open(lang_path, "r") as file:
            languages = json.load(file)
            contains = key in languages
            del languages
            return contains


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



