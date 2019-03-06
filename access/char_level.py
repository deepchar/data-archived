
path = '/home/user/data/raw/wiki_raw.txt'
path1 = '/home/user/sockeye/raw/wiki_raw.txt'
lines = None
with open(path,"r", encoding='utf-8') as file:
    lines = file.readlines()

destLines = []

for index_line in range(0, len(lines)):
    words = lines[index_line].strip().split()
    destLine = ""

    for index_word in range(0, len(words)):
        word = words[index_word]
        destWord = ""

        for index_char in range(0, len(word)):
            char = word[index_char]
            destWord = destWord + char

            if(index_char != len(word) - 1):
                destWord = destWord + " "

        destLine = destLine + destWord

        if( index_word != len(words) - 1):
            destLine = destLine + " _ "
    destLine= destLine +'\n'
    destLines.append(destLine)
    print(destLine)
print(len(lines))
print(len(destLines))
with open( path1,"w",encoding='utf-8') as file:
    file.writelines(destLines)
