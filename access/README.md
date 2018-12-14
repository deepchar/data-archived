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
python wikiclient.py hy C:\Users\Desktop\monolingual.txt 
```
Or
```
python wikiclient.py hy C:\Users\Desktop\monolingual.txt 100000 False
```

In case of using from python file need to
1. Import wikiclient.py file
2. Initialize WikiClient(language)
3. Call extract_text(path, is_char = True, count = 1000000): 

### Keys of languages

You can take language key [from Wikipedia][1], exactly from Wiki column.

[1]:https://en.wikipedia.org/wiki/List_of_Wikipedias#Detailed_list




