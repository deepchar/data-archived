
## deepchar - Data extraction and translit generation

Purpose of repository is provide tool to download distinct articles from wikipedia, with additional flexible functionality: convert extracted text into character level representation or/and generate transliteration.

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

Script splits text into rows by keeping context( add some words from end of previous row, to the front of current row ). You will have flexibility to download text as based on total count of rows as based on total counts of characters.

Following example
```
python main.py --config_path=data.yaml
``` 
will do following based on yaml configuration file:
 - Download wikipedia articles in Russian and Armenian
 - Convert to caracter level for both languages (you can set **False** to not convert to character level)
 - Generates transliteration from **source_lang** corpus to **target_langs** (you can set to **False** to not generate transilterations). 
 - For Armenian each row will have 150 chars and for Russian 100 chars.
 - For Armenian **count** means count of total rows, **count** for Russian means count of total characters to download. To switch from count of rows to count of characters you have to use **char: True**


```
output_folder: "......"
pairs:
  -
    source_lang: "hy"
    target_langs:
      - "en"
      - "ru"
    char_level: True
    translit: True
    rows_len: 150
    count: 5000
  -
    source_lang: "ru"
    target_langs:
      - "en"
    char_level: True
    translit: True
    rows_len: 100
    count: 15000
    char: True
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
