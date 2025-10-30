#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

# Decoded from modem audio files
key_string = "O1WXfra0lbr84OrUsARr2xf5mDDCnJ1S"
ciphertext_b64 = "Eswf9G+Vm6xxJg9MrPmuz2Ar9VGyWUDKSR0/rFoVfcoNT12NA1Nk59sBJbOE8li7btNC82vX0KINmSEvK9hp1A=="
mode_info = "CBC PKCS5Padding"

print("Decoded Information:")
print(f"Key: {key_string}")
print(f"Ciphertext (base64): {ciphertext_b64}")
print(f"Mode: {mode_info}")
print()

# Decode the ciphertext from base64
ciphertext = base64.b64decode(ciphertext_b64)
print(f"Ciphertext length: {len(ciphertext)} bytes")

# The key string is 32 characters
# Try different interpretations:

# Method 1: Use key string as-is (ASCII bytes)
print("\n" + "="*60)
print("Method 1: Key as ASCII bytes (32 bytes = AES-256)")
print("="*60)
try:
    key = key_string.encode('ascii')
    print(f"Key length: {len(key)} bytes")

    # In CBC mode, the IV is typically the first block of ciphertext
    # Or we might need to extract it separately
    # Let's try assuming the first 16 bytes are the IV
    if len(ciphertext) >= 16:
        iv = ciphertext[:16]
        encrypted_data = ciphertext[16:]

        print(f"IV: {iv.hex()}")
        print(f"Encrypted data length: {len(encrypted_data)} bytes")

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_data)

        # Remove PKCS5/PKCS7 padding
        plaintext = unpad(decrypted, AES.block_size)

        print(f"Decrypted: {plaintext}")
        try:
            print(f"Decoded as text: {plaintext.decode('ascii')}")
        except:
            print(f"Decoded as text: {plaintext.decode('utf-8', errors='ignore')}")
except Exception as e:
    print(f"Error: {e}")

# Method 2: Try the entire ciphertext without separate IV
print("\n" + "="*60)
print("Method 2: No separate IV (might be embedded in key)")
print("="*60)
try:
    key = key_string.encode('ascii')

    # Try using first 16 bytes of key as IV
    iv = key[:16]

    print(f"Using first 16 bytes of key as IV: {iv.hex()}")

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)

    # Remove PKCS5/PKCS7 padding
    plaintext = unpad(decrypted, AES.block_size)

    print(f"Decrypted: {plaintext}")
    try:
        print(f"Decoded as text: {plaintext.decode('ascii')}")
    except:
        print(f"Decoded as text: {plaintext.decode('utf-8', errors='ignore')}")
except Exception as e:
    print(f"Error: {e}")

# Method 3: Key might be base64 encoded itself
print("\n" + "="*60)
print("Method 3: Key is base64 encoded")
print("="*60)
try:
    # Add padding if needed for base64
    key_padded = key_string
    padding_needed = (4 - len(key_padded) % 4) % 4
    key_padded += '=' * padding_needed

    key = base64.b64decode(key_padded)
    print(f"Decoded key length: {len(key)} bytes")

    if len(ciphertext) >= 16:
        iv = ciphertext[:16]
        encrypted_data = ciphertext[16:]

        print(f"IV: {iv.hex()}")

        # Adjust key length to match AES requirements (16, 24, or 32 bytes)
        if len(key) == 16 or len(key) == 24 or len(key) == 32:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(encrypted_data)

            # Remove PKCS5/PKCS7 padding
            plaintext = unpad(decrypted, AES.block_size)

            print(f"Decrypted: {plaintext}")
            try:
                print(f"Decoded as text: {plaintext.decode('ascii')}")
            except:
                print(f"Decoded as text: {plaintext.decode('utf-8', errors='ignore')}")
        else:
            print(f"Key length {len(key)} is not valid for AES")
except Exception as e:
    print(f"Error: {e}")

# Method 4: Zero IV
print("\n" + "="*60)
print("Method 4: Using zero IV")
print("="*60)
try:
    key = key_string.encode('ascii')
    iv = b'\x00' * 16

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)

    # Remove PKCS5/PKCS7 padding
    plaintext = unpad(decrypted, AES.block_size)

    print(f"Decrypted: {plaintext}")
    try:
        print(f"Decoded as text: {plaintext.decode('ascii')}")
    except:
        print(f"Decoded as text: {plaintext.decode('utf-8', errors='ignore')}")
except Exception as e:
    print(f"Error: {e}")
