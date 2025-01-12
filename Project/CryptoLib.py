# Crypto Library w/ all Functions.
# Made by Pranav Verma from XI Raman

import random;
import math;
import os;
import hashlib;

# standard gcd function
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def generate_keys():
    primes = []
    for i in range(100, 501):
        is_prime = True
        for j in range(2, int(math.sqrt(i)) + 1):
            if i % j == 0: #check for prime
                is_prime = False
                break
        if is_prime:
            primes.append(i)

    p = random.choice(primes) # random select prime 1
    q = random.choice(primes) # random select prime 2
    while p == q: # the two numbers should not be equal to the other 
        q = random.choice(primes)

    n = p * q # calc. base
    phi = (p - 1) * (q - 1) #eulers totient function

    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1: # calc gcd
        e = random.randint(2, phi - 1)

    d = pow(e, -1, phi)

    if not os.path.exists('keys'):
        os.makedirs('keys')

    with open('keys/public.key', 'w') as f:
        f.write(f"{e},{n}")

    with open('keys/private.key', 'w') as f:
        f.write(f"{d},{n}")

    return ((e, n), (d, n))

def load_key(filename):
    if not os.path.exists(filename):
        print("Please generate keys first.")
        exit()
    with open(filename, 'r') as f:
        key = f.read().strip().split(',')
        return (int(key[0]), int(key[1]))
    
def saveKeyFromText(key_text):
    try:
        e, n = map(int, key_text.strip().split(','))
        if not os.path.exists('keys'):
            os.makedirs('keys')
            
        with open('keys/public.key', 'w') as f:
            f.write(f"{e},{n}")
        return True
    except:
        return False
    
def encryptMessage(message, public_key):
    e, n = public_key
    encrypted_message = []
    for char in message:
        encrypted_char = (ord(char) ** e) % n
        encrypted_message.append(str(encrypted_char))
    return ' '.join(encrypted_message)

def decrypt_message(encrypted_message, private_key):
    d, n = private_key
    encrypted_chars = encrypted_message.split()
    decrypted_message = ''.join([chr((int(char) ** d) % n) for char in encrypted_chars])
    return decrypted_message

def hash_message(message):
    return hashlib.sha256(message.encode()).hexdigest()

def sign_message(message, private_key):
    d, n = private_key
    message_hash = hash_message(message)
    signature = []
    for char in message_hash:
        # ok how did this actually work
        signed_char = pow(ord(char), d, n)
        signature.append(str(signed_char))
    return ' '.join(signature)

def verify_signature(message, signature, public_key):
    e, n = public_key
    # make the hash from original sig.
    signature_nums = signature.split()
    recovered_hash = ''
    for num in signature_nums:
        char = pow(int(num), e, n)
        recovered_hash += chr(char)
    # compare
    return recovered_hash == hash_message(message)

def encrypt_and_sign(message, recipient_public_key, sender_private_key):
    encrypted_message = encryptMessage(message, recipient_public_key)
    signature = sign_message(encrypted_message, sender_private_key)
    return encrypted_message, signature

def verify_and_decrypt(encrypted_message, signature, sender_public_key, recipient_private_key):
    # verify sig
    if not verify_signature(encrypted_message, signature, sender_public_key):
        return False, "Signature verification failed!"
    # decrpt the message.
    decrypted_message = decrypt_message(encrypted_message, recipient_private_key)
    return True, decrypted_message