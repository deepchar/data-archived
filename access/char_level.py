
path = '/home/user/data/access/hy-arm.txt'
path1 = '/home/user/sockeye/raw/translit_text.txt'
lines = None
with open(path,"r") as file:
    lines = file.readlines()

destLines = []

for index_line in range(0, len(lines)):
    words = lines[index_line].split()
    destLine = ""

    for index_word in range(0, len(words)):
        word = words[index_word]
        destWord = ""

        for index_char in range(0, len(word)):
            char = word[index_char]
            destWord = destWord + char

            if(index_char != len(word) - 1):
                destWord = destWord + " "

        dsestLine = destLine + destWord

        if( index_word != len(words) - 1):
            destLine = destLine + "_"
    destLines.append(destLine)

with open( path1,"w") as file:
    file.writelines(destLines)
