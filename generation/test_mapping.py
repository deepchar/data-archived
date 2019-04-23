import random
import codecs

alphabet = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split(" ")
arm_alphabet = "Ա Բ Ց Դ Ե Ֆ Գ Հ Ի Ջ Կ Լ Մ Ն Ո Պ Ք Ր Ս Տ ՈՒ Վ Ւ Խ Յ Զ".split(" ")

print(arm_alphabet, alphabet)

#number = range(len(alphabet))


mappings = zip(alphabet, arm_alphabet)
dictionary = dict(mappings)

res = ""

for index in range(1000):
    curr = ""
    for i in range(100):
        curr += random.choice(alphabet ) + " "
    res += curr + "\n"

res1 = ""

for row in res:
    for char in row:
        if char in dictionary:
            res1 += str(dictionary[char])
        else:
            res1 += char

with codecs.open('../raw/test/source.txt', 'w', encoding="utf-8") as file:
    file.write(res)

with codecs.open('../raw/test/target.txt', 'w', encoding="utf-8") as file:
    file.write(res1)