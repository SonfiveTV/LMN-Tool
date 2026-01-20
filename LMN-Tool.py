#!/usr/bin/env python3
"""
LMN Tool (Lightweight Mod Navigation Tool)
"""

import os
import sys
import subprocess
from pathlib import Path

# ================= CONFIG =================

BASE_DIR = Path(__file__).resolve().parent
PROFILES_DIR = BASE_DIR / "profiles"
MODS_DIR = BASE_DIR.parent / "Mods"
BALATRO_APPID = "2379780"

PROTECTED_MODS = {"lovely", "Steamodded", "smods"}
UPDATE_EXCLUDE = {"PokermonPlus"}

LAUNCH_METHOD = "steam"  # steam | mac_lovely

# macOS Lovely launcher (adjust if needed)
MAC_LOVELY_SCRIPT = Path.home() / "Library/Application Support/Steam/steamapps/common/Balatro/run_lovely_macos.sh"

# ==========================================

PROFILES_DIR.mkdir(exist_ok=True)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def list_mods():
    mods = []
    for d in MODS_DIR.iterdir():
        if not d.is_dir():
            continue
        if d.name in PROTECTED_MODS:
            continue
        mods.append(d)
    return sorted(mods, key=lambda p: p.name.lower())


def is_enabled(mod):
    return not (mod / ".lovelyignore").exists()


def toggle_mod(mod):
    ignore = mod / ".lovelyignore"
    if ignore.exists():
        ignore.unlink()
        print(f"Enabled  {mod.name}")
    else:
        ignore.touch()
        print(f"Disabled {mod.name}")


def display_menu(mods):
    clear()
    print("     LMN Tool")
    print("------------------\n")

    for i, mod in enumerate(mods, 1):
        status = "[ON ]" if is_enabled(mod) else "[OFF]"
        print(f"{i:2}) {status} {mod.name}")

    print("""
Commands:
  Numbers → Toggle mods (space-separated)
  U = Update mods
  S = Save profile
  L = Load profile
  O = Launch Balatro
  Q = Quit
""")


def save_profile(mods):
    name = input("Enter profile name to save: ").strip()
    if not name:
        return

    path = PROFILES_DIR / f"{name}.profile"
    with path.open("w") as f:
        for mod in mods:
            if is_enabled(mod):
                f.write(mod.name + "\n")

    print(f"Profile '{name}' saved.")



def load_profile(mods):
    profiles = list(PROFILES_DIR.glob("*.profile"))
    if not profiles:
        print("No profiles saved.")

        return

    print("\nSaved profiles:")
    for i, p in enumerate(profiles, 1):
        print(f"{i}) {p.stem}")

    choice = input("Select profile number: ").strip()
    if not choice.isdigit():
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(profiles):
        return

    enabled = {line.strip() for line in profiles[idx].read_text().splitlines()}

    for mod in mods:
        ignore = mod / ".lovelyignore"
        if mod.name in enabled:
            ignore.unlink(missing_ok=True)
        else:
            ignore.touch()

    print("Profile loaded.")



def update_mods(mods):
    print("Updating mods...\n")
    for mod in mods:
        if mod.name in UPDATE_EXCLUDE:
            continue
        if not (mod / ".git").exists():
            continue

        print(f"Updating {mod.name}")
        subprocess.run(["git", "pull"], cwd=mod)

    input("Press Enter to continue...")




def launch_balatro():
    print("Launching Balatro...")

    # ===== macOS (Lovely launcher only) =====
    if sys.platform == "darwin":
        lovely_script = (
            Path.home()
            / "Library/Application Support/Steam/steamapps/common/Balatro/run_lovely_macos.sh"
        )

        print("macOS detected — using Lovely launcher")

        if not lovely_script.is_file():
            print("\nERROR: run_lovely_macos.sh not found.")
            print("Balatro mods cannot be launched via Steam on macOS.")
            input("Press Enter to return...")
            return

        subprocess.Popen(
            ["sh", str(lovely_script)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return

    # ===== Linux =====
    if sys.platform.startswith("linux"):
        subprocess.Popen(
            ["steam", f"steam://rungameid/{BALATRO_APPID}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return

    # ===== Windows =====
    if sys.platform.startswith("win"):
        subprocess.Popen(
            ["cmd", "/c", "start", "", f"steam://rungameid/{BALATRO_APPID}"],
            shell=True
        )
        return

    print("Unsupported OS")
    input("Press Enter to return...")


def main():
    while True:
        mods = list_mods()
        display_menu(mods)
        choice = input("Enter choice: ").strip()

        if not choice:
            continue

        upper = choice.upper()

        if upper == "Q":
            break
        elif upper == "O":
            launch_balatro()
        elif upper == "U":
            update_mods(mods)
        elif upper == "S":
            save_profile(mods)
        elif upper == "L":
            load_profile(mods)
        else:
            for part in choice.split():
                if part.isdigit():
                    idx = int(part) - 1
                    if 0 <= idx < len(mods):
                        toggle_mod(mods[idx])



if __name__ == "__main__":
    main()
