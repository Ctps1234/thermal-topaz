# 🔥 Topaz Thermal Engine Mod & Extractor Tool

Repositório completo de extração, descriptografia, análise, modificação e criação de módulos Magisk/KernelSU para os arquivos térmicos do **Redmi Note 12 4G / 12 4G NFC** (Codinomes: `topaz` / `tapas` - Snapdragon 685 / SM6225).

---

## 📋 Índice
1. [O Problema do Thermal Stock a 38°C](#-o-problema-do-thermal-stock-a-38c)
2. [Mod Seguro: Apenas Adiar o Throttling (Safe Delay)](#-mod-seguro-apenas-adiar-o-throttling-safe-delay)
3. [Tabela Comparativa: Stock vs Mod Seguro](#-tabela-comparativa-stock-vs-mod-seguro)
4. [Módulos Prontos para Flash (Magisk / KernelSU / APatch)](#-módulos-prontos-para-flash)
5. [Estrutura do Repositório](#-estrutura-do-repositório)
6. [Como Funciona a Criptografia da Xiaomi (`mi_thermald`)](#-como-funciona-a-criptografia-da-xiaomi-mi_thermald)
7. [Como Modificar os Arquivos de Configuração](#-como-modificar-os-arquivos-de-configuração)
8. [Como Extrair o Thermal de um Dump Próprio](#-como-extrair-o-thermal-de-um-dump-próprio)
9. [Troca Dinâmica de Perfis via Root (`sconfig`)](#-troca-dinâmica-de-perfis-via-root-sconfig)
10. [Instalação Manual via Root / ADB](#-instalação-manual-via-root--adb)

---

## ❄️ O Problema do Thermal Stock a 38°C

No **Redmi Note 12 4G (topaz/tapas)**, a MIUI / HyperOS aplica uma política térmica excessivamente conservadora no perfil padrão (`thermal-normal.conf`):

- 📉 **Throttling Prematuro:** O cluster de alta performance (Cortex-A73) começa a cortar o clock aos **35°C**, e ao atingir **38°C - 40°C** já reduziu para 2.4 - 2.2 GHz.
- 🚨 **Queda Brusca para 806 MHz:** Aos **47.5°C**, o clock despenca para 806 MHz, causando engasgos visíveis na interface e travamentos em jogos.
- 🚫 **Desligamento de Núcleos (Hotplug):** Aos 49°C, o sistema desliga `CPU6` e `CPU7`.

---

## 🛡️ Mod Seguro: Apenas Adiar o Throttling (Safe Delay)

Se você **não quer temperaturas perigosas** e **não quer desativar as proteções**, mas quer apenas que o celular **não trave aos 38°C**, o perfil **Safe Delay** é a escolha ideal:

- ✅ **Sem temperaturas extremas:** Mantém o teto de operação normal do aparelho.
- ✅ **Apenas adia o início do throttling em ~5°C a 6°C:** O throttling que começava a 35°C agora começa de forma suave aos **41°C**.
- ✅ **Aos 38°C:** O celular opera com clock total (2.8 GHz) com **zero travamentos**.
- ✅ **Todas as proteções preservadas:**
  - Redução gradual de clock ativa a partir de 41°C.
  - Hotplug de segurança ativo a 52°C.
  - Redução de brilho de proteção ativa a 45°C.
  - Proteção de resfriamento da bateria ativa a partir de 39°C.
  - Clock mínimo de segurança em 806 MHz caso o aparelho continue esquentando além de 51°C.

---

## 📊 Tabela Comparativa: Stock vs Mod Seguro

| Temperatura | Stock (Original) | Mod Seguro (Safe Delay) | O que acontece na prática |
|:---:|:---:|:---:|---|
| **< 35°C** | 2.80 GHz | **2.80 GHz** | Clock máximo |
| **35°C** | 📉 2.59 GHz *(Throttling precoce)* | **2.80 GHz** | 🚀 Sem perda de clock |
| **37°C - 38°C** | 📉 2.40 GHz *(Começa a travar)* | **2.80 GHz** | 🚀 **Fluidez total aos 38°C** |
| **40°C** | 📉 2.20 GHz | **2.80 GHz** | 🚀 Desempenho mantido |
| **41.0°C** | 📉 2.20 GHz | **2.59 GHz** | 🛡️ Início suave do controle térmico |
| **43.0°C** | 📉 1.76 GHz | **2.40 GHz** | 🛡️ Redução gradual segura |
| **45.0°C** | 📉 1.76 GHz | **2.20 GHz** | 🛡️ Redução gradual segura |
| **47.0°C** | 🚨 **806 MHz** *(Travamento)* | **1.76 GHz** | 🛡️ Sem despencar para 800MHz precocemente |
| **49.0°C** | 🚨 806 MHz | **1.34 GHz** | 🛡️ Resfriamento seguro em alta temperatura |
| **51.0°C** | 🚨 806 MHz | **806 MHz** | 🔒 **Proteção térmica máxima preservada** |
| **Hotplug** | ❌ Desliga núcleos a 49°C | 🛡️ **Proteção mantida a 52°C** | Núcleos ativos durante uso moderado |
| **Brilho** | 🔅 Escurece a 41°C | 🛡️ **Proteção adiada para 45°C** | Brilho não cai em temperatura ambiente |

---

## 📦 Módulos Prontos para Flash

Na pasta `flashable_modules/` você encontra os módulos `.zip` prontos para instalação no **Magisk**, **KernelSU** ou **APatch**:

| Módulo | Descrição | Nível de Agressividade |
|---|---|:---:|
| **`Topaz_Thermal_Mod_Safe_Delay.zip`** | **Recomendado:** Apenas adia o throttling em ~5°C (começa aos 41°C em vez de 35°C). Resolve os travamentos aos 38°C mantendo 100% das proteções de segurança térmicas. | 🟢 **100% Seguro / Equilibrado** |
| **`Topaz_Thermal_Mod_Normal_AntiThrottling.zip`** | Mantém clock alto até 48°C, piso travado em 1.53GHz, desativa hotplug e mantém brilho livre até 60°C. | 🟡 **Desempenho Estendido** |
| **`Topaz_Thermal_Mod_Gaming_Performance.zip`** | Margem estendida para jogos pesados tanto no perfil normal quanto no Game Turbo (`thermal-tgame`). | 🟠 **Foco em Jogos** |
| **`Topaz_Thermal_Mod_Extreme_NoLimits.zip`** | Remove quase todas as travas térmicas intermediárias (salvaguarda de emergência a 58°C). | 🔴 **Extremo / Benchmarks** |
| **`Topaz_Thermal_Mod_Balanced.zip`** | Margem moderada (+5°C), elimina a queda para 800MHz e mantém consumo balanceado. | 🟢 **Uso Diário Moderado** |
| **`Topaz_Thermal_Mod_Fast_Charge.zip`** | Focado em evitar que o carregamento rápido de 33W seja reduzido a 35°C-38°C. | 🟢 **Carga Rápida** |

### Como Instalar:
1. Baixe o módulo `.zip` desejado (ex: `Topaz_Thermal_Mod_Safe_Delay.zip`).
2. Abra o aplicativo do **Magisk**, **KernelSU** ou **APatch**.
3. Vá em **Módulos** -> **Instalar a partir do armazenamento** -> Selecione o arquivo `.zip`.
4. Reinicie o celular.

---

## 📁 Estrutura do Repositório

```text
thermal-topaz/
├── flashable_modules/                     # Módulos prontos em .zip para Magisk / KernelSU / APatch
│   ├── Topaz_Thermal_Mod_Safe_Delay.zip             <-- Mod seguro (adiamento leve)
│   ├── Topaz_Thermal_Mod_Normal_AntiThrottling.zip
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
│   ├── safe_delay/                        # Mod Seguro (adiamento leve de 5°C)
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
adb push mods/safe_delay/encrypted/*.conf /vendor/etc/
adb shell chmod 0644 /vendor/etc/thermal*.conf
adb shell rm -f /data/vendor/thermal/config/*
adb shell stop mi_thermald
adb shell start mi_thermald
```
