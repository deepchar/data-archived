import os
import argparse

from utils import *
from char_level import CharLevel
from translit_generator import Translit
from connectors.wikiclient import WikiClient

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path",      help="Yaml configuration file path")
    return parser.parse_args()

def main():
    args = parse_arguments()

    #Get mappings and validate yaml file
    mappings = get_mappings_dict()
    sucsess, lang_pairs_list = validate_parse_yaml(args.config_path, mappings)

    #If sucseed go ahead
    if not sucsess:
        return 0
    
    #Create output directory
    if not os.path.exists(lang_pairs_list["output_folder"]):
        os.mkdir(lang_pairs_list["output_folder"])
    
    #Iterate over all language pairs
    for lang_pairs in lang_pairs_list["pairs"]: 
        for target_lang in lang_pairs["target_langs"]:

            wiki_client = WikiClient(lang_pairs["source_lang"])
            translit_generator = Translit(lang_pairs["source_lang"], target_lang)

            #Create language direcetory
            language_pair_dir = os.path.join(lang_pairs_list["output_folder"],lang_pairs["source_lang"] + "-" + target_lang)
            if not os.path.exists(language_pair_dir):
                os.mkdir(language_pair_dir)

            #Paths
            destination_corpus_path = os.path.join(language_pair_dir, "raw_text.txt")
            source_translit_corpus_path = os.path.join(language_pair_dir, "raw_text_translit.txt")

            #Character level paths
            destination_character_corpus_path = os.path.join(language_pair_dir, "char-translit_destination.txt")
            source_character_corpus_path = os.path.join(language_pair_dir, "char-translit_source.txt")

            is_char = lang_pairs["char"] if "char" in lang_pairs else False

            count = lang_pairs["count"] if "count" in lang_pairs else 100000
            row_length = lang_pairs["rows_len"] if "rows_len" in lang_pairs else 100

            #Download text
            wiki_client.download_corpus(destination_corpus_path, is_char, count, row_length)
        
            #If necessary generate translit
            if "translit" in lang_pairs and lang_pairs["translit"]:
                translit_generator.translit(destination_corpus_path, source_translit_corpus_path)
        
            #If necessary generate chracter level
            if "char_level" in lang_pairs and lang_pairs["char_level"]:
                char_level = CharLevel()
                #Convert to character level destination corpus
                char_level.split_to_char(destination_corpus_path, destination_character_corpus_path)
                #Convert to character level translits corpus
                char_level.split_to_char(source_translit_corpus_path, source_character_corpus_path)
if __name__ == "__main__":
    main()


