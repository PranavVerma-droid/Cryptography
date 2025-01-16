# Cryptography Project 24-25

## Overview
A Python-based implementation of public key cryptography (RSA) that allows users to encrypt messages, create digital signatures, and verify message authenticity. This project demonstrates fundamental concepts of asymmetric encryption and digital signatures.

## Features
- Message encryption using RSA public key cryptography
- Digital signature creation and verification
- Combined encryption and signing capabilities
- Key pair generation (public/private keys)
- Public key import functionality
- Message and signature file handling

## Setup
1. Clone the repository:
```bash
git clone https://github.com/PranavVerma-droid/Cryptography.git
cd Cryptography/Project
```

2. Run the program:
```bash
python Project.py
```

## Usage

### Main Menu Options
1. **Encrypt a Message**: Encrypt a message using recipient's public key
2. **Sign a Message**: Create a digital signature using your private key
3. **Encrypt and Sign**: Combine encryption and signature
4. **Decrypt a Message**: Decrypt a message using your private key
5. **Verify a Signature**: Verify a message's authenticity
6. **Decrypt and Verify**: Combine decryption and verification
7. **Generate Key Set**: Create new public/private key pair
8. **Load Someone's Public Key**: Import another user's public key
9. **Exit**: Close the program

### Key Management
- Keys are automatically stored in the `keys` directory
- Public keys can be shared (`public.key`)
- Private keys must be kept secure (`private.key`)
- Keys are stored in the format `e,n` or `d,n`

### Security Features
- RSA encryption implementation
- SHA-256 hashing for digital signatures
- Prime number selection between 100-500
- Automatic key generation and storage

## Technical Implementation
- Uses RSA algorithm for encryption/decryption
- Implements digital signatures with SHA-256 hashing
- File-based message and signature storage
- Modular arithmetic for cryptographic operations

## Project File
You can read the entire project file [Here](File.pdf)

## Author
Created by Pranav Verma, Under the [MIT](LICENSE) License.