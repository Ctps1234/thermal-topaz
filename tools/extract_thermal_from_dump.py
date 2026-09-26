#!/usr/bin/env python3
"""
Xiaomi Dump Thermal Extractor & Analyzer
Redmi Note 12 4G (topaz / tapas) - SM6225

Automatically searches, extracts, decrypts, and analyzes thermal configs
from any ROM dump folder, ZIP, or extracted image.
"""

import os
import sys
import shutil
import zipfile
import argparse
from pathlib import Path
from mi_thermal_tool import decrypt_bytes, is_encrypted

THERMAL_PATTERNS = [
    "thermal*.conf",
    "thermald*.conf"
]


def search_and_extract(input_path: Path, output_dir: Path):
    output_dec = output_dir / "decrypted"
    output_enc = output_dir / "encrypted"
    output_dec.mkdir(parents=True, exist_ok=True)
    output_enc.mkdir(parents=True, exist_ok=True)

    found_files = []

    if input_path.is_file():
        # Check if zip
        if zipfile.is_zipfile(input_path):
            print(f"[*] Scanning ZIP archive: {input_path}")
            with zipfile.ZipFile(input_path, 'r') as z:
                for member in z.namelist():
                    basename = os.path.basename(member)
                    if any(basename.startswith(p.replace("*.conf", "")) and basename.endswith(".conf") for p in THERMAL_PATTERNS):
                        raw_data = z.read(member)
                        out_enc_file = output_enc / basename
                        out_enc_file.write_bytes(raw_data)
                        found_files.append((basename, raw_data, member))
        else:
            # Single file
            raw_data = input_path.read_bytes()
            out_enc_file = output_enc / input_path.name
            out_enc_file.write_bytes(raw_data)
            found_files.append((input_path.name, raw_data, str(input_path)))

    elif input_path.is_dir():
        print(f"[*] Scanning directory: {input_path}")
        for root, _, files in os.walk(input_path):
            for file in files:
                if any(file.startswith(p.replace("*.conf", "")) and file.endswith(".conf") for p in THERMAL_PATTERNS):
                    full_p = Path(root) / file
                    raw_data = full_p.read_bytes()
                    out_enc_file = output_enc / file
                    out_enc_file.write_bytes(raw_data)
                    found_files.append((file, raw_data, str(full_p)))

    print(f"[+] Found {len(found_files)} thermal configuration files:")
    for name, data, original_loc in found_files:
        try:
            if is_encrypted(data):
                dec = decrypt_bytes(data)
                status = "Decrypted (Encrypted AES-128-CBC -> Plaintext)"
            else:
                dec = data
                status = "Plaintext"
            (output_dec / name).write_bytes(dec)
            print(f"    - {name} [{status}] from {original_loc}")
        except Exception as e:
            print(f"    - {name} [Error: {e}]")

    print(f"\n[+] Decrypted plain text configs saved to: {output_dec.resolve()}")
    print(f"[+] Encrypted raw files saved to: {output_enc.resolve()}")
    return output_dec


def analyze_thermal_conf(conf_path: Path):
    """Parse and summarize key throttling thresholds in a thermal file."""
    if not conf_path.exists():
        return
    text = conf_path.read_text(errors='replace')
    print(f"\n==================== Analysis: {conf_path.name} ====================")
    lines = text.splitlines()
    current_section = None
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current_section = line
            print(f"\n{current_section}")
        elif current_section:
            parts = line.split()
            if len(parts) >= 2:
                key = parts[0]
                values = " ".join(parts[1:])
                if key in ("algo_type", "device", "sensor", "trig", "clr", "target"):
                    if key in ("trig", "clr") and any(v.isdigit() for v in parts[1:]):
                        temps = []
                        for val in parts[1:]:
                            try:
                                t_c = float(val) / 1000.0 if float(val) > 100 else float(val)
                                temps.append(f"{t_c:.1f}C")
                            except ValueError:
                                temps.append(val)
                        print(f"  {key:<12}: {' '.join(temps)}  (raw: {values})")
                    else:
                        print(f"  {key:<12}: {values}")


def main():
    parser = argparse.ArgumentParser(description="Extract and decrypt thermal configs from Xiaomi ROM dump")
    parser.add_argument("-i", "--input", required=True, help="Input directory, ZIP archive, or file from dump")
    parser.add_argument("-o", "--output", default="./extracted_thermal", help="Output directory")
    parser.add_argument("--analyze", action="store_true", help="Analyze thermal throttling rules after extraction")
    args = parser.parse_args()

    input_p = Path(args.input)
    output_p = Path(args.output)

    dec_dir = search_and_extract(input_p, output_p)
    if args.analyze or True:
        normal_conf = dec_dir / "thermal-normal.conf"
        if normal_conf.exists():
            analyze_thermal_conf(normal_conf)
        tgame_conf = dec_dir / "thermal-tgame.conf"
        if tgame_conf.exists():
            analyze_thermal_conf(tgame_conf)


if __name__ == "__main__":
    main()
