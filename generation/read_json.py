import json

from pprint import pprint


file = '../mappings/hy-Latn.json'
with open(file, encoding="utf-8") as m:
    mapping = json.load(m)

pprint(mapping)
# uncomment in case you want to print the mapping