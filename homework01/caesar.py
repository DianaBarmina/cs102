def encrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    encryption = ""
    for cip in ciphertext:  # cip - буква из кодируемого слова
        if cip.isupper():
            cip_unicode = ord(cip)
            cip_index = ord(cip) - ord("A")
            new_index = (cip_index + shift) % 26
            new_unicode = new_index + ord("A")
            new_character = chr(new_unicode)
            encryption += new_character
        elif cip.islower():
            cip_unicode = ord(cip)
            cip_index = ord(cip) - ord("a")
            new_index = (cip_index + shift) % 26
            new_unicode = new_index + ord("a")
            new_character = chr(new_unicode)
            encryption += new_character
        else:
            encryption += cip

    return encryption


def decrypt_caesar(plaintext: str, shift: int = 3) -> str:
    dencryption = ""
    for cip in plaintext:  # cip - буква из раскодируемого слова
        if cip.isupper():
            cip_index = ord(cip) - ord("A")
            old_unicode = (cip_index - shift) % 26 + ord("A")
            old_character = chr(old_unicode)
            dencryption += old_character
        elif cip.islower():
            cip_index1 = ord(cip) - ord("a")
            cip_pos = (cip_index1 - shift) % 26 + ord("a")
            old_character1 = chr(cip_pos)
            dencryption += old_character1
        else:
            dencryption += cip
    return dencryption


if __name__ == "__main__":
    print(encrypt_caesar("Python3.6", 3), decrypt_caesar("SBWKrq6.9", 3))
