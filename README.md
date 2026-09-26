# 🔥 Topaz Thermal Engine Mod & Extractor Tool

Repositório completo de extração, descriptografia, análise, modificação e criação de módulos Magisk/KernelSU para os arquivos térmicos do **Redmi Note 12 4G / 12 4G NFC** (Codinomes: `topaz` / `tapas` - Snapdragon 685 / SM6225).

---

## 📋 Índice
1. [Visão Geral e Problema do Thermal Stock](#-visão-geral-e-o-problema-do-thermal-stock)
2. [Estrutura do Repositório](#-estrutura-do-repositório)
3. [Como Funciona a Criptografia da Xiaomi (`mi_thermald`)](#-como-funciona-a-criptografia-da-xiaomi-mi_thermald)
4. [Módulos Prontos para Flash (Magisk / KernelSU / APatch)](#-módulos-prontos-para-flash)
5. [Como Extrair o Thermal de um Dump Próprio](#-como-extrair-o-thermal-de-um-dump-próprio)
6. [Como Modificar os Arquivos de Configuração](#-como-modificar-os-arquivos-de-configuração)
7. [Entendendo os Parâmetros Térmicos (.conf)](#-entendendo-os-parâmetros-térmicos-conf)
8. [Troca Dinâmica de Perfis via Terminal/Root (`sconfig`)](#-troca-dinâmica-de-perfis-via-root-sconfig)
9. [Instalação Manual via Root / ADB](#-instalação-manual-via-root--adb)

---

## ⚡ Visão Geral e o Problema do Thermal Stock

No **Redmi Note 12 4G (topaz/tapas)**, o daemon de controle térmico da Xiaomi (`mi_thermald`) vem de fábrica com perfis extremamente agressivos que causam quedas bruscas de desempenho (thermal throttling):

- 📉 **CPU Throttling Prematuro:** O cluster de alta performance (Cortex-A73 @ 2.8GHz) começa a reduzir clock a apenas **35°C**, caindo até míseros **806 MHz** a 47.5°C.
- 🚫 **Desligamento de Núcleos (Hotplug):** A 49°C, o sistema desliga completamente 2 núcleos grandes (`CPU6` e `CPU7`), cortando pela metade o poder de processamento do Snapdragon 685.
- 🔅 **Redução de Brilho da Tela:** A partir de 41°C, o brilho máximo da tela é reduzido forçadamente.
- ⚡ **Carregamento Lento:** O carregamento turbo de 33W é reduzido progressivamente assim que a bateria atinge 35°C.

Este projeto resolve todos esses problemas através de modificações calibradas nas tabelas do `mi_thermald`.

---

## 📁 Estrutura do Repositório

```text
thermal-topaz/
├── flashable_modules/                     # Módulos prontos em .zip para Magisk / KernelSU / APatch
│   ├── Topaz_Thermal_Mod_Gaming_Performance.zip
│   ├── Topaz_Thermal_Mod_Extreme_NoLimits.zip
│   ├── Topaz_Thermal_Mod_Balanced.zip
│   └── Topaz_Thermal_Mod_Fast_Charge.zip
│
├── stock_decrypted/                       # Arquivos stock originais descriptografados (Texto puro)
│   ├── thermal-normal.conf                # Perfil padrão do sistema
│   ├── thermal-tgame.conf                 # Perfil ativado pelo Game Turbo
│   ├── thermal-nolimits.conf              # Perfil sem limites de fábrica
│   ├── thermal-camera.conf                # Perfil de câmera
│   ├── thermal-chg-only.conf              # Perfil durante carregamento
│   ├── thermal-map.conf                   # Mapeamento de perfis (sconfig ID -> arquivo)
│   ├── thermal-navigation.conf            # Perfil de GPS/Navegação
│   ├── thermal-phone.conf                 # Perfil de chamadas
│   ├── thermal-video.conf                 # Perfil de reprodução de vídeo
│   ├── thermal-videochat.conf             # Perfil de chamadas de vídeo
│   ├── thermal-class0.conf                # Perfil class0
│   ├── thermal-engine.conf                # Qualcomm thermal base
│   └── thermald-devices.conf              # Definição de dispositivos de resfriamento
│
├── stock_encrypted/                       # Arquivos stock originais criptografados (Binários do dump)
│
├── mods/                                  # Configurações modificadas geradas
│   ├── gaming_performance/                # Mod Gaming & Performance
│   ├── extreme_nolimits/                  # Mod Extreme / Sem Limites
│   ├── balanced/                          # Mod Balanceado (Daily Driver)
│   └── fast_charge/                       # Mod Focado em Carregamento Rápido
│
└── tools/                                 # Scripts utilitários em Python
    ├── mi_thermal_tool.py                 # Descriptografa e criptografa arquivos .conf
    ├── extract_thermal_from_dump.py       # Varre e extrai thermals de qualquer dump / pasta / zip
    ├── generate_mods.py                   # Gera as configurações dos 4 perfis de mod
    └── build_magisk_modules.py            # Compila os pacotes .zip instaláveis via Magisk
```

---

## 🔐 Como Funciona a Criptografia da Xiaomi (`mi_thermald`)

O binário `/vendor/bin/mi_thermald` só aceita arquivos de configuração `.conf` criptografados. Se você colocar um arquivo em texto simples em `/vendor/etc/`, o daemon irá ignorá-lo ou fechar com erro.

- **Algoritmo:** `AES-128-CBC` com preenchimento `PKCS#7`
- **Chave (Key):** `thermalopenssl.h` (`746865726d616c6f70656e73736c2e68`)
- **Vetor de Inicialização (IV):** `thermalopenssl.h` (`746865726d616c6f70656e73736c2e68`)

Nossa ferramenta `mi_thermal_tool.py` realiza essa conversão instantaneamente.

---

## 📦 Módulos Prontos para Flash

Na pasta `flashable_modules/` você encontra 4 variantes prontas:

| Módulo | Descrição | Recomendação |
|---|---|---|
| **`Topaz_Thermal_Mod_Gaming_Performance.zip`** | Mantém clock alto (2.8/2.4GHz), desativa hotplug (8 núcleos sempre ativos), remove escurecimento de tela em jogos e eleva o limite térmico em +10°C. | 🎮 **Recomendado para Jogos e Uso Geral** |
| **`Topaz_Thermal_Mod_Extreme_NoLimits.zip`** | Remove quase todas as travas térmicas (mantém apenas trava de segurança crítica a 58°C). Zero throttling intermediário. | 🚀 **Máximo Desempenho e Benchmarks** |
| **`Topaz_Thermal_Mod_Balanced.zip`** | Ganho moderado (+5°C de margem), elimina a queda brusca para 800MHz (trava mínima em 1.34GHz) mantendo o aparelho frio. | 🔋 **Uso Diário Equilibrado** |
| **`Topaz_Thermal_Mod_Fast_Charge.zip`** | Focado em manter a velocidade total de 33W Turbo Charging mesmo com o aparelho aquecido, além do perfil gaming. | ⚡ **Carregamento Mais Rápido** |

### Como Instalar:
1. Abra o **Magisk**, **KernelSU** ou **APatch**.
2. Vá em **Módulos** -> **Instalar a partir do armazenamento**.
3. Selecione o `.zip` desejado.
4. Reinicie o dispositivo.

---

## 🔍 Como Extrair o Thermal de um Dump Próprio

Se você tiver uma pasta com o dump da ROM, partições extraídas (`vendor.img`, `odm.img`) ou um arquivo `.zip` da ROM:

```bash
# Extrair e descriptografar automaticamente todos os thermals:
python3 tools/extract_thermal_from_dump.py -i /caminho/do/seu/dump -o ./meu_thermal_extraido
```

O script irá:
1. Localizar automaticamente todos os arquivos `thermal-*.conf` e `thermald-*.conf`.
2. Descriptografar para `.conf` legível na subpasta `decrypted/`.
3. Exibir uma análise detalhada dos pontos de acionamento de temperatura (temperaturas de corte de CPU, GPU, Bateria e Tela).

---

## 🛠️ Como Modificar os Arquivos de Configuração

### 1. Descriptografar um arquivo:
```bash
python3 tools/mi_thermal_tool.py decrypt -i stock_encrypted/thermal-normal.conf -o custom-normal.conf
```

### 2. Editar com seu editor preferido:
Abra `custom-normal.conf` e altere os valores conforme desejado (veja o guia abaixo).

### 3. Criptografar de volta para o formato do `mi_thermald`:
```bash
python3 tools/mi_thermal_tool.py encrypt -i custom-normal.conf -o thermal-normal.conf
```

### 4. Gerar novos módulos .zip automaticamente:
Após editar os arquivos em `mods/`, execute:
```bash
python3 tools/generate_mods.py
python3 tools/build_magisk_modules.py
```

---

## 📖 Entendendo os Parâmetros Térmicos (.conf)

Cada bloco de configuração no arquivo `.conf` controla um algoritmo de proteção:

### 1. Throttling de CPU Big Cluster (Cortex-A73)
```ini
[Normal-SS-CPU4]
algo_type   ss
sensor      VIRTUAL-SENSOR
device      cpu4
polling     1000
trig        35000       37000       40000       44000       46500       47500
clr         33000       35000       38000       42000       45000       46500
target      2592000     2400000     2208000     1766400     1344000     806400
```
- `trig`: Temperaturas em mili-graus Celsius para acionar o corte (ex: `35000` = 35°C, `44000` = 44°C).
- `clr`: Temperaturas para limpar o corte e restaurar a frequência.
- `target`: Clock máximo permitido em kHz (ex: `2592000` = 2.59 GHz, `806400` = 806 MHz).
- **Como moddar:** Aumente os valores de `trig` (ex: `45000 48000 50000...`) para adiar o throttling, e aumente o menor valor de `target` para não cair para 800MHz.

### 2. Desligamento de Núcleos (Hotplug)
```ini
[Normal-MONITOR-CCC_CTRL]
algo_type   monitor
sensor      VIRTUAL-SENSOR
device      hotplug_cpu6+hotplug_cpu7
polling     1000
trig        49000
clr         47000
target      1+1
```
- A 49°C (`49000`), o sistema desliga a CPU6 e CPU7 (`1+1`).
- **Como moddar:** Aumente `trig` para `65000` e `clr` para `62000` para manter todos os 8 núcleos sempre ligados.

### 3. Redução de Brilho da Tela
```ini
[Normal-MONITOR-LCD]
algo_type   monitor
sensor      VIRTUAL-SENSOR
device      backlight
polling     1000
trig        41000       43000       46000
clr         40000       42000       45000
target      12          100         155
```
- A 41°C, o brilho da tela sofre redução.
- **Como moddar:** Eleve `trig` para `60000` ou remova a regra para manter brilho total mesmo em dias quentes.

### 4. Carregamento da Bateria
```ini
[Normal-MONITOR-BAT]
algo_type   monitor
sensor      VIRTUAL-SENSOR
device      battery
polling     1000
trig        35000   36000   37000   38000   39000 ...
clr         34000   35000   36000   37000   38000 ...
target      500     700     801     902     1103 ...
```
- Cada nível de target reduz a corrente de carga (mA).
- **Como moddar:** Eleve os primeiros `trig` para 40°C - 43°C para garantir carga rápida contínua.

---

## 🔀 Troca Dinâmica de Perfis via Root (`sconfig`)

O arquivo `thermal-map.conf` define qual configuração é usada por cada modo:

| ID (`sconfig`) | Arquivo de Configuração | Cenário de Uso |
|---|---|---|
| `0` | `thermal-normal.conf` | Uso diário padrão |
| `9` | `thermal-tgame.conf` | Game Turbo / Jogos |
| `10` | `thermal-nolimits.conf` | Modo Extremo / Sem Limites |
| `12` | `thermal-camera.conf` | Aplicativo de Câmera |
| `14` | `thermal-youtube.conf` | Reprodução de Mídia |
| `19` | `thermal-navigation.conf` | GPS / Waze / Maps |

Você pode alternar o perfil ativo a qualquer momento no **Termux** com root:
```bash
su
# Ativar modo Game Turbo manualmente:
echo 9 > /sys/class/thermal/thermal_message/sconfig

# Ativar modo Sem Limites:
echo 10 > /sys/class/thermal/thermal_message/sconfig

# Voltar para o modo normal:
echo 0 > /sys/class/thermal/thermal_message/sconfig
```

---

## 📲 Instalação Manual via Root / ADB

Se preferir copiar os arquivos manualmente sem Magisk:

```bash
# Conecte o aparelho no computador via ADB com root:
adb root
adb remount

# Enviar os arquivos criptografados para /vendor/etc:
adb push mods/gaming_performance/encrypted/*.conf /vendor/etc/

# Ajustar permissões:
adb shell chmod 0644 /vendor/etc/thermal*.conf
adb shell chown root:root /vendor/etc/thermal*.conf

# Limpar cache do mi_thermald e reiniciar daemon:
adb shell rm -f /data/vendor/thermal/config/*
adb shell stop mi_thermald
adb shell start mi_thermald
```

---

## ⚠️ Avisos e Isenção de Responsabilidade
- O aumento dos limites térmicos permite que o dispositivo opere em temperaturas ligeiramente maiores para manter alta taxa de quadros (FPS) sustentada.
- Todos os perfis deste repositório mantêm salvaguardas de emergência de hardware ativas contra sobreaquecimento crítico.
