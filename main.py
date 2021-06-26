import os
import argparse

from utils import *
from char_level import CharLevel
from translit_generator import Translit
from connectors.wikiclient import WikiClient

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_lang",      help="Source language")
    parser.add_argument("target_lang",      help="Target language")
    parser.add_argument("output_folder",    help="Output folder")
    parser.add_argument("generate_translit",help="Generate transliteration", type=bool)
    parser.add_argument("character_level",  help="Convert to character level", type=bool)
    parser.add_argument("--row_length",     help="Count of characters in one row", type=int, default = 100)
    parser.add_argument("--count",          help="Total count of characters or rows", type=int, default = 100000)
    parser.add_argument("--is_char",        help="Consider count as total count of characters", type=bool, default = False)
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    #args = Args("hy","en","C:\\Users\\grigor.vardanyan\\Desktop\\ML projects\\data",True,True,100,10000,False)
    
    wiki_client = WikiClient(args.source_lang)
    translit_generator = Translit(args.source_lang, args.target_lang)
    mappings = get_mappings_dict()

    if (args.source_lang not in mappings) or (args.target_lang not in mappings[args.source_lang]):
        print("There are no mapping file for pairs of language {0} - {1}.".format(args.source_lang, args.target_lang))
    else:  
        if not os.path.exists(args.output_folder):
            os.mkdir(args.output_folder)
        
        #Paths
        destination_corpus_path = os.path.join(args.output_folder, "raw_text.txt")
        source_translit_corpus_path = os.path.join(args.output_folder, "raw_text_translit.txt")

        #Character level paths
        destination_character_corpus_path = os.path.join(args.output_folder, "char-translit_destination.txt")
        source_character_corpus_path = os.path.join(args.output_folder, "char-translit_source.txt")

        #Download text
        wiki_client.download_corpus(destination_corpus_path, args.is_char, args.count, args.row_length)
        
        #If necessary generate translit
        if args.generate_translit:
            translit_generator.translit(destination_corpus_path, source_translit_corpus_path)
        
        #If necessary generate chracter level
        if args.character_level:
            char_level = CharLevel()
            #Convert to character level destination corpus
            char_level.split_to_char(destination_corpus_path, destination_character_corpus_path)
            #Convert to character level translits corpus
            char_level.split_to_char(source_translit_corpus_path, source_character_corpus_path)

if __name__ == "__main__":
    main()


