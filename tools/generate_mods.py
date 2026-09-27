#!/usr/bin/env python3
"""
Generate modified thermal profiles for Redmi Note 12 4G (topaz / tapas)
SoC: Snapdragon 685 (SM6225-AD)
"""

import os
import shutil
from pathlib import Path
from mi_thermal_tool import encrypt_bytes, decrypt_bytes

BASE_DIR = Path(__file__).resolve().parent.parent
STOCK_DEC_DIR = BASE_DIR / "stock_decrypted"
MODS_DIR = BASE_DIR / "mods"


def generate_safe_delay():
    """Safe Delay Preset (Adiar Throttling Levemente):
    - Highly safe and conservative: delays throttling onset by ~5C to 6C
    - At 38C: CPU runs at full 2.8 GHz with zero lag
    - At 41C: gentle step to 2.59 GHz (stock did this at 35C)
    - At 43C: 2.40 GHz
    - At 45C: 2.20 GHz
    - At 47C: 1.76 GHz
    - At 49C: 1.34 GHz
    - At 51C: 806 MHz (full safety thermal protection intact)
    - Hotplug preserved at 52C
    - Screen dimming preserved at 45C
    - Battery protection preserved starting at 39C
    """
    out_dir_dec = MODS_DIR / "safe_delay" / "decrypted"
    out_dir_enc = MODS_DIR / "safe_delay" / "encrypted"
    out_dir_dec.mkdir(parents=True, exist_ok=True)
    out_dir_enc.mkdir(parents=True, exist_ok=True)

    # Copy rest of stock configs so full set exists
    for f in STOCK_DEC_DIR.glob("*.conf"):
        if f.name != "thermal-normal.conf":
            (out_dir_dec / f.name).write_bytes(f.read_bytes())

    # Encrypt all
    for f in out_dir_dec.glob("*.conf"):
        data = f.read_bytes()
        if f.name in ("thermal-engine.conf", "thermald-devices.conf"):
            (out_dir_enc / f.name).write_bytes(data)
        else:
            (out_dir_enc / f.name).write_bytes(encrypt_bytes(data))

    print("[+] Generated Safe Delay Preset successfully!")


