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

| Argument name  | Type         | Description                                                                                               | Default |
| :------------- | :----------: | :--------------------------------------------------------------------------------------------------------:|--------:|
| Language       | String       | Key of language                                                                                           |         |
| Path           | String       | Destination file where need to save                                                                       |         |
| Count          | Int          | Total cout of data                                                                                        | 1000000 |
| Is_char        | Bool         | If set to true, the count parameter shows the number of characters, otherwise count is the number of rows.| True    |

**Note:** Row length is 100

Example:
```
python wikiclient.py hy hy-Armn.txt 
```
Or
```
python wikiclient.py hy hy-Armn.txt 100000 False
```

In case of using from python file need to
1. Import wikiclient.py file
2. Initialize WikiClient(language)
3. Call extract_text(path, is_char = True, count = 1000000): 

### Language code

You should used the ISO 639-1 or 639-2 language code used in *WP Code* column of the [list of Wikipedias][1].

For your own files we also suggest you use the ISO 15924 script codes to distinguish, for example, canonical Russian (`ru-Cyrl`) from translit Russian (`ru-Latn`).

[1]:https://en.wikipedia.org/wiki/List_of_Wikipedias#List




