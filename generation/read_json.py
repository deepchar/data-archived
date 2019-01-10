import json

file = input('Enter a filename')
path = '\\mappings' + file
with open(path) as m:
	mapping = json.load(m)