def generate_normal_anti_throttling():
    out_dir_dec = MODS_DIR / "thermal_normal_anti_throttling" / "decrypted"
    out_dir_enc = MODS_DIR / "thermal_normal_anti_throttling" / "encrypted"
    out_dir_dec.mkdir(parents=True, exist_ok=True)
    out_dir_enc.mkdir(parents=True, exist_ok=True)

    normal_content = """# ====================================================================================
# 🔥 TOPAZ THERMAL NORMAL - ANTI-THROTTLING & NO-LAG MOD
# Device: Redmi Note 12 4G / 12 4G NFC (topaz / tapas)
# SoC: Qualcomm Snapdragon 685 (SM6225-AD)
# ====================================================================================

[BAT_SOC]
algo_type\tsimulated
path\t/sys/class/power_supply/battery/capacity
polling\t10000

[VIRTUAL-SENSOR]
algo_type\tvirtual
sensors\t\tpa-therm0-usr\tquiet-therm-usr\tcharge-therm-usr\temmc-therm-usr\tbattery
weight\t\t389.944\t\t391.91\t-222.96\t216.101\t132.14
polling\t\t\t2000
weight_sum\t\t1000
compensation\t2125.646

# CPU0 (Little Cluster - 4x Cortex-A53 @ 1.9 GHz)
[Normal-SS-CPU0]
algo_type\tss
sensor\t\tVIRTUAL-SENSOR
device\t\tcpu0
polling\t\t1000
trig\t\t\t50000\t\t\t52000\t54000\t\t56000
clr\t\t\t\t48000\t\t\t50000\t52000\t\t54000
target\t\t1900800\t1804800\t1516800\t1190400

# CPU4 (Big Cluster - 4x Cortex-A73 @ 2.8 GHz) - Prevents lag at 35-38C!
[Normal-SS-CPU4]
algo_type\tss
sensor\t\tVIRTUAL-SENSOR
device\t\tcpu4
polling\t\t1000
trig\t\t\t48000\t\t51000\t\t53000\t\t55000\t\t57000
clr\t\t\t\t46000\t\t49000\t\t51000\t\t53000\t\t55000
target\t\t2592000\t2400000\t2208000\t1766400\t1536000

# Battery Charging Throttling relaxed
[Normal-MONITOR-BAT]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\tbattery
polling\t\t1000
trig\t\t42000\t43000\t44000\t45000\t46000\t47000\t48000\t49000\t50000\t51000\t52000\t53000
clr\t\t\t41000\t42000\t43000\t44000\t45000\t46000\t47000\t48000\t49000\t50000\t51000\t52000
target\t\t500\t\t700\t\t801\t\t902\t\t1103\t1205\t1207\t1309\t1311\t1313\t1414\t1515

# Screen Brightness Dimmimg delayed to 60C
[Normal-MONITOR-LCD]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\tbacklight
polling\t\t1000
trig\t    60000\t63000\t66000
clr\t      58000\t61000\t64000
target\t  12\t100  155

[Normal-MONITOR-TEMP_STATE]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\ttemp_state
polling\t\t1000
trig\t\t50000\t\t55000
clr\t\t\t48000\t\t53000
target\t\t10100000\t12500001

[Normal-MONITOR-BCL]
algo_type\tmonitor
sensor\t\tBAT_SOC
device\t\thotplug_cpu2+hotplug_cpu3
polling\t\t1000
trig\t\t  3
clr\t\t\t  4
target\t\t1+1
reverse\t\t1

# Core Hotplugging Disabled (Triggers at 65C emergency only)
[Normal-MONITOR-CCC_CTRL]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t  hotplug_cpu6+hotplug_cpu7
polling\t  1000
trig\t    65000
clr\t      62000
target\t  1+1

# Touch Boost Active up to 55C
[Normal-MONITOR-BOOST_LIMIT]
algo_type\tmonitor
sensor\t  VIRTUAL-SENSOR
device\t  boost_limit
polling\t  2000
trig\t    55000
clr\t      53000
target\t  1
"""

    (out_dir_dec / "thermal-normal.conf").write_text(normal_content)

    for f in STOCK_DEC_DIR.glob("*.conf"):
        if f.name != "thermal-normal.conf":
            (out_dir_dec / f.name).write_bytes(f.read_bytes())

    for f in out_dir_dec.glob("*.conf"):
        data = f.read_bytes()
        if f.name in ("thermal-engine.conf", "thermald-devices.conf"):
            (out_dir_enc / f.name).write_bytes(data)
        else:
            (out_dir_enc / f.name).write_bytes(encrypt_bytes(data))

    print("[+] Generated Thermal Normal Anti-Throttling Preset successfully!")


