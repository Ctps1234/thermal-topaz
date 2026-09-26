#!/usr/bin/env bash
# Criptografar todos os arquivos da pasta stock_decrypted ou de uma pasta personalizada
set -e
SRC="${1:-stock_decrypted}"
DST="${2:-output_encrypted}"

echo "[*] Criptografando arquivos de '$SRC' para '$DST'..."
python3 tools/mi_thermal_tool.py encrypt -i "$SRC" -o "$DST"
echo "[+] Concluído com sucesso!"
