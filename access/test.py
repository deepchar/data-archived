pat = '/home/user/data/raw/translit_text.txt'

for line in open(pat,'r').readlines():
    if len(line)==0:
        print("kashmar")
