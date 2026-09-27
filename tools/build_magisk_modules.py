#!/usr/bin/env python3
"""
Magisk / KernelSU / APatch Module Builder for Redmi Note 12 4G (topaz / tapas)
"""

import os
import shutil
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODS_DIR = BASE_DIR / "mods"
OUTPUT_ZIP_DIR = BASE_DIR / "flashable_modules"

UPDATE_BINARY_CONTENT = """#!/sbin/sh
##########################################################################################
#
# Magisk Module Installer Script
#
##########################################################################################

OUTFD=$2
ZIPFILE=$3

# Extract update-binary-flags
MODPATH="${0%/*}"

# Set up ui_print
ui_print() {
  echo -e "$1"
}

ui_print "************************************"
ui_print "   Redmi Note 12 4G Thermal Mod     "
ui_print "      Device: topaz / tapas         "
ui_print "************************************"

# Magisk module install execution
if [ -f "$ZIPFILE" ]; then
  unzip -o "$ZIPFILE" 'module.prop' -d "$MODPATH" >&2
  unzip -o "$ZIPFILE" 'customize.sh' -d "$MODPATH" >&2
  unzip -o "$ZIPFILE" 'service.sh' -d "$MODPATH" >&2
  unzip -o "$ZIPFILE" 'system/*' -d "$MODPATH" >&2
fi

exit 0
"""

UPDATER_SCRIPT_CONTENT = "#MAGISK\n"

CUSTOMIZE_SH_CONTENT = """# Magisk / KernelSU / APatch module customize script
ui_print "- Installing Topaz Thermal Config Mod..."

# Verify architecture / platform
DEVICE_PRODUCT=$(getprop ro.product.device)
DEVICE_NAME=$(getprop ro.build.product)
CHIPSET=$(getprop ro.board.platform)

ui_print "- Detected Device: $DEVICE_PRODUCT ($CHIPSET)"

if [ "$DEVICE_PRODUCT" != "topaz" ] && [ "$DEVICE_PRODUCT" != "tapas" ] && [ "$CHIPSET" != "bengal" ] && [ "$CHIPSET" != "khaje" ]; then
  ui_print "  [!] Warning: This module is designed for Redmi Note 12 4G (topaz/tapas - SM6225)."
  ui_print "  Proceeding anyway on user confirmation..."
fi

# Set proper permissions for vendor etc files
ui_print "- Setting permissions..."
set_perm_recursive $MODPATH/system/vendor/etc 0 0 0755 0644
set_perm_recursive $MODPATH/system/vendor/bin 0 0 0755 0755 2>/dev/null

# Clean old thermal caches
rm -rf /data/vendor/thermal/config/* 2>/dev/null

ui_print "- Thermal optimization successfully installed!"
ui_print "- Please reboot your device to apply changes."
"""

SERVICE_SH_CONTENT = """#!/system/bin/sh
# Restart mi_thermald or apply sconfig on boot completed

while [ "$(getprop sys.boot_completed)" != "1" ]; do
  sleep 2
done

# Ensure permissions
chmod 0664 /sys/class/thermal/thermal_message/sconfig 2>/dev/null
chmod 0666 /sys/class/thermal/thermal_message/temp_state 2>/dev/null

# Reset thermal daemon caches if needed
if [ -d /data/vendor/thermal/config ]; then
  rm -f /data/vendor/thermal/config/* 2>/dev/null
fi
"""


def create_module_zip(preset_name: str, display_name: str, desc: str, source_enc_dir: Path):
    OUTPUT_ZIP_DIR.mkdir(parents=True, exist_ok=True)
    zip_filename = OUTPUT_ZIP_DIR / f"Topaz_Thermal_Mod_{preset_name}.zip"

    prop_content = f"""id=topaz_thermal_{preset_name.lower()}
name=Topaz Thermal Mod - {display_name}
version=v1.3
versionCode=130
author=Ctps1234
description={desc}
"""

    with zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        # META-INF
        zf.writestr("META-INF/com/google/android/update-binary", UPDATE_BINARY_CONTENT)
        zf.writestr("META-INF/com/google/android/updater-script", UPDATER_SCRIPT_CONTENT)
        
        # Scripts & Prop
        zf.writestr("module.prop", prop_content)
        zf.writestr("customize.sh", CUSTOMIZE_SH_CONTENT)
        zf.writestr("service.sh", SERVICE_SH_CONTENT)

        # Thermal config files into system/vendor/etc/
        for conf in source_enc_dir.glob("*.conf"):
            zf.write(conf, f"system/vendor/etc/{conf.name}")

    print(f"[+] Built module: {zip_filename.name} ({zip_filename.stat().st_size} bytes)")


def main():
    presets = [
        (
            "Safe_Delay",
            "Safe Mild Delay (Adiar Throttling Seguro)",
            "Delays thermal throttling safely by ~5-6C. Eliminates 35-38C lag while preserving all stock thermal safeguards, hotplug protection, and battery safety.",
            MODS_DIR / "safe_delay" / "encrypted"
        ),
        (
            "Normal_AntiThrottling",
            "Thermal Normal (Anti-Throttling & No-Lag)",
            "Fixes premature thermal throttling at 35-38C on Redmi Note 12 4G (topaz/tapas). Maintains full CPU clocks until 48C, prevents drops to 800MHz, and keeps all 8 cores active.",
            MODS_DIR / "thermal_normal_anti_throttling" / "encrypted"
        ),
        (
            "Gaming_Performance",
            "Gaming & Performance",
            "Redmi Note 12 4G (topaz/tapas) thermal mod. Relaxes CPU throttling, keeps all 8 cores active (no hotplug), and disables screen brightness dimming in games.",
            MODS_DIR / "gaming_performance" / "encrypted"
        ),
        (
            "Extreme_NoLimits",
            "Extreme / No Limits",
            "Maximum sustained clock rates for Redmi Note 12 4G. Removes thermal limits up to 58C safety cutoff. Maximum FPS for gaming and benchmarks.",
            MODS_DIR / "extreme_nolimits" / "encrypted"
        ),
        (
            "Balanced",
            "Balanced Daily Driver",
            "Smoothed thermal curve with +5C headroom. Eliminates sudden 800MHz drops, keeps 8 cores active, and balances performance with cool battery temperatures.",
            MODS_DIR / "balanced" / "encrypted"
        ),
        (
            "Fast_Charge",
            "Fast Charging Focused",
            "Maintains 33W Fast Turbo Charging at higher operating temperatures while keeping smooth gaming performance.",
            MODS_DIR / "fast_charge" / "encrypted"
        )
    ]

    for preset_name, display_name, desc, enc_dir in presets:
        create_module_zip(preset_name, display_name, desc, enc_dir)


if __name__ == "__main__":
    main()