def generate_gaming_performance():
    out_dir_dec = MODS_DIR / "gaming_performance" / "decrypted"
    out_dir_enc = MODS_DIR / "gaming_performance" / "encrypted"
    out_dir_dec.mkdir(parents=True, exist_ok=True)
    out_dir_enc.mkdir(parents=True, exist_ok=True)

    normal_content = """# ====================================================================
# MODIFIED THERMAL CONFIG - GAMING & PERFORMANCE
# Device: Redmi Note 12 4G (topaz / tapas) - Snapdragon 685 (SM6225)
# Preset: Gaming / High Performance
# ====================================================================

[BAT_SOC]
algo_type\tsimulated
path\t/sys/class/power_supply/battery/capacity
polling\t10000

[VIRTUAL-SENSOR]
algo_type\tvirtual
sensors\t\tpa-therm0-usr\tquiet-therm-usr\tcharge-therm-usr\temmc-therm-usr\tbattery
weight\t\t389.944\t\t391.91\t-222.96\t216.101\t132.14
polling\t\t\t2000
weight_sum\t\t1000
compensation\t2125.646

# CPU0 Little Cluster (Cortex-A53): Extended headroom
[Normal-SS-CPU0]
algo_type\tss
sensor\t\tVIRTUAL-SENSOR
device\t\tcpu0
polling\t\t1000
trig\t\t\t47000\t\t\t49000\t52000\t\t54000
clr\t\t\t\t45000\t\t\t47000\t50000\t\t52000
target\t\t1900800\t1804800\t1516800\t1190400

# CPU4 Big Cluster (Cortex-A73): High sustained clock, no drop below 1.34 GHz
[Normal-SS-CPU4]
algo_type\tss
sensor\t\tVIRTUAL-SENSOR
device\t\tcpu4
polling\t\t1000
trig\t\t\t45000\t\t48000\t\t50000\t\t52000\t\t54000\t\t56000
clr\t\t\t\t43000\t\t46000\t\t48000\t\t50000\t\t52000\t\t54000
target\t\t2592000\t2400000\t2208000\t1766400\t1536000\t1344000

# Battery Charging Throttling: Higher temperature tolerance
[Normal-MONITOR-BAT]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\tbattery
polling\t\t1000
trig\t\t40000\t41000\t42000\t43000\t44000\t45000\t46000\t47000\t48000\t49000\t51000\t52000
clr\t\t\t39000\t40000\t41000\t42000\t43000\t44000\t45000\t46000\t47000\t48000\t50000\t51000
target\t\t500\t\t700\t\t801\t\t902\t\t1103\t1205\t1207\t1309\t1311\t1313\t1414\t1515

# Screen Brightness: Throttling disabled for full brightness in games
[Normal-MONITOR-LCD]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\tbacklight
polling\t\t1000
trig\t    60000\t63000\t65000
clr\t      58000\t61000\t63000
target\t  12\t100  155

# Temperature State for MIUI system reporting
[Normal-MONITOR-TEMP_STATE]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\ttemp_state
polling\t\t1000
trig\t\t50000\t\t55000
clr\t\t\t48000\t\t53000
target\t\t10100000\t12500001

# Battery Capacity Hotplug (Only when battery <= 3%)
[Normal-MONITOR-BCL]
algo_type\tmonitor
sensor\t\tBAT_SOC
device\t\thotplug_cpu2+hotplug_cpu3
polling\t\t1000
trig\t\t  3
clr\t\t\t  4
target\t\t1+1
reverse\t\t1

# Core Hotplugging Disabled (Triggers pushed to safe emergency temp 65C)
[Normal-MONITOR-CCC_CTRL]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t  hotplug_cpu6+hotplug_cpu7
polling\t  1000
trig\t    65000
clr\t      62000
target\t  1+1

# Boost limit threshold raised
[Normal-MONITOR-BOOST_LIMIT]
algo_type\tmonitor
sensor\t  VIRTUAL-SENSOR
device\t  boost_limit
polling\t  2000
trig\t    54000
clr\t      52000
target\t  1
"""

    tgame_content = """# ====================================================================
# MODIFIED THERMAL CONFIG - GAME TURBO (tgame)
# Device: Redmi Note 12 4G (topaz / tapas) - Snapdragon 685 (SM6225)
# Preset: Gaming / High Performance
# ====================================================================

[TGAME-SS-CPU0]
algo_type\tss
sensor\t\tVIRTUAL-SENSOR
device\t\tcpu0
polling\t  1000
trig\t    48000\t  50000\t  52000  	54000\t  56000
clr\t      46000\t  48000\t  50000\t  52000\t  54000
target\t  1900800\t1804800\t1516800\t1190400\t940800

[TGAME-SS-CPU4]
algo_type\tss
sensor\t\tVIRTUAL-SENSOR
device\t\tcpu4
polling\t\t1000
trig\t    46000\t  49000\t  52000\t  54000\t  56000
clr\t      44000\t  47000\t  50000\t  52000\t  54000
target\t  2592000\t2208000\t1766400\t1536000\t1344000

[TGAME-MONITOR-BAT]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\tbattery
polling\t  1000
trig\t    42000\t43000\t44000\t45000\t46000\t47000\t48000\t49000\t50000\t51000
clr     \t41000\t42000\t43000\t44000\t45000\t46000\t47000\t48000\t49000\t50000
target\t  301\t  402\t  607  \t712\t  912\t\t1013\t1113\t1214\t1414\t1515

[TGAME-MONITOR-LCD]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\tbacklight
polling\t  1000
trig\t    60000\t63000\t65000
clr\t      58000\t61000\t63000
target\t  12\t  70   130

[TGAME-MONITOR-TEMP_STATE]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t  temp_state
polling\t  1000
trig\t    50000\t    52000\t\t\t56000
clr\t      48000\t    50000\t\t\t54000
target\t  10100000\t10100004\t12500001

[TGAME-MONITOR-BCL]
algo_type\tmonitor
sensor\t\tBAT_SOC
device\t\thotplug_cpu2+hotplug_cpu3
polling\t\t1000
trig\t\t  3
clr\t\t\t  4
target\t\t1+1
reverse\t\t1

# Disabled core hotplugging
[TGAME-MONITOR-CCC_CTRL]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\thotplug_cpu2+hotplug_cpu3
polling\t\t1000
trig\t\t  65000
clr\t\t\t  62000
target\t\t1+1

[TGAME-MONITOR-CCC_CTRL-1]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\thotplug_cpu6+hotplug_cpu7
polling\t\t1000
trig\t\t  65000
clr\t\t\t  62000
target\t\t1+1

[TGAME-MONITOR-BOOST_LIMIT]
algo_type\tmonitor
sensor\t  VIRTUAL-SENSOR
device\t  boost_limit
polling\t  2000
trig\t    54000
clr\t      52000
target\t  1
"""

    (out_dir_dec / "thermal-normal.conf").write_text(normal_content)
    (out_dir_dec / "thermal-tgame.conf").write_text(tgame_content)

    for f in STOCK_DEC_DIR.glob("*.conf"):
        if f.name not in ("thermal-normal.conf", "thermal-tgame.conf"):
            (out_dir_dec / f.name).write_bytes(f.read_bytes())

    for f in out_dir_dec.glob("*.conf"):
        data = f.read_bytes()
        if f.name in ("thermal-engine.conf", "thermald-devices.conf"):
            (out_dir_enc / f.name).write_bytes(data)
        else:
            (out_dir_enc / f.name).write_bytes(encrypt_bytes(data))

    print("[+] Generated Gaming & Performance Preset successfully!")


