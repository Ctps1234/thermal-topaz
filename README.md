# 🔥 Topaz Thermal Engine Mod & Extractor Tool

Repositório completo de extração, descriptografia, análise, modificação e criação de módulos Magisk/KernelSU para os arquivos térmicos do **Redmi Note 12 4G / 12 4G NFC** (Codinomes: `topaz` / `tapas` - Snapdragon 685 / SM6225).

---

## 📋 Índice
1. [O Problema do Thermal Stock a 38°C](#-o-problema-do-thermal-stock-a-38c)
2. [Tabela Comparativa: Stock vs Mod Anti-Throttling](#-tabela-comparativa-stock-vs-mod-anti-throttling)
3. [Módulos Prontos para Flash (Magisk / KernelSU / APatch)](#-módulos-prontos-para-flash)
4. [Estrutura do Repositório](#-estrutura-do-repositório)
5. [Como Funciona a Criptografia da Xiaomi (`mi_thermald`)](#-como-funciona-a-criptografia-da-xiaomi-mi_thermald)
6. [Como Modificar os Arquivos de Configuração](#-como-modificar-os-arquivos-de-configuração)
7. [Como Extrair o Thermal de um Dump Próprio](#-como-extrair-o-thermal-de-um-dump-próprio)
8. [Troca Dinâmica de Perfis via Root (`sconfig`)](#-troca-dinâmica-de-perfis-via-root-sconfig)
9. [Instalação Manual via Root / ADB](#-instalação-manual-via-root--adb)

---

## ❄️ O Problema do Thermal Stock a 38°C

No **Redmi Note 12 4G (topaz/tapas)**, a MIUI / HyperOS aplica uma política térmica extremamente restritiva no perfil padrão (`thermal-normal.conf`).

Mesmo em tarefas simples ou jogando por poucos minutos, assim que o aparelho atinge **35°C a 38°C**, o daemon `mi_thermald` inicia cortes agressivos no clock da CPU, culminando em travamentos severos e quedas de FPS:

- 📉 **Throttling Prematuro dos Big Cores (Cortex-A73):** O clock começa a ser podado logo aos 35°C (2.59 GHz), cai para 2.4 GHz aos 37°C, 2.2 GHz aos 40°C e **despenca para míseros 806 MHz aos 47.5°C**.
- 🚫 **Desligamento Forçado de Núcleos (Hotplug):** Ao atingir 49°C, o sistema desliga fisicamente os núcleos `CPU6` e `CPU7`, cortando 50% dos núcleos de alto desempenho.
- 🔅 **Redução Forçada do Brilho da Tela:** A partir de 41°C, o brilho da tela sofre corte automático.
- ⏱️ **Desativação do Touch Boost:** Aos 47°C, o sistema remove o boost de resposta ao toque (`boost_limit`), fazendo a interface parecer pesada e com atraso no toque.

---

## 📊 Tabela Comparativa: Stock vs Mod Anti-Throttling

| Temperatura | Clock Stock (Big Cluster CPU4-7) | Clock Mod Anti-Throttling | O que acontece no Mod |
|:---:|:---:|:---:|---|
| **< 35°C** | 2.80 GHz | **2.80 GHz** | Clock máximo disponível |
| **35°C - 37°C** | 📉 2.59 GHz *(Throttling)* | **2.80 GHz** | 🚀 **Sem queda de clock** |
| **38°C - 40°C** | 📉 2.40 GHz - 2.20 GHz | **2.80 GHz** | 🚀 **Fluidez total e zero lag** |
| **44°C** | 📉 1.76 GHz | **2.80 GHz** | 🚀 **Sem throttling prematuro** |
| **47.5°C** | 🚨 **806 MHz** *(Travamento)* | **2.80 GHz** | 🚀 **Zero travamentos** |
| **48°C** | 🚨 806 MHz | **2.59 GHz** | Leve transição térmica |
| **51°C** | 🚨 806 MHz | **2.40 GHz** | Alto desempenho constante |
| **53°C** | 🚨 806 MHz | **2.20 GHz** | Desempenho sustentado |
| **55°C** | 🚨 806 MHz | **1.76 GHz** | Controle térmico seguro |
| **57°C** | 🚨 806 MHz | **1.53 GHz** | 🔒 **Piso mínimo travado (nunca cai para 800MHz)** |
| **Hotplug (49°C)** | ❌ Desliga CPU6 e CPU7 | ✅ **8 Núcleos 100% Ativos** | Sem perda de núcleos |
| **Brilho (41°C)** | 🔅 Tela escurece | ☀️ **Brilho 100% Livre até 60°C** | Sem escurecimento surpresa |

---

## 📦 Módulos Prontos para Flash

Na pasta `flashable_modules/` você encontra os módulos `.zip` prontos para instalação direta pelo **Magisk**, **KernelSU** ou **APatch**:

| Módulo | Descrição | Cenário Indicado |
|---|---|---|
| **`Topaz_Thermal_Mod_Normal_AntiThrottling.zip`** | **Solução direta para o thermal-normal:** Mantém clock máximo de CPU até 48°C, nunca cai para 800MHz (piso em 1.53GHz), 8 núcleos sempre ativos e sem escurecimento de tela. | ⭐ **Recomendado para o problema dos 38°C** |
| **`Topaz_Thermal_Mod_Gaming_Performance.zip`** | Ajusta tanto o `thermal-normal` quanto o `thermal-tgame` (Game Turbo) com margem estendida para jogos pesados. | 🎮 **Jogos e Emuladores** |
| **`Topaz_Thermal_Mod_Extreme_NoLimits.zip`** | Remove quase todas as travas térmicas intermediárias (salvaguarda de emergência a 58°C). | 🚀 **Benchmarks e Máximo FPS** |
| **`Topaz_Thermal_Mod_Balanced.zip`** | Margem moderada (+5°C), elimina a queda para 800MHz e mantém consumo balanceado. | 🔋 **Uso Diário Moderado** |
| **`Topaz_Thermal_Mod_Fast_Charge.zip`** | Focado em evitar que o carregamento rápido de 33W seja reduzido a 35°C-38°C. | ⚡ **Carga Rápida Contínua** |

### Como Instalar:
1. Baixe o módulo `.zip` desejado da pasta `flashable_modules/`.
2. Abra o aplicativo do **Magisk**, **KernelSU** ou **APatch**.
3. Vá na aba **Módulos** -> **Instalar a partir do armazenamento**.
4. Selecione o arquivo `.zip` e aguarde a conclusão.
5. Reinicie o celular.

---

## 📁 Estrutura do Repositório

```text
thermal-topaz/
├── flashable_modules/                     # Módulos prontos em .zip para Magisk / KernelSU / APatch
│   ├── Topaz_Thermal_Mod_Normal_AntiThrottling.zip   <-- Mod específico para o thermal normal
│   ├── Topaz_Thermal_Mod_Gaming_Performance.zip
│   ├── Topaz_Thermal_Mod_Extreme_NoLimits.zip
│   ├── Topaz_Thermal_Mod_Balanced.zip
│   └── Topaz_Thermal_Mod_Fast_Charge.zip
│
├── stock_decrypted/                       # Arquivos stock originais descriptografados (Texto puro)
│   ├── thermal-normal.conf                # Perfil padrão stock
│   ├── thermal-tgame.conf                 # Perfil Game Turbo stock
│   ├── thermal-nolimits.conf              # Perfil sem limites de fábrica
│   ├── thermal-map.conf                   # Mapeamento de perfis (sconfig)
│   └── ... (todos os 13 arquivos conf)
│
├── stock_encrypted/                       # Arquivos stock originais criptografados
│
├── mods/                                  # Configurações modificadas geradas
│   ├── thermal_normal_anti_throttling/    # Mod Anti-Throttling do thermal-normal
│   ├── gaming_performance/                # Mod Gaming & Performance
│   ├── extreme_nolimits/                  # Mod Extreme / Sem Limites
│   ├── balanced/                          # Mod Balanceado
│   └── fast_charge/                       # Mod Focado em Carregamento Rápido
│
└── tools/                                 # Scripts utilitários em Python
    ├── mi_thermal_tool.py                 # Descriptografa e criptografa arquivos .conf
    ├── extract_thermal_from_dump.py       # Extrai thermals de qualquer dump / pasta / zip
    ├── generate_mods.py                   # Gera as configurações dos perfis de mod
    └── build_magisk_modules.py            # Compila os pacotes .zip do Magisk
```

---

## 🔐 Como Funciona a Criptografia da Xiaomi (`mi_thermald`)

O daemon `/vendor/bin/mi_thermald` exige que os arquivos `.conf` estejam criptografados:

- **Algoritmo:** `AES-128-CBC` com padding `PKCS#7`
- **Key:** `thermalopenssl.h` (`746865726d616c6f70656e73736c2e68`)
- **IV:** `thermalopenssl.h` (`746865726d616c6f70656e73736c2e68`)

---

## 🛠️ Como Modificar os Arquivos de Configuração

### Descriptografar para editar:
```bash
python3 tools/mi_thermal_tool.py decrypt -i stock_encrypted/thermal-normal.conf -o custom-normal.conf
```

### Criptografar de volta após alterar:
```bash
python3 tools/mi_thermal_tool.py encrypt -i custom-normal.conf -o thermal-normal.conf
```

### Recompilar todos os módulos Magisk:
```bash
./build_all_modules.sh
```

---

## 🔍 Como Extrair o Thermal de um Dump Próprio

```bash
./extract_from_dump.sh /caminho/do/seu/dump ./meu_thermal_extraido
```

---

## 🔀 Troca Dinâmica de Perfis via Root (`sconfig`)

Você pode testar perfis instantaneamente via Termux com root sem reiniciar:

```bash
su
# Ativar modo Normal:
echo 0 > /sys/class/thermal/thermal_message/sconfig

# Ativar modo Game Turbo:
echo 9 > /sys/class/thermal/thermal_message/sconfig

# Ativar modo Sem Limites:
echo 10 > /sys/class/thermal/thermal_message/sconfig
```

---

## 📲 Instalação Manual via Root / ADB

```bash
adb root
adb remount
adb push mods/thermal_normal_anti_throttling/encrypted/*.conf /vendor/etc/
adb shell chmod 0644 /vendor/etc/thermal*.conf
adb shell rm -f /data/vendor/thermal/config/*
adb shell stop mi_thermald
adb shell start mi_thermald
```
