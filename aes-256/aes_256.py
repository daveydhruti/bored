"""
AES-256 Encryption/Decryption Program
Implements secure AES-256-GCM encryption with proper key derivation
"""

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os
import base64
import getpass


class AES256Cipher:
    """AES-256-GCM encryption with PBKDF2 key derivation"""
    
    def __init__(self):
        self.key_length = 32  # 256 bits
        self.salt_length = 16
        self.nonce_length = 12
        self.iterations = 600000  # OWASP recommended minimum
    
    def derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive a 256-bit key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.key_length,
            salt=salt,
            iterations=self.iterations
        )
        return kdf.derive(password.encode())
    
    def encrypt(self, plaintext: str, password: str) -> str:
        """
        Encrypt plaintext using AES-256-GCM
        Returns base64-encoded: salt + nonce + ciphertext + tag
        """
        # Generate random salt and nonce
        salt = os.urandom(self.salt_length)
        nonce = os.urandom(self.nonce_length)
        
        # Derive key from password
        key = self.derive_key(password, salt)
        
        # Encrypt using AES-GCM
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
        
        # Combine salt + nonce + ciphertext (includes auth tag)
        encrypted_data = salt + nonce + ciphertext
        
        # Return base64-encoded result
        return base64.b64encode(encrypted_data).decode()
    
    def decrypt(self, encrypted_b64: str, password: str) -> str:
        """
        Decrypt base64-encoded ciphertext using AES-256-GCM
        Returns original plaintext
        """
        # Decode from base64
        encrypted_data = base64.b64decode(encrypted_b64)
        
        # Extract components
        salt = encrypted_data[:self.salt_length]
        nonce = encrypted_data[self.salt_length:self.salt_length + self.nonce_length]
        ciphertext = encrypted_data[self.salt_length + self.nonce_length:]
        
        # Derive key from password
        key = self.derive_key(password, salt)
        
        # Decrypt using AES-GCM
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        return plaintext.decode()
    
    def encrypt_file(self, input_path: str, output_path: str, password: str):
        """Encrypt a file"""
        with open(input_path, 'rb') as f:
            plaintext = f.read()
        
        salt = os.urandom(self.salt_length)
        nonce = os.urandom(self.nonce_length)
        key = self.derive_key(password, salt)
        
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        
        with open(output_path, 'wb') as f:
            f.write(salt + nonce + ciphertext)
    
    def decrypt_file(self, input_path: str, output_path: str, password: str):
        """Decrypt a file"""
        with open(input_path, 'rb') as f:
            encrypted_data = f.read()
        
        salt = encrypted_data[:self.salt_length]
        nonce = encrypted_data[self.salt_length:self.salt_length + self.nonce_length]
        ciphertext = encrypted_data[self.salt_length + self.nonce_length:]
        
        key = self.derive_key(password, salt)
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        with open(output_path, 'wb') as f:
            f.write(plaintext)


def main():
    cipher = AES256Cipher()
    
    print("=== AES-256 Encryption Tool ===\n")
    print("1. Encrypt text")
    print("2. Decrypt text")
    print("3. Encrypt file")
    print("4. Decrypt file")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    try:
        if choice == '1':
            plaintext = input("Enter text to encrypt: ")
            password = getpass.getpass("Enter password: ")
            encrypted = cipher.encrypt(plaintext, password)
            print(f"\nEncrypted (base64):\n{encrypted}")
        
        elif choice == '2':
            encrypted = input("Enter encrypted text (base64): ")
            password = getpass.getpass("Enter password: ")
            decrypted = cipher.decrypt(encrypted, password)
            print(f"\nDecrypted text:\n{decrypted}")
        
        elif choice == '3':
            input_file = input("Enter input file path: ")
            output_file = input("Enter output file path: ")
            password = getpass.getpass("Enter password: ")
            cipher.encrypt_file(input_file, output_file, password)
            print(f"\nFile encrypted successfully: {output_file}")
        
        elif choice == '4':
            input_file = input("Enter encrypted file path: ")
            output_file = input("Enter output file path: ")
            password = getpass.getpass("Enter password: ")
            cipher.decrypt_file(input_file, output_file, password)
            print(f"\nFile decrypted successfully: {output_file}")
        
        else:
            print("Invalid option")
    
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
