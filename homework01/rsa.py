import random
import typing as tp


def is_prime(num: int) -> bool:
    result = 0
    for i in range(2, num // 2 + 1):
        if num % i == 0:
            result += 1
    if result > 0 or num <= 0:
        return False
    else:
        return True


def gcd(num1: int, num2: int) -> int:
    while num1 != 0 and num2 != 0:
        if num1 >= num2:
            num1 %= num2
        else:
            num2 %= num1
    return num1 or num2


def multiplicative_inverse(num1, num2):
    copy_num2 = num2
    nod, nod_help = 1, 0
    while num2:
        chastnoe = num1 // num2
        num1, num2 = num2, num1 % num2
        nod, nod_help = nod_help, nod - nod_help * chastnoe

    nod = nod % copy_num2
    return nod


def generate_keypair(p: int, q: int) -> tp.Tuple[tp.Tuple[int, int], tp.Tuple[int, int]]:
    if not (is_prime(keynum1) == True and is_prime(keynum2) == True):
        raise ValueError("Both numbers must be prime.")
    elif keynum1 == keynum2:
        raise ValueError("keynum1 and keynum2 cannot be equal")
    else:
        proisved = keynum1 * keynum2
        eiler = (keynum1 - 1) * (keynum2 - 1)
        randomnum1 = random.randrange(1, eiler)
        gcd_num = gcd(randomnum1, eiler)
        while gcd_num != 1:
            randomnum2 = random.randrange(1, eiler)
            gcd_num = gcd(randomnum2, eiler)
        bezoutnum = multiplicative_inverse(randomnum2, eiler)
        return ((randomnum2, proisved), (bezoutnum, proisved))


def encrypt(pk: tp.Tuple[int, int], plaintext: str) -> tp.List[int]:
    key, n = pk

    cipher = [(ord(char) ** key) % n for char in plaintext]

    return cipher


def decrypt(pk: tp.Tuple[int, int], ciphertext: tp.List[int]) -> str:

    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphertext]

    return "".join(plain)


if __name__ == "__main__":
    print("RSA Encrypter/ Decrypter")
    keynum1 = int(input("Enter a prime number (17, 19, 23, etc): "))
    keynum2 = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(keynum1, keynum2)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print("".join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
