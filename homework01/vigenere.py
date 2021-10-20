list1 = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]
list2 = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
text = "attackatdawn"
text1 = "lxfopvefrnhr"
shift = "lemon"


def vigenere_cipher(text, shift):

    encryption = ""
    i = 0
    for cip in text:
        if cip.isupper():
            key = shift[i]
            keys = list1.index(key)
            res = ord(cip) - ord("A")
            res1 = res + keys
            res2 = chr(res1 % 26 + ord("A"))
            encryption += res2
            if len(shift) == 1:
                i = i + 1
            else:
                if i == len(shift) - 1:
                    i = 0
                else:
                    i += 1

        elif cip.islower():
            key = shift[i]
            keys = list2.index(key)
            res3 = ord(cip) - ord("a")
            res4 = res3 + keys
            res5 = chr(res4 % 26 + ord("a"))
            encryption += res5
            if len(shift) == 1:
                i = i
            else:
                if i == len(shift) - 1:
                    i = 0
                else:
                    i += 1
        else:
            encryption += cip

    return encryption


def descrypt_vigenere(text1, shift):
    dencryption = ""
    i = 0
    for cip in text1:
        if cip.isupper():
            key = shift[i]
            keys = list1.index(key)
            res = ord(cip) - ord("A")
            res1 = (res - keys) % 26 + ord("A")
            res2 = chr(res1)
            dencryption += res2
            if len(shift) == 1:
                i = i + 1
            else:
                if i == len(shift) - 1:
                    i = 0
                else:
                    i += 1
        elif cip.islower():
            key = shift[i]
            keys = list2.index(key)
            res3 = ord(cip) - ord("a")
            res4 = res3 - keys
            res5 = chr(res4 % 26 + ord("a"))
            dencryption += res5
            if len(shift) == 1:
                i = i
            else:
                if i == len(shift) - 1:
                    i = 0
                else:
                    i += 1
        else:
            dencryption += cip

    return dencryption


print(vigenere_cipher(text, shift))
print(descrypt_vigenere(text1, shift))