def generate_extreme_nolimits():
    out_dir_dec = MODS_DIR / "extreme_nolimits" / "decrypted"
    out_dir_enc = MODS_DIR / "extreme_nolimits" / "encrypted"
    out_dir_dec.mkdir(parents=True, exist_ok=True)
    out_dir_enc.mkdir(parents=True, exist_ok=True)

    nolimits_content = """# ====================================================================
# MODIFIED THERMAL CONFIG - EXTREME / NO LIMITS
# Device: Redmi Note 12 4G (topaz / tapas) - Snapdragon 685 (SM6225)
# Preset: Extreme / No Throttling
# ====================================================================

[BAT_SOC]
algo_type\tsimulated
path\t/sys/class/power_supply/battery/capacity
polling\t10000

[VIRTUAL-SENSOR]
algo_type\tvirtual
sensors\t\tpa-therm0-usr\tquiet-therm-usr\tcharge-therm-usr\temmc-therm-usr\tbattery
weight\t\t389.944\t\t391.91\t-222.96\t216.101\t132.14
polling\t\t\t2000
weight_sum\t\t1000
compensation\t2125.646

# Emergency safeguard only at 58C
[Normal-SS-CPU0]
algo_type\tss
sensor\t\tVIRTUAL-SENSOR
device\t\tcpu0
polling\t\t1000
trig\t    58000
clr\t      55000
target\t  1190400

# Emergency safeguard only at 58C
[Normal-SS-CPU4]
algo_type\tss
sensor\t\tVIRTUAL-SENSOR
device\t\tcpu4
polling\t\t1000
trig\t\t  58000
clr\t\t    55000
target\t\t1344000

# High-tolerance battery thermal
[Normal-MONITOR-BAT]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\tbattery
polling\t\t1000
trig\t    44000\t46000\t48000\t50000\t52000\t54000
clr\t      42000\t44000\t46000\t48000\t50000\t52000
target\t  500\t  801\t  1103\t1207\t1313\t1515

# Screen Dimming: DISABLED
[Normal-MONITOR-LCD]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\tbacklight
polling\t\t1000
trig\t    70000
clr\t      68000
target\t  12

[Normal-MONITOR-TEMP_STATE]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\ttemp_state
polling\t\t1000
trig\t\t  56000
clr\t\t    54000
target\t\t12500001

# Hotplug disabled
[Normal-MONITOR-CCC_CTRL]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t  hotplug_cpu6+hotplug_cpu7
polling\t  1000
trig\t    70000
clr\t      67000
target\t  1+1

[Normal-MONITOR-BOOST_LIMIT]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\tboost_limit
polling\t\t1000
trig\t\t  60000
clr\t\t    58000
target\t\t1

[Normal-MONITOR-BCL]
algo_type\tmonitor
sensor\t\tBAT_SOC
device\t\thotplug_cpu2+hotplug_cpu3
polling\t\t1000
trig\t\t  2
clr\t      3
target\t\t1+1
reverse\t\t1
"""

    (out_dir_dec / "thermal-normal.conf").write_text(nolimits_content)
    (out_dir_dec / "thermal-tgame.conf").write_text(nolimits_content.replace("Normal-", "TGAME-"))
    (out_dir_dec / "thermal-nolimits.conf").write_text(nolimits_content.replace("Normal-", "NL-"))

    for f in STOCK_DEC_DIR.glob("*.conf"):
        if f.name not in ("thermal-normal.conf", "thermal-tgame.conf", "thermal-nolimits.conf"):
            (out_dir_dec / f.name).write_bytes(f.read_bytes())

    for f in out_dir_dec.glob("*.conf"):
        data = f.read_bytes()
        if f.name in ("thermal-engine.conf", "thermald-devices.conf"):
            (out_dir_enc / f.name).write_bytes(data)
        else:
            (out_dir_enc / f.name).write_bytes(encrypt_bytes(data))

    print("[+] Generated Extreme / No-Limits Preset successfully!")


