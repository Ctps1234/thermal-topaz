#!/usr/bin/env bash
# Extrair e descriptografar automaticamente os thermals de uma pasta de dump ou zip
set -e

if [ -z "$1" ]; then
    echo "Uso: ./extract_from_dump.sh <caminho_do_dump_ou_zip> [pasta_destino]"
    echo "Exemplo: ./extract_from_dump.sh /caminho/para/dump_topaz ./meu_thermal_extraido"
    exit 1
fi

INPUT="$1"
OUTPUT="${2:-./extracted_thermal}"

python3 tools/extract_thermal_from_dump.py -i "$INPUT" -o "$OUTPUT" --analyze
