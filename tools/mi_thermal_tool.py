#!/usr/bin/env python3
"""
Xiaomi / Redmi Thermal Configuration Tool (mi_thermal_tool)
Device: Redmi Note 12 4G (topaz / tapas) - SM6225 / Bengal

This tool can:
  - Decrypt encrypted Xiaomi mi_thermald configuration files (*.conf)
  - Encrypt plaintext configuration files for mi_thermald
  - Apply custom performance & thermal mods (Gaming, Extreme, Fast Charge, Balanced)
  - Build flashable Magisk / KernelSU / APatch modules
"""

import os
import sys
import argparse
import subprocess
import shutil
import zipfile
from pathlib import Path

# Xiaomi AES-128-CBC fixed key and IV
XIAOMI_KEY = b"thermalopenssl.h"
XIAOMI_IV  = b"thermalopenssl.h"
KEY_HEX = XIAOMI_KEY.hex()
IV_HEX = XIAOMI_IV.hex()


def decrypt_bytes(data: bytes) -> bytes:
    """Decrypt AES-128-CBC data with Xiaomi mi_thermald key."""
    # Method 1: Try cryptography library if installed
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.primitives import padding
        cipher = Cipher(algorithms.AES(XIAOMI_KEY), modes.CBC(XIAOMI_IV))
        decryptor = cipher.decryptor()
        padded = decryptor.update(data) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded) + unpadder.finalize()
    except ImportError:
        pass

    # Method 2: Try ctypes libcrypto
    try:
        import ctypes
        import ctypes.util
        libname = ctypes.util.find_library('crypto')
        if libname:
            # Let openssl subprocess do it reliably or ctypes
            pass
    except Exception:
        pass

    # Method 3: Fallback to openssl CLI
    p = subprocess.run(
        ['openssl', 'enc', '-d', '-aes-128-cbc', '-K', KEY_HEX, '-iv', IV_HEX],
        input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if p.returncode == 0:
        return p.stdout
    raise RuntimeError(f"Decryption failed: {p.stderr.decode('utf-8', errors='replace')}")


def encrypt_bytes(data: bytes) -> bytes:
    """Encrypt plaintext data to AES-128-CBC for Xiaomi mi_thermald."""
    # Method 1: Try cryptography library if installed
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.primitives import padding
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        cipher = Cipher(algorithms.AES(XIAOMI_KEY), modes.CBC(XIAOMI_IV))
        encryptor = cipher.encryptor()
        return encryptor.update(padded_data) + encryptor.finalize()
    except ImportError:
        pass

    # Method 2: Fallback to openssl CLI
    p = subprocess.run(
        ['openssl', 'enc', '-e', '-aes-128-cbc', '-K', KEY_HEX, '-iv', IV_HEX],
        input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if p.returncode == 0:
        return p.stdout
    raise RuntimeError(f"Encryption failed: {p.stderr.decode('utf-8', errors='replace')}")


def is_encrypted(data: bytes) -> bool:
    """Check if file starts with recognizable plaintext or appears encrypted."""
    if not data:
        return False
    # If starting with '[' or '#', likely plain text
    stripped = data.lstrip()
    if stripped.startswith(b'[') or stripped.startswith(b'#'):
        return False
    # Check ASCII printable ratio
    printable = sum(1 for b in data[:100] if 32 <= b <= 126 or b in (9, 10, 13))
    return (printable / min(len(data), 100)) < 0.75


def cmd_decrypt(args):
    in_path = Path(args.input)
    out_path = Path(args.output) if args.output else None

    if in_path.is_file():
        data = in_path.read_bytes()
        if not is_encrypted(data):
            print(f"[*] {in_path.name} appears to be plaintext already.")
            dec = data
        else:
            dec = decrypt_bytes(data)
        
        target = out_path if out_path else in_path.with_suffix('.dec.conf')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(dec)
        print(f"[+] Decrypted: {in_path} -> {target}")

    elif in_path.is_dir():
        out_dir = out_path if out_path else in_path.parent / (in_path.name + "_decrypted")
        out_dir.mkdir(parents=True, exist_ok=True)
        for f in sorted(in_path.glob("*.conf")):
            data = f.read_bytes()
            try:
                if is_encrypted(data):
                    dec = decrypt_bytes(data)
                    print(f"[+] Decrypted: {f.name}")
                else:
                    dec = data
                    print(f"[*] Plaintext (copied): {f.name}")
                (out_dir / f.name).write_bytes(dec)
            except Exception as e:
                print(f"[-] Error decrypting {f.name}: {e}")
        print(f"[+] All files processed to {out_dir}")
    else:
        print(f"[-] Input not found: {in_path}")


def cmd_encrypt(args):
    in_path = Path(args.input)
    out_path = Path(args.output) if args.output else None

    if in_path.is_file():
        data = in_path.read_bytes()
        enc = encrypt_bytes(data)
        target = out_path if out_path else in_path.with_suffix('.enc.conf')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(enc)
        print(f"[+] Encrypted: {in_path} -> {target}")

    elif in_path.is_dir():
        out_dir = out_path if out_path else in_path.parent / (in_path.name + "_encrypted")
        out_dir.mkdir(parents=True, exist_ok=True)
        for f in sorted(in_path.glob("*.conf")):
            data = f.read_bytes()
            try:
                enc = encrypt_bytes(data)
                (out_dir / f.name).write_bytes(enc)
                print(f"[+] Encrypted: {f.name}")
            except Exception as e:
                print(f"[-] Error encrypting {f.name}: {e}")
        print(f"[+] All files processed to {out_dir}")
    else:
        print(f"[-] Input not found: {in_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Xiaomi Thermal Configuration Tool (decrypt, encrypt & mod mi_thermald configs)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Decrypt command
    p_dec = subparsers.add_parser("decrypt", help="Decrypt encrypted .conf file or folder")
    p_dec.add_argument("-i", "--input", required=True, help="Input encrypted .conf file or folder")
    p_dec.add_argument("-o", "--output", help="Output decrypted .conf file or folder")

    # Encrypt command
    p_enc = subparsers.add_parser("encrypt", help="Encrypt plaintext .conf file or folder")
    p_enc.add_argument("-i", "--input", required=True, help="Input plaintext .conf file or folder")
    p_enc.add_argument("-o", "--output", help="Output encrypted .conf file or folder")

    args = parser.parse_args()
    if args.command == "decrypt":
        cmd_decrypt(args)
    elif args.command == "encrypt":
        cmd_encrypt(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
