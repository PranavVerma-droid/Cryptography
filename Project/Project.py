# This file contains the Final Version of my Cryptography Algorithm.
# Made by Pranav Verma, XI Raman.

import CryptoLib as lb;
import os;
import sys;

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


while True:
    choice = input("Enter your choice (1, 2, 3, 4, 5, 6, or 7): ")

    # number 1
    if choice == "1":
        public_key = lb.load_key('keys/public.key')
        message = input("Enter the message to encrypt: ")
        encrypted_message = lb.encryptMessage(message, public_key)
        with open('message.txt', 'w') as f:
            f.write(encrypted_message)
        print("Encrypted message saved to message.txt")

    # number 2
    elif choice == "2":
        private_key = lb.load_key('keys/private.key')
        message = input("Enter the message to sign: ")
        signature = lb.sign_message(message, private_key)
        with open('signature.txt', 'w') as f:
            f.write(signature)
        print("Message signed and saved to signature.txt")
        print("Share both the message and signature.txt with the recipient")

    # number 3
    elif choice == "3":
        recipient_public_key = lb.load_key('keys/public.key')
        sender_private_key = lb.load_key('keys/private.key')
        message = input("Enter message to encrypt and sign: ")
        encrypted_message, signature = lb.encrypt_and_sign(message, recipient_public_key, sender_private_key)
        with open('message.txt', 'w') as f:
            f.write(encrypted_message)
        with open('signature.txt', 'w') as f:
            f.write(signature)
        print("Encrypted message and signature saved to message.txt and signature.txt")

    # number 4
    elif choice == "4":
        private_key = lb.load_key('keys/private.key')
        filename = 'message.txt'
        if not os.path.exists(filename):
            print("File not found.")
            exit()
        with open(filename, 'r') as f:
            encrypted_message = f.read().strip()
        decrypted_message = lb.decrypt_message(encrypted_message, private_key)
        print("Decrypted Message:", decrypted_message)
        
    # number 5
    elif choice == "5":
        public_key = lb.load_key('keys/public.key')
        message = input("Enter the original message: ")
        filename = 'signature.txt'
        if not os.path.exists(filename):
            print("File not found.")
            exit()
        with open(filename, 'r') as f:
            signature = f.read().strip()
        if lb.verify_signature(message, signature, public_key):
            print("Signature is valid! Message is authentic.")
        else:
            print("Invalid signature! Message may have been tampered with.")

    # number 6
    elif choice == "6":
        sender_public_key = lb.load_key('keys/public.key')
        recipient_private_key = lb.load_key('keys/private.key')
        if (not os.path.exists('signature.txt')):
            print("Signature Not Found.")
            exit()
        if (not os.path.exists('message.txt')):
            print("Message.txt Not Found.")
            exit()
        with open('message.txt', 'r') as f:
            encrypted_message = f.read().strip()
        with open('signature.txt', 'r') as f:
            signature = f.read().strip()
        verified, result = lb.verify_and_decrypt(encrypted_message, signature, sender_public_key, recipient_private_key)
        if verified:
            print("Signature verified! Decrypted message:", result)
        else:
            print("Error:", result)

    # number 7
    elif choice == "7":
        print("Working, please wait....")
        public_key, private_key = lb.generate_keys()
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
        if lb.saveKeyFromText(key_text):
            print("Public key successfully loaded and saved to keys/public.key")
        else:
            print("Error: Invalid key format. Please use the format 'e,n' with numbers only")

    # number 9
    elif choice == "9":
        sys.exit(0)

    else:
        print("Please enter 1, 2, 3, 4, 5, 6, or 7.")