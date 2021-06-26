## deepchar - Data extraction and translit generation

Prupose of repository is provide tool to download distinct articles from wikipedia with additional flexible functionality: convert extracted text into character level representation or/and generate transliteration.

# Table of Contents
 - [Requirements](#requirements)
 - [Arguments](#arguments)
 - [Language codes](#lang-code)
 - [How to add a new language pairs for translit generation](#new-lang)

### Requirements <a name="requirements"></a>

Install package dependencies:

```
pip install -r requirements.txt
```
### Arguments <a name="arguments"></a>
You have flexibility to :
 - Download only wikipedia articles for any language
 - Download wikipedia articles for any language + convert to character level
 - Download wikipedia articles for any language + convert to character level + transliteration 

Script splits text into rows by keeping context( add some words from end of previous row, to the front of current row ). You will have flexibility to download text as based on total count of rows as based on total counts of characters. Here is listed all arguments:

```
parser.add_argument("source_lang",      help="Source language")
parser.add_argument("target_lang",      help="Target language")
parser.add_argument("output_folder",    help="Output folder")
parser.add_argument("generate_translit",help="Generate transliteration", type=bool)
parser.add_argument("character_level",  help="Convert to character level", type=bool)
parser.add_argument("--row_length",     help="Count of characters in one row", type=int, default = 100)
parser.add_argument("--count",          help="Total count of characters or rows", type=int, default = 100000)
parser.add_argument("--is_char",        help="Consider count as total count of characters", type=bool, default = False)
```

Example:
Following example will:
 - Download wikipedia articles in Russian
 - Convert to caracter level
 - Generate transliteration 
 - Each row length will be 100 chars
 - Last argument False means, will collect 100000 rows
```
python main.py ru en data True True  100 100000  False
```
Another example:
- Download wikipedia articles in Armenian
- Convert to caracter level
- Generate transliteration 
- Each row length will be 100 chars
- Download in total 100000 characters 
```
python main.py hy en data True True  100 100000  True
```

### Language codes <a name="lang-code"></a>

You should used the ISO 639-1 or 639-2 language code used in *WP Code* column of the [list](https://en.wikipedia.org/wiki/List_of_Wikipedias#List) of Wikipedias 

### How to add a new language pairs for translit generation <a name="new-lang"></a>
For generating transliaterations for language, which we do not support, you have to create mapping file, which have to have json format. Keys must be source language alphabets and values list of potential characters from target language.<br/>
Here is example for russian -> english:

```
{
 "А": ["A"],
    "Б": ["B"],
    "В": ["V", "W"],
    "Г": ["G"],
    "Д": ["D"],
    "Е": ["E", "YE", "Ye"],
    "Ё": ["YO","Yo", "E", "IO", "Io", "JO", "Jo"]
}
```
After creating mapping file, move it into following [directory](./resources/mappings) and run main.py.<br/>
**Note:** We will appreciate if you will share your created mappings with us. 




