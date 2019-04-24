## deepchar - data access

Tools for downloading target language corpora - monolingual text.

### To download a dataset

First install package dependencies:

```
pip install -r requirements.txt
```

In case of running from cmd need to specify 5 arguments mentioned behind.
Only first two arguments are required. You may not fill last two if you don't need more data or don't want to consider count as number of rows.

#### Arguments

| Argument name  | Type         | Description                                                                                               | Default | CLI args names  |
| :------------- | :----------: | :--------------------------------------------------------------------------------------------------------:|:-------:|----------------:|
| Language       | String       | Key of language                                                                                           |         |      -l         |
| Path           | String       | Destination file where need to save                                                                       |         |      -f         |
| Count          | Int          | Total cout of data                                                                                        | 1000000 |      -c         |
| Is_char        | Bool         | If set to true, the count parameter shows the number of characters, otherwise count is the number of rows.| True    |      -ch        |

**Note:** Row length is 100

Example:
```
python wikiclient.py -l hy -f hy-Armn.txt 
```
Or
```
python wikiclient.py -l hy -f hy-Armn.txt -c 100000 -ch False
```

In case of using from python file need to
1. Import wikiclient.py file
2. Initialize WikiClient(language)
3. Call extract_text(path, is_char = True, count = 1000000): 

### To download a dataset with MultiLanguageTranslitGenerator.py (Need to test!!!)

First install package dependencies:

```
pip install -r requirements.txt
```

In case of running from cmd need to specify 7 arguments mentioned behind.
Only first two arguments are required. You may not fill last two if you don't need more data or don't want to consider count as number of rows.

#### Arguments

| Argument name  | Type         | Description                                                                                               | Default | CLI args names  |
| :------------- | :----------: | :--------------------------------------------------------------------------------------------------------:|:-------:|----------------:|
| Languages      | String       | Keys of languages. Need to sepearate language's keys with comma ","                                       |         |      -languages |
| Source path    | String       | As a result you will recevie two files. Source(where stores text with proper alpahbets) and translits.    |         |      -file      |
| Translit path  | String       | File path where will store text with mapping from one system of writing into another                      |         |      -translit  |
| Mappings path  | String       | Directory path where places mappings with JSON format.Each language's mapping file name need to be corresponding ISO 639-1 or 639-2 language name                     |         |      -mappings  | 
| Proportion     | String       | For each language text count proportion based on Count. Note: Order should be a same as for -Languages    | Languages/Count |      -proportion |
| Count          | Int          | Total cout of data                                                                                        | 1000000 |      -count     |
| Is_char        | Bool         | If set to true, the count parameter shows the number of characters, otherwise count is the number of rows.| True    |      -character |

**Note:** Row length is 100

**Example**
```
python MultiLanguageTranslitGenerator.py -languages en,ru,fr,hy -file path -translit path -mappings dir_path -proportion 400000,200000,200000,200000 
```

```
python MultiLanguageTranslitGenerator.py -languages en,ru,fr,hy -file path -translit path -mappings dir_path  
```

### Language code

You should used the ISO 639-1 or 639-2 language code used in *WP Code* column of the [list of Wikipedias][1].

For your own files we also suggest you use the ISO 15924 script codes to distinguish, for example, canonical Russian (`ru-Cyrl`) from translit Russian (`ru-Latn`).

[1]:https://en.wikipedia.org/wiki/List_of_Wikipedias#List




