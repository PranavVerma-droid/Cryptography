# This file contains the Final Version of my Cryptography Algorithm.
# Made by Pranav Verma, XI Raman.

import random
import math
import os
import sys
import hashlib


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def generate_keys():
    primes = []
    for i in range(100, 501):
        is_prime = True
        for j in range(2, int(math.sqrt(i)) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)

    p = random.choice(primes)
    q = random.choice(primes)
    while p == q:
        q = random.choice(primes)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
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
    
def save_public_key_from_text(key_text):
    try:
        e, n = map(int, key_text.strip().split(','))
        if not os.path.exists('keys'):
            os.makedirs('keys')
            
        with open('keys/public.key', 'w') as f:
            f.write(f"{e},{n}")
        return True
    except:
        return False

def encrypt_message(message, public_key):
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
    # what is this my guy ☠️
    encrypted_message = encrypt_message(message, recipient_public_key)
    signature = sign_message(encrypted_message, sender_private_key)
    return encrypted_message, signature

def verify_and_decrypt(encrypted_message, signature, sender_public_key, recipient_private_key):
    # verify sig
    if not verify_signature(encrypted_message, signature, sender_public_key):
        return False, "Signature verification failed!"
    # decrpt the message.
    decrypted_message = decrypt_message(encrypted_message, recipient_private_key)
    return True, decrypted_message


print("Welcome to the Public Key Message Encoder/Decoder!")

print("\nChoose an option:")
print("")
print("1. Encrypt a Message")
print("2. Sign a Message")
print("3. Do Both 1 & 2")
print("")
print("4. Decrypt a Message")
print("5. Verify a Signature")
print("6. Do Both 4 & 5")
print("")
print("7. Generate Key Set")
print("8. Load Someone's Public Key")
print("")
print("9. Exit the Program")



choice = input("Enter your choice (1, 2, 3, 4, 5, 6, or 7): ")

# number 1
if choice == "1":
    public_key = load_key('keys/public.key')
    message = input("Enter the message to encrypt: ")
    encrypted_message = encrypt_message(message, public_key)
    with open('message.txt', 'w') as f:
        f.write(encrypted_message)
    print("Encrypted message saved to message.txt")

# number 2
elif choice == "2":
    private_key = load_key('keys/private.key')
    message = input("Enter the message to sign: ")
    signature = sign_message(message, private_key)
    with open('signature.txt', 'w') as f:
        f.write(signature)
    print("Message signed and saved to signature.txt")
    print("Share both the message and signature.txt with the recipient")

# number 3
elif choice == "3":
    recipient_public_key = load_key('keys/public.key')
    sender_private_key = load_key('keys/private.key')
    message = input("Enter message to encrypt and sign: ")
    encrypted_message, signature = encrypt_and_sign(message, recipient_public_key, sender_private_key)
    with open('message.txt', 'w') as f:
        f.write(encrypted_message)
    with open('signature.txt', 'w') as f:
        f.write(signature)
    print("Encrypted message and signature saved to message.txt and signature.txt")

# number 4
elif choice == "4":
    private_key = load_key('keys/private.key')
    filename = input("Enter the filename to decrypt: ")
    if not os.path.exists(filename):
        print("File not found.")
        exit()
    with open(filename, 'r') as f:
        encrypted_message = f.read().strip()
    decrypted_message = decrypt_message(encrypted_message, private_key)
    print("Decrypted Message:", decrypted_message)
    
# number 5
elif choice == "5":
    public_key = load_key('keys/public.key')
    message = input("Enter the original message: ")
    with open('signature.txt', 'r') as f:
        signature = f.read().strip()
    if verify_signature(message, signature, public_key):
        print("Signature is valid! Message is authentic.")
    else:
        print("Invalid signature! Message may have been tampered with.")

# number 6
elif choice == "6":
    sender_public_key = load_key('keys/public.key')
    recipient_private_key = load_key('keys/private.key')
    with open('message.txt', 'r') as f:
        encrypted_message = f.read().strip()
    with open('signature.txt', 'r') as f:
        signature = f.read().strip()
    verified, result = verify_and_decrypt(encrypted_message, signature, sender_public_key, recipient_private_key)
    if verified:
        print("Signature verified! Decrypted message:", result)
    else:
        print("Error:", result)

# number 7
elif choice == "7":
    print("Working, please wait....")
    public_key, private_key = generate_keys()
    print("New key set generated and saved in 'keys' directory:")
    print("Public Key (e,n):", public_key)
    print("Private Key (d,n):", private_key)
    print("You can now share your 'public key' with someone who wants to encrypt.")
    print("DO NOT SHARE YOUR PRIVATE KEY! THAT IS ONLY MEANT FOR DECRYPTION!")

# number 8
elif choice == "8":
    print("Enter the public key in the format 'e,n'")
    print("Example: 6553,2341")
    key_text = input("Enter public key: ")
    if save_public_key_from_text(key_text):
        print("Public key successfully loaded and saved to keys/public.key")
    else:
        print("Error: Invalid key format. Please use the format 'e,n' with numbers only")

# number 9
elif choice == "9":
    sys.exit(0)

else:
    print("Please enter 1, 2, 3, 4, 5, 6, or 7.")