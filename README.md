# Password Manager

**Owner:** Laurent Zogaj  
**Date delivered:** April 11, 2025  
**Updated:** April 26, 2025  

## Description
This project is a password manager that enables users to store, retrieve, and manage passwords locally on their computer. 

Passwords are encrypted using the cryptography library with symmetric encryption (Fernet). The program also provides functionality to generate random and secure passwords. The content is stored in a CSV file and encrypted/decrypted there.

## Main Features
- Secure storage and retrieval of passwords
- Generation of strong random passwords
- Simple graphical user interface (GUI)
- Easy password management

## Dependencies
The following packages must be installed:
```
pip install cryptography
```

## File Structure
The program creates the following files:
- `passwords.csv`: Stored passwords (encrypted)
- `secret.key`: Encryption key

## User Guide
1. Install dependencies as described above
2. Download the repository in its entirety
3. Run `password_manager.py`
4. The first time the program runs, it will create an encryption key
5. Use the GUI to add, view, and manage passwords etc.

## Security
- All passwords are encrypted with Fernet encryption before storage
- The encryption key is stored separately in `secret.key`
- The content of the CSV file is unreadable without the correct decryption key

## Future Features
Future extensions planned for the project:
- Better handling of encryption key
- Add master password for program access
- Add support for JSON format
- SQLite integration
- Base64 implementation for additional security layer
- Support for multiple languages
- General code improvements