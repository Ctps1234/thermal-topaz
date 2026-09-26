#!/usr/bin/env bash
# Descriptografar todos os arquivos da pasta stock_encrypted ou de uma pasta personalizada
set -e
SRC="${1:-stock_encrypted}"
DST="${2:-stock_decrypted}"

echo "[*] Descriptografando arquivos de '$SRC' para '$DST'..."
python3 tools/mi_thermal_tool.py decrypt -i "$SRC" -o "$DST"
echo "[+] Concluído com sucesso!"
