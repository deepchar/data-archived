import os
import json
import yaml
import codecs
from pathlib import Path

def get_mapping_dir():
    #Get mapping directory
    working_dir = Path(os.path.dirname(os.path.abspath((__file__))))
    mapping_dir =  os.path.join( working_dir.absolute(),"resources","mappings")
    return mapping_dir

def get_mapping(source_language, target_language):
    #Get mappings dir
    mapping_dir = get_mapping_dir()
    #Get mapping file
    mapping_file = os.path.join(mapping_dir, source_language + "-" + target_language) + ".json"
    with codecs.open(mapping_file, encoding="utf-8-sig") as m:
        mapping = json.load(m)
    return mapping

#Read existing mapping files
def get_mappings_dict():
    #Get mappings dir
    mapping_dir = get_mapping_dir()
    mappings = dict()

    #Get existing language mapping
    for mapping in os.listdir(mapping_dir):
        if "-" not in mapping:
            continue
        src_lang, dst_lang = mapping.split(".")[0].split("-")

        if src_lang not in mappings:
            mappings[src_lang] = set()

        if dst_lang not in mappings[src_lang]:
            mappings[src_lang].add(dst_lang)
    return mappings

def validate_parse_yaml(yaml_path, mappings):
    with open(yaml_path) as f:
        lang_pairs_list = list(yaml.load_all(f, Loader=yaml.FullLoader))[0]
    if "output_folder" not in lang_pairs_list:
        print("Missing output folder path")
        return False, lang_pairs_list

    for lang_pairs in lang_pairs_list["pairs"]:
        if "source_lang" not in lang_pairs or "target_langs" not in lang_pairs:
            return False, lang_pairs_list
        
        if lang_pairs["source_lang"] not in mappings:
            print("There is no mapping for source language {}".format(lang_pairs["source_lang"]))
            return False, lang_pairs_list
        
        for target_lang in lang_pairs["target_langs"]:
            if target_lang not in mappings[lang_pairs["source_lang"]]:
                print("There is no mapping for  {} - {} languages".format(lang_pairs["source_lang"],target_lang))
                return False, lang_pairs_list
    return True, lang_pairs_list

class Args(object):
    def __init__(self, config_path, source_lang, target_lang, out_folder, generate_translit, char_level, row_length, count, is_char):
        self.config_path = config_path
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.output_folder = out_folder 
        self.generate_translit = generate_translit
        self.character_level= char_level
        self.row_length = row_length
        self.count = count
        self.is_char = is_char

