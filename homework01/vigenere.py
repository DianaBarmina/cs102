def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    encryption = ""
    i = 0
    for cip in plaintext:  # cip - буква из кодируемого слова
        if cip.isupper():
            key = keyword[i]
            keys = ord(key) - ord("A")
            cip_index = ord(cip) - ord("A")
            new_unicode = cip_index + keys
            new_character = chr(new_unicode % 26 + ord("A"))
            encryption += new_character
            if len(keyword) == 1:
                i = i + 1
            else:
                if i == len(keyword) - 1:
                    i = 0
                else:
                    i += 1

        elif cip.islower():
            key = keyword[i]
            keys = ord(key) - ord("a")
            cip_index1 = ord(cip) - ord("a")
            new_unicode1 = cip_index1 + keys
            new_character1 = chr(new_unicode1 % 26 + ord("a"))
            encryption += new_character1
            if len(keyword) == 1:
                i = i
            else:
                if i == len(keyword) - 1:
                    i = 0
                else:
                    i += 1
        else:
            encryption += cip

    return encryption


def descrypt_vigenere(ciphertext: str, keyword: str) -> str:
    dencryption = ""
    i = 0
    for cip in ciphertext:  # cip - буква из раскодируемого слова
        if cip.isupper():
            key = keyword[i]
            keys = ord(key) - ord("A")
            cip_index = ord(cip) - ord("A")
            old_unicode = (cip_index - keys) % 26 + ord("A")
            old_character = chr(old_unicode)
            dencryption += old_character
            if len(keyword) == 1:
                i = i + 1
            else:
                if i == len(keyword) - 1:
                    i = 0
                else:
                    i += 1
        elif cip.islower():
            key = keyword[i]
            keys = ord(key) - ord("a")
            cip_index1 = ord(cip) - ord("a")
            old_unicode1 = cip_index1 - keys
            old_character1 = chr(old_unicode1 % 26 + ord("a"))
            dencryption += old_character1
            if len(keyword) == 1:
                i = i
            else:
                if i == len(keyword) - 1:
                    i = 0
                else:
                    i += 1
        else:
            dencryption += cip

    return dencryption


if __name__ == "__main__":
    print(encrypt_vigenere("attackatdawn", "lemon"))
    print(descrypt_vigenere("lxfopvefrnhr", "lemon"))
