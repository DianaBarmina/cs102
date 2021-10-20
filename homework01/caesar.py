import typing as tp

encryption = ""
dencryption = ""
shift = 3


def encrypt_caesar(shift, encryption):

    ciphertext = "Python3.6"

    for cip in ciphertext:
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


def decrypt_caesar(dencryption, shift):

    plaintext = "SBWKrq6.9"

    for cip in plaintext:
        if cip.isupper():
            cip_index = ord(cip) - ord("A")
            cip_pos = (cip_index - shift) % 26 + ord("A")
            cip_og = chr(cip_pos)
            dencryption += cip_og
        elif cip.islower():
            cip_index = ord(cip) - ord("a")
            cip_pos = (cip_index - shift) % 26 + ord("a")
            cip_og = chr(cip_pos)
            dencryption += cip_og
        else:
            dencryption += cip
    return dencryption


res = encrypt_caesar(shift, encryption)
res1 = decrypt_caesar(dencryption, shift)

print(res, res1)