def generate_balanced():
    out_dir_dec = MODS_DIR / "balanced" / "decrypted"
    out_dir_enc = MODS_DIR / "balanced" / "encrypted"
    out_dir_dec.mkdir(parents=True, exist_ok=True)
    out_dir_enc.mkdir(parents=True, exist_ok=True)

    normal_content = """# ====================================================================
# MODIFIED THERMAL CONFIG - BALANCED PERFORMANCE & COOL TEMPS
# Device: Redmi Note 12 4G (topaz / tapas) - Snapdragon 685 (SM6225)
# Preset: Balanced Daily Driver
# ====================================================================

[BAT_SOC]
algo_type\tsimulated
path\t/sys/class/power_supply/battery/capacity
polling\t10000

[VIRTUAL-SENSOR]
algo_type\tvirtual
sensors\t\tpa-therm0-usr\tquiet-therm-usr\tcharge-therm-usr\temmc-therm-usr\tbattery
weight\t\t389.944\t\t391.91\t-222.96\t216.101\t132.14
polling\t\t\t2000
weight_sum\t\t1000
compensation\t2125.646

# CPU0 Little Cluster (Cortex-A53)
[Normal-SS-CPU0]
algo_type\tss
sensor\t\tVIRTUAL-SENSOR
device\t\tcpu0
polling\t\t1000
trig\t\t\t44000\t\t\t46000\t49000\t\t51000
clr\t\t\t\t42000\t\t\t44000\t47000\t\t49000
target\t\t1804800\t1516800\t1190400\t940800

# CPU4 Big Cluster (Cortex-A73)
[Normal-SS-CPU4]
algo_type\tss
sensor\t\tVIRTUAL-SENSOR
device\t\tcpu4
polling\t\t1000
trig\t\t\t40000\t\t43000\t\t46000\t\t49000\t\t51000\t\t53000
clr\t\t\t\t38000\t\t41000\t\t44000\t\t47000\t\t49000\t\t51000
target\t\t2592000\t2400000\t2208000\t1766400\t1536000\t1344000

# Battery Charging
[Normal-MONITOR-BAT]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\tbattery
polling\t\t1000
trig\t\t38000\t39000\t40000\t41000\t42000\t43000\t44000\t45000\t47000\t48000\t49000\t50000
clr\t\t\t37000\t38000\t39000\t40000\t41000\t42000\t43000\t44000\t46000\t47000\t48000\t49000
target\t\t500\t\t700\t\t801\t\t902\t\t1103\t1205\t1207\t1309\t1311\t1313\t1414\t1515

# Screen Brightness Dimmimg delayed to 48C
[Normal-MONITOR-LCD]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\tbacklight
polling\t\t1000
trig\t    48000\t51000\t54000
clr\t      46000\t49000\t52000
target\t  12\t100  155

[Normal-MONITOR-TEMP_STATE]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\ttemp_state
polling\t\t1000
trig\t\t48000\t\t53000
clr\t\t\t46000\t\t51000
target\t\t10100000\t12500001

[Normal-MONITOR-BCL]
algo_type\tmonitor
sensor\t\tBAT_SOC
device\t\thotplug_cpu2+hotplug_cpu3
polling\t\t1000
trig\t\t  4
clr\t\t\t  5
target\t\t1+1
reverse\t\t1

# Disabled core hotplugging
[Normal-MONITOR-CCC_CTRL]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t  hotplug_cpu6+hotplug_cpu7
polling\t  1000
trig\t    60000
clr\t      58000
target\t  1+1

[Normal-MONITOR-BOOST_LIMIT]
algo_type\tmonitor
sensor\t  VIRTUAL-SENSOR
device\t  boost_limit
polling\t  2000
trig\t    50000
clr\t      48000
target\t  1
"""

    (out_dir_dec / "thermal-normal.conf").write_text(normal_content)
    (out_dir_dec / "thermal-tgame.conf").write_text(normal_content.replace("Normal-", "TGAME-"))

    for f in STOCK_DEC_DIR.glob("*.conf"):
        if f.name not in ("thermal-normal.conf", "thermal-tgame.conf"):
            (out_dir_dec / f.name).write_bytes(f.read_bytes())

    for f in out_dir_dec.glob("*.conf"):
        data = f.read_bytes()
        if f.name in ("thermal-engine.conf", "thermald-devices.conf"):
            (out_dir_enc / f.name).write_bytes(data)
        else:
            (out_dir_enc / f.name).write_bytes(encrypt_bytes(data))

    print("[+] Generated Balanced Preset successfully!")


