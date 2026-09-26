#!/usr/bin/env bash
# Gerar presets de mod e compilar módulos Magisk / KernelSU / APatch
set -e

echo "[1/2] Gerando perfis modificados (Gaming, Extreme, Balanced, Fast Charge)..."
python3 tools/generate_mods.py

echo "[2/2] Construindo pacotes .zip instaláveis via Magisk/KernelSU..."
python3 tools/build_magisk_modules.py

echo ""
echo "[+] Módulos prontos gerados na pasta 'flashable_modules/':"
ls -lh flashable_modules/*.zip