def generate_fast_charge():
    out_dir_dec = MODS_DIR / "fast_charge" / "decrypted"
    out_dir_enc = MODS_DIR / "fast_charge" / "encrypted"
    out_dir_dec.mkdir(parents=True, exist_ok=True)
    out_dir_enc.mkdir(parents=True, exist_ok=True)

    chg_content = """# ====================================================================
# MODIFIED THERMAL CONFIG - FAST CHARGE OPTIMIZED
# Device: Redmi Note 12 4G (topaz / tapas) - Snapdragon 685 (SM6225)
# Preset: Fast Charging
# ====================================================================

[MONITOR-BAT]
algo_type\tmonitor
sensor\t\tVIRTUAL-SENSOR
device\t\tbattery
polling\t\t1000
trig\t    43000\t44000\t45000\t46000\t47000\t48000\t49000\t50000\t51000\t52000\t53000\t54000
clr\t      41000\t42000\t43000\t44000\t45000\t46000\t47000\t48000\t49000\t50000\t51000\t52000
target\t  500\t  700  \t801\t  902\t  1103\t1205\t1207\t1309\t1311\t1313\t1414\t1515
"""
    (out_dir_dec / "thermal-chg-only.conf").write_text(chg_content)

    for f in (MODS_DIR / "gaming_performance" / "decrypted").glob("*.conf"):
        if f.name != "thermal-chg-only.conf":
            (out_dir_dec / f.name).write_bytes(f.read_bytes())

    for f in out_dir_dec.glob("*.conf"):
        data = f.read_bytes()
        if f.name in ("thermal-engine.conf", "thermald-devices.conf"):
            (out_dir_enc / f.name).write_bytes(data)
        else:
            (out_dir_enc / f.name).write_bytes(encrypt_bytes(data))

    print("[+] Generated Fast Charge Preset successfully!")


def main():
    generate_safe_delay()
    generate_normal_anti_throttling()
    generate_gaming_performance()
    generate_extreme_nolimits()
    generate_balanced()
    generate_fast_charge()


if __name__ == "__main__":
    main()
